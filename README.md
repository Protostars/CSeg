# CSeg
## �򵥵Ļ��ڻ�Ϸ��������ķִ���

����������jiebaһ�£�
 - ʹ�ôʵ�Ծ��ӽ��г������з֣��ҳ����дʵ��з�λ�ã�����һ��DAG��
 - ʹ�ö�̬�滮��������DAG���ҵ�1-gram����ֵ�����з�·����
 - ����ڻ��ֹ����г����˶�����ַ��з֣�ʹ�����ֹ��ʵ�HMM��������ַ������ٴ��з֣�����������߷���δ��¼�ʵ�������

�������ﻹ����������������
 - ������������з�·��ʱ������2-gram����ģ�͡�
 - �Ƚ�2-gram�в�ͬ��ƽ����ʽ��+1ƽ�������Լ�ֵƽ����Kneser-Neyƽ���Էִ�Ч����Ӱ�졣

CSegĿ¼�µ��ļ����£�
```
CSeg
�� corpus_process.py # ���ϴ���������ɴʵ䣬2-gramͳ����Ϣ��HMM���ʹ�����Ϣ
�� cseg.py # �ִ���������
�� eval.py # ��֤���򣬿ɼ���ִʵ�׼ȷ�ʡ��ٻ��ʺ�F1��ͬʱ���ҳ����л��ִ���Ĵ�
�� hmm.py # ����hmmģ�͵ĸ����ִʳ������ڽ�һ���з�
�� test.py # ���Գ���
��
����corpus # ����Ŀ¼������SIGHAN2005�е�pkr��msr���ݼ���NLPCC2016��΢�����ݼ�
�� msr_test.utf8 # test: ��������
�� msr_test_gold.utf8 # glod���ִʲο���
�� msr_training.utf8 # train: ѵ������
�� nlpcc2016-word-seg-train.dat
�� nlpcc2016-wordseg-dev.dat
�� nlpcc2016-wordseg-dev_gold.dat
�� pku_test.utf8
�� pku_test_gold.utf8
�� pku_training.utf8
��
����data # CSegʹ�õĴ������������ݣ�����2-gramͳ����Ϣ���ʵ��hmm���ʹ�����Ϣ
�� bi_gram.txt
�� dict.txt
�� hmm_prob
��
����output # �������Ŀ¼
```
Ĭ��dataĿ¼�µ�������ʹ��corpus_process������MSR���Ϻ�Ľ������ʹ��corpus_process.py�����������ϣ��ִ�������λ��cseg.py�У�test.py�ǲ��Գ���

���Խ��

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
      <td>���Լ�ֵ</td>
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
      <td>���Լ�ֵ</td>
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

�����Ͻ�����Կ�����
 - ʹ��2-gram����ģ��ʱ��ƽ�������Էִ�Ч���зǳ����Ӱ�졣
 - ������ѵ�����Ͻ��ٵ�Ե�ʣ�1-gram�������⼸�����ݼ��ϵ�Ч������2-gram������
