import glob
import os
import json

FILE_PATTERN = '*.txt'

list_of_files = glob.glob(FILE_PATTERN,recursive=True)

for file_name in list_of_files:
    if(os.path.isdir(file_name) or __file__ == file_name or not os.path.isfile(file_name)):
        continue
        
    print("start to generate %s." % file_name)
    
    with open(file_name, "r") as fin:
        old_lines = fin.readlines()
        new_lines = []
        for old_line in old_lines:
            json_obj = json.loads(old_line)
            
            old_value = json_obj["msgbody"]["SECID"]["SecurityIDValue"]
            
            json_obj["msgbody"]["SECID"]["SecurityIDValue"] = old_value + "X"
            
            new_value = json_obj["msgbody"]["SECID"]["SecurityIDValue"]
            
            # print(old_value + " ==> " + new_value)
            json_str = json.dumps(json_obj)
            
            new_lines.append(json_str)
            
    with open(file_name+".new.txt", "w") as fout:
        fout.writelines("\n".join(new_lines))
    print("ended to generate %s." % file_name)
