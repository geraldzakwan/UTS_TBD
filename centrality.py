from __future__ import division
import snap
import sys
import os
import Queue as Q
import csv

def extract_domain(line):
	domain_raw = line.split('\t')[1]
	temp = domain_raw.split('/')
	domain_net = temp[2]
	domain_net = domain_net.replace('\n', '')
	return domain_net


domain_mapping = []
g1 = snap.TNGraph.New()
isload = None

# want to load ?
files_in_directory = os.listdir('./')
if("memetracker1.graph" in files_in_directory and "domain_mapping.txt" in files_in_directory):
	load_choice = raw_input("Graph data found, want to load it instead(Y/N)? ")
	if(load_choice.lower() == 'y'):
		isload = True
		# load graph model
		FIn = snap.TFIn("memetracker1.graph")
		g1 = snap.TNGraph.Load(FIn)

		# load mapping
		with open("domain_mapping.txt") as infile:
			for line in infile:
				domain_mapping.append(line.replace('\n', ''))
		print "graph and mapping has been loaded succesfully! "
	else :
		isload = False
else:
	isload = False

# make graph from source
if(not isload):
	filename = '../' + sys.argv[1]
	counter = int(sys.argv[2])
	last_domain = -1

	with open(filename) as infile:
		for line in infile:
			if('P' in line):
				counter -= 1
				domain_name = extract_domain(line)
				nodeid = -1
				if domain_name in domain_mapping:
					nodeid = domain_mapping.index(domain_name)
				else:
					domain_mapping.append(domain_name)
					nodeid = len(domain_mapping) - 1
					g1.AddNode(nodeid)
				last_domain = nodeid

			elif('L' in line):
				domain_name = extract_domain(line)
				node_link_id = -1
				if domain_name in domain_mapping:
					node_link_id = domain_mapping.index(domain_name)
				else:
					domain_mapping.append(domain_name)
					node_link_id = len(domain_mapping) - 1
					g1.AddNode(node_link_id)

				#print "add edge from %d to %d" % (last_domain, node_link_id)
				if(last_domain != node_link_id):
					g1.AddEdge(last_domain, node_link_id)

			if (counter == 0):
				break

	print "Graph built successfully (%d nodes, %d edges)!" % (g1.GetNodes(), g1.GetEdges())
	#choice = raw_input("Save the graph for future use (Y/N)? ")
	choice = 'y'
	if choice.lower() == 'y':
		# save the graph model
		FOut = snap.TFOut("memetracker1.graph")
		g1.Save(FOut)
		FOut.Flush()

		# save the domain mapping
		fout = open('domain_mapping.txt', 'w')
		for i in range(len(domain_mapping)-1):
			fout.write(domain_mapping[i] + '\n')
		fout.write(domain_mapping[len(domain_mapping)-1])
		fout.close

		print "Graph model and mapping has been saved !"

if not os.path.exists('./centrality_result'):
	os.makedirs('./centrality_result')

print "domain mapping length = %d" % (len(domain_mapping))
print "nodes = %d" % (g1.GetNodes())
# calculating node centrality and save it as csv
with open('./centrality_result/deg_centrality.csv', 'wb') as csvfile:
	q = Q.PriorityQueue()
	for NI in g1.Nodes():
		#print "id = %d" % (NI.GetId())
		q.put((-NI.GetInDeg(), domain_mapping[NI.GetId()]))
	
	writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
	while not q.empty():
		tup = q.get()
		newtup = (tup[0] * -100) / (g1.GetEdges()-1), tup[1]
		writer.writerow(newtup)

print "node centrality saved successfully !"

print "Plotting the graph...."
snap.DrawGViz(g1, snap.gvlDot, "g1.png", "g1", False)