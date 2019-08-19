import re
import os
import pickle
import sys
from math import log

DICT_NAME = "dict.txt"
BI_GRAM_FILE = "bi_gram.txt"
HMM_PROB = "hmm_prob"
SMALL_PROB = 1e-200

# 识别汉字、数字和字母、全角字符，及+,#,&,.,%
re_ch = re.compile("([\u4E00-\u9FD5a-zA-Z0-9\uFF10-\uFF5A+#&\._%％]+)", re.U)
re_stop = re.compile("([。，]+)", re.U)

# 处理分词语料，生成词典和2-gram列表
# 语料内容：每行一个句子，词用空格分开
def process(input_file, output_path):
    words = {}
    bi_grams = {}
    max_word_length = 0
    m_w = ''
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            word_line = line.split()
            last_word = '<BOS>'
            for w in word_line:
                if re_ch.match(w):
                    words[w] = words.get(w, 0) + 1  # 没匹配到的是一些符号：、，等等
                    if last_word:
                        bg = last_word + ' ' + w
                        bi_grams[bg] = bi_grams.get(bg, 0) + 1
                    last_word = w
                    if len(w) > max_word_length:
                        max_word_length = len(w)
                        m_w = w
                elif re_stop.match(w):
                    if last_word:
                        bg = last_word + ' <EOS>'
                        bi_grams[bg] = bi_grams.get(bg, 0) + 1
                        last_word = '<BOS>'
            if last_word:
                bg = last_word + ' <EOS>'
                bi_grams[bg] = bi_grams.get(bg, 0) + 1
    print("字典大小：%d" % len(words))
    print("最长词长度：%d %s" % (max_word_length,m_w))
    with open(os.path.join(output_path, DICT_NAME), 'w', encoding='utf8') as f:
        for k in sorted(words):
            f.write("%s %d\n" % (k, words[k]))
    print("2-gram 数量：%d" % len(bi_grams))
    with open(os.path.join(output_path, BI_GRAM_FILE), 'w', encoding='utf8') as f:
        for k in sorted(bi_grams):
            f.write("%s %d\n" % (k, bi_grams[k]))


# 估计HMM模型的概率
def process_hmm(input_file, output_path):
    line_count = 0
    state_list = ['B', 'M', 'E', 'S']
    A = {}
    B = {}
    Pi = {}
    State_Count = {}
    for s in state_list:
        A[s] = {t: 0. for t in state_list}  # 转移概率
        B[s] = {}  # 观测概率
        Pi[s] = 0.  # 初始概率
        State_Count[s] = 0
    print('开始估计HMM概率...')
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            line_count += 1
            line = line.strip()
            if not line: continue
            word_list = line.split()
            chars = ''.join(word_list)
            states = []
            for w in word_list:
                if len(w) == 1: states.append('S')
                else: states += ['B']+['M']*(len(w)-2)+['E']
            assert len(chars) == len(states)
            i = 0
            for s in states:
                State_Count[s] += 1
                if i == 0:
                    Pi[s] += 1.
                else:
                    A[states[i-1]][s] += 1.
                    B[s][chars[i]] = B[s].get(chars[i], 0) + 1.
                i += 1
        A = {k: {tk: log(max(tv/State_Count[k], SMALL_PROB)) for tk, tv in v.items()} for k, v in A.items()}
        B = {k: {tk: log(max(tv/State_Count[k], SMALL_PROB)) for tk, tv in v.items()} for k, v in B.items()}
        Pi = {k: log(max(v/line_count, SMALL_PROB)) for k, v in Pi.items()}
    with open(os.path.join(output_path, HMM_PROB), 'wb') as f:
        pickle.dump(A, f)
        pickle.dump(B, f)
        pickle.dump(Pi, f)


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 2:
        print('corpus_process.py <corpus_file> <out_dir>')
        sys.exit()
    else:
        process(argv[0], argv[1])
        process_hmm(argv[0], argv[1])
        print("处理完成")


