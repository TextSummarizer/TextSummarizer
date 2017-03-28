"""import rouge

results_path = 'bugfix_results.txt'
script_path = 'C:/Users/Peppo/Desktop/w2vm/rouge4MultiLing/rouge/ROUGE-1.5.5.pl'
data_path = 'C:/Users/Peppo/Desktop/w2vm/rouge4MultiLing/rouge/data'
gold_standard_path = 'C:/evaluation/summaries_300_500_eval/'
system_summary_path = 'C:/evaluation/095/summaries_300_bugfix/'

print 'Grid search on summaryes with ROUGE metrics: STARTED!'
rouge.compute(results_path=results_path,
              script_path=script_path,
              data_path=data_path,
              system_summary_path=system_summary_path,
              gold_standard_path=gold_standard_path)
print "Everything done. Now go to your result path and see results. Bye!"
"""


"""
import rouge_single

results_path = 'speranza.txt'
script_path = 'C:/Users/Peppo/Desktop/rouge-eval-copia/ROUGE-1.5.7.pl'
data_path = 'C:/Users/Peppo/Desktop/rouge-eval-copia/data'
gold_standard_path = 'C:/Users/Peppo/Desktop/rouge-eval/models/'
system_summary_path = 'C:/Users/Peppo/Desktop/rouge-eval/systems/'

print 'Grid search on summaryes with ROUGE metrics: STARTED!'
rouge_single.compute(
    results_path=results_path,
    script_path=script_path,
    data_path=data_path,
    system_summary_path=system_summary_path,
    gold_standard_path=gold_standard_path)
print "Everything done. Now go to your result path and see results. Bye!"
"""