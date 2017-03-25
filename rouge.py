import os


def _create_settings_file(systems_dir_path, gold_standard_path):
    import os
    models_dir_path = gold_standard_path

    settings_file = open('settings.xml', 'w')
    settings_file.write('<ROUGE_EVAL version=\"1.5.5\">\n')

    task_counter = 0
    for filename in os.listdir(systems_dir_path):
        settings_file.write('<EVAL ID=\"TASK_' + str(task_counter) + '\">\n')
        settings_file.write('<MODEL-ROOT>' + models_dir_path + '</MODEL-ROOT>\n')
        settings_file.write('<PEER-ROOT>' + systems_dir_path + '</PEER-ROOT>\n')
        settings_file.write('<INPUT-FORMAT TYPE=\"SPL\"></INPUT-FORMAT>\n')
        settings_file.write('<PEERS>\n')
        settings_file.write('<P ID=\"0\">' + filename + '</P>\n')
        settings_file.write('</PEERS>\n')
        settings_file.write('<MODELS>\n')
        summary_filename = filename.split("_")[0] + "_summary.txt"
        settings_file.write('<M ID=\"0\">' + summary_filename + '</M>\n')
        settings_file.write('</MODELS>\n')
        settings_file.write('</EVAL>\n')
        task_counter += 1
    settings_file.write('</ROUGE_EVAL>')
    settings_file.close()


def _run_rouge_script(script_path, data_path):
    import subprocess

    perl_script = subprocess.Popen(
        ["perl", script_path, "-e " + data_path, "-f A", "-a", "-s", "-n 4",
         "settings.xml"], stdout=subprocess.PIPE)
    return perl_script.communicate()[0]


def _post_processing(message, results_file, path):
    os.remove('settings.xml')
    message_lines = message.split("\n")
    r1 = message_lines[1]
    r2 = message_lines[5]
    r3 = message_lines[9]
    r4 = message_lines[13]
    rl = message_lines[17]

    config_name = path.split('/')[-1]

    results_file.write(config_name + '\n')
    results_file.write(r1)
    results_file.write(r2)
    results_file.write(r3)
    results_file.write(r4)
    results_file.write(rl + '\n')


def compute(tfidf_values,                   # range of tfidf you want to check
            redundancy_values,              # redundancy values you want to check
            results_path,                   # tell me where store your results
            script_path,                    # tell me where is your rouge script
            data_path,                      # tell me where is your data (same dir of rouge script, generally)
            summary_destination_path,       # tell me where you stored your system-generated summaries
            gold_standard_path):            # tell me where are your gold standards

    results = open(results_path, 'w')
    for tfidf in tfidf_values:
        print 'Computing ROUGE for tfidf ' + str(tfidf) + '...'

        for redundancy in redundancy_values:
            tfidf_str = "".join(str(tfidf).split("."))
            redundancy_str = "".join(str(redundancy).split("."))
            new_systems_dir_path = summary_destination_path + 'tfidf_' + str(tfidf_str) + "_redundancy_" + str(redundancy_str)

            _create_settings_file(new_systems_dir_path, gold_standard_path)
            msg = _run_rouge_script(script_path, data_path)
            _post_processing(msg, results, new_systems_dir_path)

    results.close()
    print 'Rouge: done!'
