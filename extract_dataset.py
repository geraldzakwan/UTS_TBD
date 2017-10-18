import sys

def extract_link(line, delimiter):
	ret = ""
	for huruf in line:
		if(huruf != delimiter and huruf != ' ' and huruf != '\t' and huruf != '\n'):
			ret += huruf
	return ret

def extract_domain(line):
	first_slash = line.index('/')
	i = first_slash + 2

	while (i < len(line)):
		if(line[i] == '/'):
			break
		i = i + 1
			
	return line[:i]

fp = open("../" + sys.argv[1])
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
		page.append(extract_domain(extract_link(line, 'P')))
	elif('L' in line):
		# link.append(extract_domain(extract_link(line, 'L')))
		link.append(extract_domain(extract_link(line, 'L')))

# print(page)
# print()
# print(link)
# print(len(link) == len(set(link)))
# print(set(link))
# print(set(page))
print(set(link).intersection(set(page)))