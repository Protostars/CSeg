import re
from math import log
from hmm import HMMSeg

DICT_FILE = "data/dict.txt"
BI_GRAM_FILE = "data/bi_gram.txt"
# 识别汉字、数字和字母、全角字符，及+,#,&,.,%
re_ch = re.compile("([\u4E00-\u9FD5a-zA-Z0-9\uFF10-\uFF5A+#&\._%％]+)", re.U)
# 当切分出来的单独字符超过MAX_ALLOW_CHAR后，使用HMM重新切分
MAX_ALLOW_CHAR = 1
MIN_FLOAT = -3.14e100


class CSeg:

    def __init__(self):
        self.dict = {}
        self.bi_gram = {}
        self.word_count = 0
        self.initialized = False
        self.bi_initialized = False
        self.d = 0.
        self.p_kn = {}  # Kneser–Ney中的P_kn
        self.hmm_seg = HMMSeg()

    def __load_dict(self):
        self.dict = {}
        self.word_count = 0
        with open(DICT_FILE, 'r', encoding='utf8') as f:
            for line in f:
                if not line: continue
                word, freq = line.strip().split(' ')[:2]
                freq = int(freq)
                self.dict[word] = freq
                self.word_count += freq
                for i in range(2, len(word)):  # 不使用Trie树，需要将前缀都加入到字典中，但单个字符没有必要加入
                    prefix = word[:i]
                    if prefix not in self.dict: self.dict[prefix] = 0
        self.initialized = True

    def __load_bigram(self):
        with open(BI_GRAM_FILE, 'r', encoding='utf8') as f:
            for line in f:
                if not line: continue
                b1, b2, freq = line.strip().split(' ')[:3]
                freq = int(freq)
                if b1 not in self.bi_gram:
                    self.bi_gram[b1] = [0, {}]  # 内容分别是：以b1开始的2-gram数量，b2字典
                self.bi_gram[b1][0] += freq
                self.bi_gram[b1][1][b2] = freq
        n1, n2 = 0., 0.  # n_i 出现i次的2-gram数量
        bi_count = 0.
        for k, v in self.bi_gram.items():
            # 计数，统计每个gram之前出现的不同单词数目
            for b2 in v[1].keys():
                self.p_kn[b2] = self.p_kn.get(b2, 0) + 1
                if v[1][b2] == 1:
                    n1 += 1
                elif v[1][b2] == 2:
                    n2 += 1
            bi_count += len(v[1])
        for k in self.p_kn.keys():
            self.p_kn[k] /= bi_count
        self.d = n1/(n1+2*n2)
        self.bi_initialized = True

    def __build_DAG(self, sentence):
        length = len(sentence)
        DAG = []
        for i in range(length):
            node = [i+1]  # 记录节点的全部可能的后继，每个字符是一个节点
            t = 2
            while i+t <= length:
                word = sentence[i:i+t]
                if word in self.dict:
                    if self.dict[word] > 0: node.append(i+t)
                    t += 1
                else:
                    break
            DAG.append(node)
        return DAG

    def __build_2gram_DAG(self, DAG):
        bi_DAG = []
        for i, succs in enumerate(DAG):
            level_nodes = []
            for succ in succs:
                level_nodes.append([i, succ])
            bi_DAG.append(level_nodes)
        return bi_DAG

    def __prob_calc(self, sentence, DAG):
        i = len(DAG)
        prob_path = [(0., 0) for _ in range(i+1)]  # 记录从每个节点出发的最大路径概率和对应的后继
        i -= 1
        log_pbase = log(self.word_count)
        # 动态规划求解，使用对数避免概率下溢
        while i >= 0:
            prob_path[i] = max((log(self.dict.get(sentence[i:succ], 1))-log_pbase+prob_path[succ][0], succ)
                               for succ in DAG[i])
            i -= 1
        return prob_path

    # Kneser–Ney平滑
    def __get_kneser_ney_prob(self, prev, succ):
        if prev not in self.bi_gram:
            return MIN_FLOAT
        p1 = max(self.bi_gram[prev][1].get(succ, 0) - self.d, 0.) / self.bi_gram[prev][0]
        p2 = self.d / self.bi_gram[prev][0] * len(self.bi_gram[prev][1]) * self.p_kn.get(succ, 0.)
        prob = p1 + p2
        if prob > 0:
            return log(prob)
        else:
            return MIN_FLOAT

    # 绝对减值平滑
    def __get_abs_prob(self, prev, succ):
        if prev not in self.bi_gram:
            return MIN_FLOAT
        p1 = max(self.bi_gram[prev][1].get(succ, 0) - self.d, 0.) / self.bi_gram[prev][0]
        p2 = self.d / self.bi_gram[prev][0] * len(self.bi_gram[prev][1]) * self.dict.get(succ, 0.)/self.word_count
        prob = p1 + p2
        if prob > 0:
            return log(prob)
        else:
            return MIN_FLOAT

    # +1平滑
    def __get_add1_prob(self, prev, succ):
        if prev not in self.bi_gram:
            return MIN_FLOAT
        count = self.bi_gram[prev][1].get(succ, 0.) + 1.
        return count / (self.bi_gram[prev][0] + self.word_count + 2.)  # <EOS> <BOS>

    def __prob_calc_2gram(self, sentence, DAG, smooth='kneser_ney'):
        i = len(DAG)
        bi_DAG = self.__build_2gram_DAG(DAG)
        prob_path = [[(0., 0) for _ in range(len(bi_DAG[t]))] for t in range(i)]  # 记录从每个节点出发的最大路径概率和对应的后继
        prob_path.append([(0., 0)])
        i -= 1
        smooth_probs = {'kneser_ney': self.__get_kneser_ney_prob, 'add1': self.__get_add1_prob,
                        'abs': self.__get_abs_prob}
        smooth_prob = smooth_probs[smooth]
        # 从后向前逐层求解（每个字符对应一层），使用对数避免概率下溢
        while i >= 0:
            for j, prev in enumerate(bi_DAG[i]):  # 求解层中以每个词开始的句子的最大概率
                prob_list = []
                w_prev = sentence[prev[0]:prev[1]]  # 当前词
                target_level = prev[1]  # 当前词的后继所在的层
                if target_level >= len(bi_DAG):  # 后继是句尾
                    w_succ = '<EOS>'
                    prob = smooth_prob(w_prev, w_succ)
                    if i == 0:
                        prob += smooth_prob('<BOS>', w_prev)
                    prob_path[i][j] = (prob, 0)
                    continue
                for k, succ in enumerate(bi_DAG[target_level]):  # 求解当前词和每个后继词的2-gram概率
                    w_succ = sentence[succ[0]:succ[1]]
                    if not w_succ: w_succ = '<EOS>'
                    prob = smooth_prob(w_prev, w_succ) + prob_path[target_level][k][0]
                    if i == 0:
                        prob += smooth_prob('<BOS>', w_prev)
                    prob_list.append((prob, k))
                prob_path[i][j] = max(prob_list)
            i -= 1
        # 调整概率路径的形式，使其和1-gram计算的形式一致
        bi_prob_path = [(0., 0) for _ in range(len(prob_path)-1)]
        i = 0
        while True:
            if i >= len(bi_prob_path): break
            m = max(prob_path[i])
            index = prob_path[i].index(m)
            bi_prob_path[i] = (m[0], bi_DAG[i][index][1])
            i = bi_DAG[i][index][1]
        return bi_prob_path

    def __cut_sentence(self, sentence, hmm=True, bi_gram=True, smooth='kneser_ney'):
        DAG = self.__build_DAG(sentence)
        if bi_gram:
            prob_path = self.__prob_calc_2gram(sentence, DAG, smooth)
        else:
            prob_path = self.__prob_calc(sentence, DAG)
        i = 0
        char_buf = ''
        while i < len(sentence):
            word = sentence[i:prob_path[i][1]]
            if len(word) == 1:
                char_buf += word
            else:
                if char_buf:
                    if len(char_buf) <= MAX_ALLOW_CHAR:
                        for elem in char_buf:
                            yield elem
                        char_buf = ''
                    else:
                        # 如果有超过MAX_ALLOW_CHAR个字符被单独切分，考虑使用HMM重新切分
                        if not self.dict.get(char_buf) and hmm:
                            recognized = self.hmm_seg.cut(char_buf)
                            for t in recognized:
                                yield t
                        else:
                            for elem in char_buf:
                                yield elem
                        char_buf = ''
                yield word
            i = prob_path[i][1]
        if char_buf:
            if len(char_buf) <= MAX_ALLOW_CHAR:
                for elem in char_buf:
                    yield elem
            elif not self.dict.get(char_buf) and hmm:
                recognized = self.hmm_seg.cut(char_buf)
                for t in recognized:
                    yield t
            else:
                for elem in char_buf:
                    yield elem

    def cut(self, text, hmm=True, bi_gram=True, smooth='kneser_ney'):
        if not self.initialized:
            self.__load_dict()
        if bi_gram and not self.bi_initialized:
            self.__load_bigram()
        sentences = re_ch.split(text)
        for sentence in sentences:
            if not sentence: continue
            if re_ch.match(sentence):
                for word in self.__cut_sentence(sentence, hmm, bi_gram, smooth):
                    yield word
            else:
                for x in sentence:
                    yield x


c_seg = CSeg()


def cut_file(input, output, use_hmm=True, bi_gram=True, smooth='kneser_ney'):
    with open(input, 'r', encoding='utf8') as input_f:
        with open(output, 'w', encoding='utf8') as output_f:
            for line in input_f:
                if not line:
                    output_f.write('\n')
                else:
                    seg_list = c_seg.cut(line.strip(), use_hmm, bi_gram,smooth)
                    outline = '  '.join(seg_list)
                    output_f.write(outline+'\n')


def cut_text(text, use_hmm=True, bi_gram=True, smooth='kneser_ney'):
    return c_seg.cut(text, use_hmm, bi_gram, smooth)



s='我来到位于怀柔的雁栖湖。如果有超过MAX_ALLOW_CHAR个字符被单独切分，考虑使用HMM重新切分。'
print("|".join(cut_text(s)))
print("|".join(cut_text(s, False)))
print("|".join(cut_text(s, True, False)))
print("|".join(cut_text(s, False, False)))
