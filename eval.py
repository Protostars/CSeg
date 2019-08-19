import sys


def seg_eval(truth, test, err=''):
    with open(truth, 'r', encoding='utf8') as ftruth:
        truth_lines = ftruth.readlines()
    with open(test, 'r', encoding='utf8') as ftest:
        test_lines = ftest.readlines()

    truth_word_count = 0.
    test_word_count = 0.
    right_count = 0.
    err_dict = {}
    line_no = 1
    for truth_line, test_line in zip(truth_lines, test_lines):
        truth_words = truth_line.strip().split()
        test_words = test_line.strip().split()

        truth_word_count += len(truth_words)
        test_word_count += len(test_words)

        truth_index = set()
        index = 0
        for word in truth_words:
            truth_index.add('%d-%d' %(index, index+len(word)))
            index += len(word)

        test_index = set()
        index = 0
        for word in test_words:
            test_index.add('%d-%d' %(index, index+len(word)))
            index += len(word)

        right_count += len(truth_index.intersection(test_index))

        if err:
            # 先从参考答案中找出没有分对的词，之后从测试结果中找出实际的切分结果
            err_index = truth_index.difference(test_index)
            t_line = ''.join(truth_words)
            for ei in err_index:
                indexes = ei.split('-')
                err_words = []
                b, e = int(indexes[0]), int(indexes[1])
                correct_word = t_line[b:e]
                for ti in test_index:
                    tis = ti.split('-')
                    tb, te = int(tis[0]), int(tis[1])
                    if b <= tb < e or b < te <= e:
                        err_words.append((tb, t_line[tb:te]))
                err_words.sort()
                if len(err_words) > 0:
                    if correct_word not in err_dict:
                        err_dict[correct_word] = []
                    e = '|'.join(list(zip(*err_words))[1])
                    err_dict[correct_word].append(e + '(%d)' % line_no)
            line_no += 1
    if err:
        with open(err, 'w', encoding='utf8') as ferr:
            for k in sorted(err_dict, key=lambda x:len(err_dict[x]), reverse = True):
                ferr.write('%d\t%s\t:\t%s\n' % (len(err_dict[k]), k, '  '.join(err_dict[k])))

    P = right_count/test_word_count
    R = right_count/truth_word_count
    F1 = 2*P*R/(P+R)
    return P, R, F1


if __name__ == '__main__':
    argv = sys.argv[1:]
    if len(argv) < 2:
        print('eval.py <truthfile> <testfile> <errfile>(optional)')
        sys.exit()
    else:
        print('evaluating...')
        err_file = ''
        if len(argv)>2: err_file = argv[2]
        P, R, F1 = seg_eval(argv[0], argv[1], err_file)
        print('precision: %f  recall: %f  f1: %f' % (P, R, F1))
