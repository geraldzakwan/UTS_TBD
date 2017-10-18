import sys

def extract_link(line, delimiter):
	ret = ""
	for huruf in line:
		if(huruf != delimiter and huruf != ' ' and huruf != '\t' and huruf != '\n'):
			ret += huruf
	return ret

def extract_domain(line):
	

fp = open(sys.argv[1])
linelist = []
for i, line in enumerate(fp):
    if i < int(sys.argv[2]):	
    	linelist.append(line)
    else:
        break
fp.close()

queue = []
topics = []
page = []
link = []
for line in linelist:
	if('Q' in line):
		queue.append(line)
	elif('T' in line):
		topics.append(line)
	elif('P' in line):
		page.append(extract_link(line, 'P'))
	elif('L' in line):
		link.append(line)

print(len(link) == len(set(link)))
# print(set(link))
# print(set(page))
# print(set(link).intersection(set(page)))