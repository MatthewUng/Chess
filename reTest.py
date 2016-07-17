import re


pattern = re.compile('([PRBNQK]{1})([a-f]{,1}[1-8]{,1})([a-f]{1}[1-8]{1})')

f = open('input.txt','r')

for line in f:
    m = re.search(pattern, line)
    if m == None:
        print 'fail'
        continue
    print m.group(0), m.group(1), m.group(2), m.group(3) 
    

f.close()
