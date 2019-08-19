import pickle

HMM_PROB_FILE = "data/hmm_prob"
MIN_FLOAT = -3.14e100


class HMMSeg:

    def __init__(self):
        self.A = {}  # 状态转移概率
        self.B = {}  # 观测概率
        self.Pi = {}  # 初始概率
        self.states = ['B', 'M', 'E', 'S']
        self.prev_status = {
            'B': 'ES',
            'M': 'MB',
            'S': 'SE',
            'E': 'BM'
        }
        self.initialized = False

    def __load_prob(self):
        with open(HMM_PROB_FILE, 'rb') as f:
            self.A = pickle.load(f)
            self.B = pickle.load(f)
            self.Pi = pickle.load(f)
            self.initialized = True

    def __viterbi(self, text):
        V = [{}]
        path = {}  # 记录每个隐状态对应的最大概率路径
        for s in self.states:
            # 在HMM_PROB文件中，概率已经是对数的形式了
            V[0][s] = self.Pi[s] + self.B[s].get(text[0], MIN_FLOAT)
            path[s] = s
        for i in range(1, len(text)):
            V.append({})
            newpath = {}
            for s in self.states:
                em_p = self.B[s].get(text[i], MIN_FLOAT)
                prob, state = max((V[i - 1][ts] + self.A[ts].get(s) + em_p, ts) for ts in self.prev_status[s])
                V[i][s] = prob
                newpath[s] = path[state] + s
            path = newpath
        prob, state = max((V[len(text) - 1][s], s) for s in 'ES')
        return prob, path[state]

    def cut(self, text):
        if not self.initialized:
            self.__load_prob()
        prob, path = self.__viterbi(text)
        begin, next = 0, 0
        for i in range(len(text)):
            state = path[i]
            if state == 'B':
                begin = i
            elif state == 'E':
                yield text[begin:i+1]
                next = i+1
            elif state == 'S':
                yield text[i]
                next = i+1
        if next < len(text):
            yield text[next:]

