# CSeg
## 简单的基于混合方法的中文分词器

方法基本和jieba一致：
 - 使用词典对句子进行初步的切分，找出所有词的切分位置，构成一个DAG。
 - 使用动态规划方法，在DAG上找到1-gram概率值最大的切分路径。
 - 如果在划分过程中出现了多个单字符切分，使用由字构词的HMM对这个单字符序列再次切分，这样可以提高发现未登录词的能力。

不过这里还尝试了如下做法：
 - 在求概率最大的切分路径时，改用2-gram语言模型。
 - 比较2-gram中不同的平滑方式：+1平滑、绝对减值平滑和Kneser-Ney平滑对分词效果的影响。

CSeg目录下的文件如下：
```
CSeg
│ corpus_process.py # 语料处理程序，生成词典，2-gram统计信息和HMM概率估计信息
│ cseg.py # 分词器主程序
│ eval.py # 验证程序，可计算分词的准确率、召回率和F1，同时可找出所有划分错误的词
│ hmm.py # 基于hmm模型的辅助分词程序，用于进一步切分
│ test.py # 测试程序
│
├─corpus # 语料目录，包含SIGHAN2005中的pkr、msr数据集和NLPCC2016的微博数据集
│ msr_test.utf8 # test: 测试语料
│ msr_test_gold.utf8 # glod：分词参考答案
│ msr_training.utf8 # train: 训练语料
│ nlpcc2016-word-seg-train.dat
│ nlpcc2016-wordseg-dev.dat
│ nlpcc2016-wordseg-dev_gold.dat
│ pku_test.utf8
│ pku_test_gold.utf8
│ pku_training.utf8
│
├─data # CSeg使用的处理后的语料数据，包含2-gram统计信息，词典和hmm概率估计信息
│ bi_gram.txt
│ dict.txt
│ hmm_prob
│
└─output # 测试输出目录
```
默认data目录下的语料是使用corpus_process程序处理MSR语料后的结果，可使用corpus_process.py处理其他语料，分词主程序位于cseg.py中，test.py是测试程序

测试结果

<escape>
<table>
   <tr>
      <td colspan="2"></td>
      <td colspan="3">PKU</td>
      <td colspan="3">MSR</td>
      <td colspan="3">Weibo</td>
   </tr>
   <tr>
      <td></td>
      <td></td>
      <td>P</td>
      <td>R</td>
      <td>F1</td>
      <td>P</td>
      <td>R</td>
      <td>F1</td>
      <td>P</td>
      <td>R</td>
      <td>F1</td>
   </tr>
   <tr>
      <td rowspan="3">2-gram</td>
      <td>+1</td>
      <td>0.4960</td>
      <td>0.6903</td>
      <td>0.5772</td>
      <td>0.4931</td>
      <td>0.7039</td>
      <td>0.5799</td>
      <td>0.4614</td>
      <td>0.6630</td>
      <td>0.5441</td>
   </tr>
   <tr>
      <td>绝对减值</td>
      <td>0.7928</td>
      <td>0.8890</td>
      <td>0.8381</td>
      <td>0.8984</td>
      <td>0.9538</td>
      <td>0.9253</td>
      <td>0.7575</td>
      <td>0.8698</td>
      <td>0.8097</td>
   </tr>
   <tr>
      <td>Kneser-Ney</td>
      <td>0.8122</td>
      <td>0.8986</td>
      <td>0.8532</td>
      <td>0.9195</td>
      <td>0.9629</td>
      <td>0.9407</td>
      <td>0.7932</td>
      <td>0.8892</td>
      <td>0.8385</td>
   </tr>
   <tr>
      <td colspan="2">1-gram</td>
      <td>0.8507</td>
      <td>0.9181</td>
      <td>0.8831</td>
      <td>0.9238</td>
      <td>0.9639</td>
      <td>0.9434</td>
      <td>0.8210</td>
      <td>0.9062</td>
      <td>0.8615</td>
   </tr>
   <tr>
      <td colspan="11"></td>
   </tr>
   <tr>
      <td rowspan="3">2-gram +HMM</td>
      <td>+1</td>
      <td>0.7794</td>
      <td>0.7925</td>
      <td>0.7859</td>
      <td>0.7497</td>
      <td>0.7989</td>
      <td>0.7735</td>
      <td>0.7713</td>
      <td>0.8106</td>
      <td>0.7904</td>
   </tr>
   <tr>
      <td>绝对减值</td>
      <td>0.8825</td>
      <td>0.8513</td>
      <td>0.8666</td>
      <td>0.8941</td>
      <td>0.8921</td>
      <td>0.8931</td>
      <td>0.8580</td>
      <td>0.8718</td>
      <td>0.8648</td>
   </tr>
   <tr>
      <td>Kneser-Ney</td>
      <td>0.8946</td>
      <td>0.8562</td>
      <td>0.8750</td>
      <td>0.9105</td>
      <td>0.8994</td>
      <td>0.9049</td>
      <td>0.8793</td>
      <td>0.8832</td>
      <td>0.8812</td>
   </tr>
   <tr>
      <td colspan="2">1-gram+HMM</td>
      <td>0.9047</td>
      <td>0.8683</td>
      <td>0.8861</td>
      <td>0.9116</td>
      <td>0.8995</td>
      <td>0.9055</td>
      <td>0.8874</td>
      <td>0.8916</td>
      <td>0.8895</td>
   </tr>

</table>
</escape>

从以上结果可以看出：
 - 使用2-gram语言模型时，平滑方法对分词效果有非常大的影响。
 - 可能是训练语料较少的缘故，1-gram方法在这几个数据集上的效果优于2-gram方法。
