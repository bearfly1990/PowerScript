with open("in.txt") as f:
    content = f.readlines()
    
content = [x.strip().lower() for x in content]
content = [x for x in content if x]
content.sort()

outfile = open('out.txt', 'w')

for item in content:
    outfile.write("%s\n" % item)

    