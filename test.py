import os
import sys
from cseg import cut_file

msr_test = 'corpus/msr_test.utf8'
msr_test_gold = 'corpus/msr_test_gold.utf8'
msr_out = ['output/msr_test_2_add1', 'output/msr_test_2_ad', 'output/msr_test_2_kn', 'output/msr_test_1',
           'output/msr_test_2_add1_hmm', 'output/msr_test_2_ad_hmm',
           'output/msr_test_2_kn_hmm',  'output/msr_test_1_hmm']

pku_test = 'corpus/pku_test.utf8'
pku_test_gold = 'corpus/pku_test_gold.utf8'
pku_out = ['output/pku_test_2_add1', 'output/pku_test_2_ad', 'output/pku_test_2_kn', 'output/pku_test_1',
           'output/pku_test_2_add1_hmm', 'output/pku_test_2_ad_hmm', 'output/pku_test_2_kn_hmm', 'output/pku_test_1_hmm']

weibo_test = 'corpus/nlpcc2016-wordseg-dev.dat'
weibo_test_gold = 'corpus/nlpcc2016-wordseg-dev_gold.dat'
weibo_out = ['output/weibo_test_2_add1', 'output/weibo_test_2_ad', 'output/weibo_test_2_kn', 'output/weibo_test_1',
             'output/weibo_test_2_add1_hmm', 'output/weibo_test_2_ad_hmm', 'output/weibo_test_2_kn_hmm', 'output/weibo_test_1_hmm']

tips = ["2-gram, +1平滑：", "2-gram, 绝对减值平滑：", "2-gram, Kneser-Ney平滑：", "1-gram：", "HMM: 2-gram, +1平滑：",
        "HMM: 2-gram, 绝对减值平滑：", "HMM: 2-gram, Kneser-Ney平滑：", "HMM: 1-gram："]
use_hmm = [False, False, False, False, True, True, True, True]
use_2gram = [True, True, True, False, True, True, True, False]
smooth = ['add1', 'abs', 'kneser_ney', '', 'add1', 'abs', 'kneser_ney', '']

tests = {'msr': msr_test, 'pku': pku_test, 'weibo': weibo_test }
test_golds = {'msr': msr_test_gold, 'pku': pku_test_gold, 'weibo': weibo_test_gold }
outs = {'msr': msr_out, 'pku': pku_out, 'weibo': weibo_out }

if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 1:
        print('test.py msr|pku|weibo')
        sys.exit()
    else:
        if argv[0] not in ['msr', 'pku', 'weibo']:
            print('test.py msr|pku|weibo')
            sys.exit()
        print("开始切分... ")
        test = tests[argv[0]]
        test_gold = test_golds[argv[0]]
        out = outs[argv[0]]
        for i in range(len(out)):
            cut_file(test, out[i], use_hmm[i], use_2gram[i], smooth[i])
        print("%s 测试结果： " % argv[0])
        for i in range(len(out)):
            print(tips[i])
            os.system("python eval.py %s %s %s" % (test_gold, out[i], out[i]+'_err'))
