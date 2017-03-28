import os


def _create_settings_file(systems_dir_path, gold_standard_path):
    import os
    models_dir_path = gold_standard_path

    settings_file = open('settings.xml', 'w')
    settings_file.write('<ROUGE_EVAL version=\"1.5.5\">\n')

    for filename in os.listdir(systems_dir_path):
        settings_file.write('<EVAL ID=\"TASK_' + filename.split("_")[0] + '\">\n')
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
    settings_file.write('</ROUGE_EVAL>')
    settings_file.close()


def _run_rouge_script(script_path, data_path):
    import subprocess

    perl_script = subprocess.Popen(
        ["perl", script_path, "-e " + data_path, "-a", "-n 4", "-u", "-m",
         "settings.xml"], stdout=subprocess.PIPE)
    return perl_script.communicate()[0]


def _post_processing(message, results_file, path=None):
    # os.remove('settings.xml')
    message_lines = message.split("\n")
    r1 = message_lines[1]
    r2 = message_lines[5]
    r3 = message_lines[9]
    r4 = message_lines[13]
    rl = message_lines[17]

    r1_value = float(r1.split(" ")[3])
    r2_value = float(r2.split(" ")[3])
    r3_value = float(r3.split(" ")[3])
    r4_value = float(r4.split(" ")[3])
    rl_value = float(rl.split(" ")[3])
    r_mean = (r1_value + r2_value + r3_value + r4_value + rl_value) / float(5);

    if path is not None:
        config_name = path.split('/')[-1]
        results_file.write(config_name + '\n')

    results_file.write(r1)
    results_file.write(r2)
    results_file.write(r3)
    results_file.write(r4)
    results_file.write(rl)
    results_file.write("mean: " + str(r_mean) + '\n\n')


def compute_for_grid_search(
        tfidf_values,                       # range of tfidf you want to check
        redundancy_values,                  # redundancy values you want to check
        results_path,                       # tell me where store your results
        script_path,                        # tell me where is your rouge script
        data_path,                          # tell me where is your data (same dir of rouge script, generally)
        summary_destination_path,           # tell me where are stored your system-generated summaries
        gold_standard_path):                # tell me where are your gold standards

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


def compute(
        results_path,                       # tell me where store your results
        script_path,                        # tell me where is your rouge script
        data_path,                          # tell me where is your data (same dir of rouge script, generally)
        system_summary_path,                # tell me where are stored your system-generated summaries
        gold_standard_path):

    """import summary_generator
    target_length_path = 'C:/prove-disperate/length.txt'
    lmap = summary_generator.read_len(target_length_path)"""

    results = open(results_path, 'w')
    _create_settings_file(system_summary_path, gold_standard_path)
    msg = _run_rouge_script(script_path, data_path)
    _post_processing(msg, results, system_summary_path)
