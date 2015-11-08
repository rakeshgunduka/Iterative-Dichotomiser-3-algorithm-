from __future__ import division
from math import log
import operator
import csv
import copy
from sys import argv
script,file_name = argv

reader = csv.reader(open(file_name))
d = []
for row in reader:
	d.append(row)
#GLOBALS
tl = []
t_titles = d[0]
cls = {}
classes = {}
n = len(d)-1
ctitle = t_titles[len(d[0])-1]
init = 1
tree = {}
trap = 0

def init_classes(dset):
	global n,trap
	cls = {}
	dataset = copy.copy(dset)
	title = dataset[0]
	del dataset[0]
	for p in title:
		index = title.index(p)
		ii = title.index(ctitle)
		cld = {}
		cnt = {}
		cl = []
		count = []
		countYN = []
		m = 0
		for lists in dataset:
			ts = lists[index]
			if ts not in cl:
				cl.append(ts)
				i = cl.index(ts)
				if lists[ii] in ['yes','Yes','YES']:
					countYN.append([1,0])
				elif lists[ii] in ['no','No','NO']:
					countYN.append([0,1])
				count.append(1)
				i = cl.index(ts)	
			else:
				for val in cl:
					ind = cl.index(val)
					if ts == val:
						count[ind] += 1
						if lists[ii] in ['yes','Yes','YES']:
							countYN[ind][0] += 1
						elif lists[ii] in ['no','No','NO']:
							countYN[ind][1] += 1
					
			q = cl.index(ts)	
			m += 1 
	 	for x in range(len(cl)):
			cnt[count[x]]  = countYN[x]
			tcls = cl[x]
			cld[tcls] = cnt[count[x]]
		cls[p] = cld
		if n < m:
			n = m
	return cls

def project_columns(title1,title2,dset):
	dataset = copy.copy(dset)
	title = dataset[0]
	t1_index = t_titles.index(title1)
	t2_index = t_titles.index(title2)
	nd = []
	rw = []
	rw.append(title1)
	rw.append(title2)
	nd.append(rw)
	for rows in dataset:
		rw = []
		d1 = rows[t1_index]
		rw.append(d1)
		d2 = rows[t2_index]
		rw.append(d2)
		nd.append(rw)
	return nd

def select_rows(title,attribute,dset):
	dataset = copy.copy(dset)
	del dataset[0]
	t_index = t_titles.index(title)
	nd = []
	nd.append(dset[0])
	for rows in dataset:
		if rows[t_index] == attribute:
			nd.append(rows)
	return nd	


def initial_entropy(dt,dset):
	global init
	e = 0
	dataset = copy.copy(dset)
	classes = init_classes(dataset)
	del dataset[0]
	n = len(dataset)
	for data in classes[dt]:
		num = (classes[dt][data])[0]+(classes[dt][data])[1]	
		p = num/n
		e = e + entropy(classes[dt][data])	
	init = 0
	return e

def entropy(st):
	global init
	tn = st[0] + st[1]
	e = 0
	if init == 0:
		if 0 in st:
			e = 0
		else:	
			for num in st:
				p = num/tn
				e = e + ((-p*log(p))/(log(2)))
	else:
		p = tn/n
		e = (-p*log(p))/(log(2))
	return e	 

def infogain_for(dset):	
	sum = 0
	n = len(dset)-1
	cls = init_classes(dset)
	e = 0
	for data in cls:
		if data != ctitle:
			for xdata in cls[data]:
				m = cls[data][xdata][0] + cls[data][xdata][1]
				p = m/n
				e = e + p*entropy(cls[data][xdata])
	return eS-e

def getroot(dset,node):
	global eS
	dataset = copy.copy(dset)
	cls = init_classes(dataset)
	del dataset[0]
	n = len(dataset)
	ig = {}
	check_list = dset[0]
	print check_list
	eS = initial_entropy(ctitle,dset)
	for dt in check_list:
		if dt !=  node:
			ptable = project_columns(dt,ctitle,dataset)
			#print "for",dt
			#printtable(ptable)
			ig[dt] = infogain_for(ptable)
	ig = sorted(ig.items(),key = operator.itemgetter(1),reverse = True)
	print ig
	return ig[0][0]

def prediction_for(node,table):
	cls = init_classes(table)
	print cls
	ls = {}
	for xdata in cls:
		if xdata != ctitle:
			for ydata in cls[xdata]:
				if 0 not in cls[xdata][ydata]:
					mx = max(cls[xdata][ydata])
					if cls[xdata][ydata].index(mx) == 0:
						return "YES"
					else:
						return "NO"

def getnode(node,path,dset,branches):
	global trap
	dataset = copy.copy(dset)
	cls = init_classes(dataset)
	del dataset[0]
	n = len(dataset)
	ig = {}
	check_list	 = dset[0]
	if 0 in cls[node][path]:
		ls = 0
		for i in range(len(cls[node][path])):
			if cls[node][path][i] == 0:
				ls = "YES"
			else:
				ls = "NO"				
	else:
		ls = {}
		if trap == 3:
			printtable(dataset)
		if trap == 2:
			printtable(dataset)
		for dt in check_list:
			if dt !=  node and dt != ctitle and dt not in branches:
				ptable = project_columns(dt,ctitle,dataset)
				printtable(ptable)
				ig[dt] = infogain_for(ptable)
		ig = sorted(ig.items(),key = operator.itemgetter(1),reverse = True)
		print ig
		if len(ig) == 2:
			printtable(ptable)
			if ig[0][1] == ig[0][1]:
				#for ambiguous situation
				val = prediction_for(ptable[0][0],ptable)
				return val
		ils = {}
		for f_paths in cls[ig[0][0]]:
			branches.append(ig[0][0])
			ils[f_paths] = getnode(ig[0][0],f_paths,dset,branches)
		ls[ig[0][0]] = ils
	return ls

def printtable(table):
	for row in table:
		print row
	print

def developtree(node,cls,dset):
	global trap
	branches = []
	tls = {}
	for paths in cls[node]:
		ls = {}
		tdataset = select_rows(node,paths,dset)
		branches.append(node)
		tls[paths] = getnode(node,paths,tdataset,branches)
	return tls

def printtree(tree,depth):
	for xdata in tree:
		print "\t"*depth,xdata
		if type(tree[xdata]) is str:
			depth += 1
			depth -= 1
		elif type(tree[xdata]) is dict:
			depth += 1		
			printtree(tree[xdata],depth)
			depth -= 1
			
def inittree(dset):
	global eS
	classes = init_classes(dset)
	i = t_titles.index(ctitle)
	root = getroot(dset,ctitle)
	print "Root is",root
	tree[root] = developtree(root,classes,dset)
	printtree(tree,0)

if __name__ == "__main__":
	classes = init_classes(d)
	tree = inittree(d)
