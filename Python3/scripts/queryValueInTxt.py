import sys
import re

inFile  = "in.txt"#sys.argv[1]
outFile = "out.txt"#sys.argv[2] 
print(inFile + " -- " + outFile)
with open(inFile) as f:
    content1 = f.readlines()
# Get out key ~ value approximately
content1 = [x[11:21].strip() + "~"+ x[81:96] for x in content1 if x[11:21].strip()] 
# Remove empty key string
content1 = [x for x in content1 if not (' ' in x.split("~")[0])]
# Remove special key string with _____ or -------
content1 = [re.sub('[\s+]', '',x) for x in content1 if not re.search('[_*-*]', x)]
# Remove value string witch is not number
content1 = [re.sub('[\s+]', '',x) for x in content1 if not re.search('[a-zA-Z_*-*]', x.split("~")[1])]
# Remove empty value string
content1 = [x for x in content1 if x.split("~")[1]]
# Split key and value with \t instead of ~
content1 = [x.replace("~", "\t") for x in content1]

thefile = open(outFile, 'w')
for item in content1:
  thefile.write("%s \n" % item)

