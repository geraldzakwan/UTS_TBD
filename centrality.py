import snap
import sys
import os

def extract_domain(line):
	domain_raw = line.split('\t')[1]
	temp = domain_raw.split('/')
	domain_net = temp[0] + temp[1] + temp[2]
	domain_net = domain_net.replace('\n', '')
	return domain_net


domain_mapping = []
g1 = snap.TNGraph.New()

files_in_directory = os.listdir('./')
if("memetracker1.graph" in files_in_directory and "domain_mapping.txt" in files_in_directory):
	load_choice = raw_input("Graph data found, want to load it instead(Y/N)? ")
	if(load_choice.lower() == 'y'):
		# load graph model
		FIn = snap.TFIn("memetracker1.graph")
		g1 = snap.TNGraph.Load(FIn)

		# load mapping
		with open("domain_mapping.txt") as infile:
			for line in infile:
				if(len(line) > 1):
					domain_mapping.append(line.replace('\n', ''))
	else :
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

					print "add edge from %d to %d" % (last_domain, node_link_id)
					g1.AddEdge(last_domain, node_link_id)

				if (counter == 0):
					break

		print "Graph built successfully !"
		choice = raw_input("Save the graph for future use (Y/N)? ")
		if choice.lower() == 'y':
			# save the graph model
			FOut = snap.TFOut("memetracker1.graph")
			g1.Save(FOut)
			FOut.Flush()

			# save the domain mapping
			fout = open('domain_mapping.txt', 'w')
			for item in domain_mapping:
				fout.write(item + '\n')
			fout.close()

			print "Graph model and mapping has been saved !"

print "\n======================================"
print "Betweenness Centrality : "
print "======================================\n"
Nodes = snap.TIntFltH()
Edges = snap.TIntPrFltH()
snap.GetBetweennessCentr(g1, Nodes, Edges, 1.0)
print "%-50s %s" % ("Domain Name", "Betweenness Centrality\n")
for node, domain in zip(Nodes, domain_mapping):
	print "%-50s %s" % (domain_mapping[node], Nodes[node])