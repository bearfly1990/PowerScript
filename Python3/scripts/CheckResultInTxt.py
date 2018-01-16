import glob

list_of_files = glob.glob('./*.log')
FO = open('Result_PY.txt', 'a') 
FO.write("")
FO.close()
for file_name in list_of_files:
    results = open(file_name).read().splitlines()
    FO = open('Result_PY.txt', 'a') 
    FO.write(results[0] + " - " + file_name + "\n")
    FO.close()
