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

def delete_front(line):
	if(line[1] == '\t'):
		return line[2:]

fp = open(sys.argv[1], encoding='utf-8')
linelist = []
for i, line in enumerate(fp):
    if i < int(sys.argv[2]):
    	linelist.append(line)
    else:
        break
fp.close()

# for i in range(0, int(sys.argv[2])):
# 	print(linelist[i])

quotes = []
time = []
page = []
links = []

is_new_element = False
temp_elem = []
quotes_elem = []
links_elem = []
elem = []
l_st = False

for line in linelist:
	if('Q' in line):
		quotes.append(line)
		quotes_elem.append(quotes[len(quotes)-1])
		q_st = True
	elif('T' in line):
		time.append(line)
		temp_elem.append(time[len(time)-1])
	elif('P' in line):
		if(l_st):
			temp_elem.append(links_elem)
			links_elem = []
			l_st = False

		# page.append(extract_domain(extract_link(line, 'P')))
		page.append(delete_front(line))
		elem.append(temp_elem)
		temp_elem = []
		temp_elem.append(page[len(page)-1])
	elif('L' in line):
		if(q_st):
			temp_elem.append(quotes_elem)
			quotes_elem = []
			q_st = False

		# links.append(extract_domain(extract_link(line, 'L')))
		links.append(delete_front(line))
		links_elem.append(links[len(links)-1])
		l_st = True

elem = elem[1:]
print('Element 1: ' + str(elem[0]))
print(' ')
print('Element 2: ' + str(elem[1]))
print(' ')
print('Element 3: ' + str(elem[2]))
print(' ')

# print('Page : ' + str(page))
# print(' ')
# print('Time : ' + str(time))
# print(' ')
# print('Quotes : ' + str(quotes))
# print(' ')
# print('Links : ' + str(links))

# print(len(quotes))
# print(' ')
# print(len(set(quotes)))
# print(' ')

# print(page)
# print(' ')
# print(links)
# print(' ')
# print(set(links))
# print(' ')
# print(set(page))
# print(' ')

print(len(links) > len(set(links)))
print(' ')
print(len(page) >len(set(links)))
print(' ')
print(set(links).intersection(set(page)))
print(' ')
