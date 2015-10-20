from __future__ import division
from math import log
import operator
import csv
from sys import argv
script,file_name = argv

reader = csv.reader(open(file_name))
d = []
for row in reader:
	d.append(row)
'''
d = [['Outlook','Temperature','Humidity','Wind','PlayTennis'],\
	 ['Sunny'	,'Hot'	,'High'		,'Weak'		,'No'],\
	 ['Sunny'	,'Hot'	,'High'		,'Strong'	,'No'],\
	 ['Overcast','Hot'	,'High'		,'Weak'		,'Yes'],\
	 ['Rain'	,'Mild'	,'High'		,'Weak'		,'Yes'],\
	 ['Rain'	,'Cool'	,'Normal'	,'Weak'		,'Yes'],\
	 ['Rain'	,'Cool'	,'Normal'	,'Strong'	,'No'],\
	 ['Overcast','Cool'	,'Normal'	,'Strong'	,'Yes'],\
	 ['Sunny'	,'Mild'	,'High'		,'Weak'		,'No'],\
	 ['Sunny'	,'Cool'	,'Normal'	,'Weak'		,'Yes'],\
	 ['Rain'	,'Mild'	,'Normal'	,'Weak'		,'Yes'],\
	 ['Sunny'	,'Mild'	,'Normal'	,'Strong'	,'Yes'],\
	 ['Overcast','Mild'	,'High'		,'Strong'	,'Yes'],\
	 ['Overcast','Hot'	,'Normal'	,'Weak'		,'Yes'],\
	 ['Rain'	,'Mild'	,'High'		,'Strong'	,'No']]
'''
tl = []
title = d[0]
del d[0]
classes = {}
n = 0
eS = 0
es = {}
init = 1
ig = {}
tree = {}
dset = []
ltree = [] 


def init_classes(cls,ttl):
	global n,init
	print title
	for p in title:
		index = title.index(p)
		ii = title.index(ttl)
		cld = {}
		cnt = {}
		cl = []
		count = []
		countYN = []
		m = 0
		for lists in d:
			ts = lists[index]
			if ts not in cl:
				#print "first time",ts
				cl.append(ts)
				i = cl.index(ts)
				if init == 0:
					for r in classes[ttl]:
						if lists[ii] == r:
							countYN.append([1,0])
						elif lists[ii] == 'No':
							countYN.append([0,1])	 
					exit(0)
				else:	
					if lists[ii] == 'Yes':
						countYN.append([1,0])
					elif lists[ii] == 'No':
						countYN.append([0,1])
				count.append(1)
				i = cl.index(ts)	
			else:
				#print ts,"already there"
				for val in cl:
					ind = cl.index(val)
					if ts == val:
						count[ind] += 1
						if lists[ii] == 'Yes':
							countYN[ind][0] += 1
						elif lists[ii] == 'No':
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

def entropy(ttl,dc):
	lt = classes[ttl][dc]
	if ttl is not "PlayTennis":
		n = lt[0]+lt[1]
	else:
		n = 14	
	e = 0
	if 0 in lt and ttl is not "PlayTennis":
		return 0
	else:	
		for data in lt:
			num = data
			if num is not 0:
				p = (num/n)
				et = -((p*log(p))/(log(2)))
				e = e + et
	return e

def entr(num):
	p = num
	return p

def find_entropy(ttl):
	e = 0
	for dc in classes[ttl]:
		et = entropy(ttl,dc)
		e = e + et
	print e
	return e

def informationgain(ttl):
	e = 0
	for dc in classes[ttl]:
		num = (classes[ttl][dc])[0]+(classes[ttl][dc])[1]	
		p = num/n
		et = entropy(ttl,dc)
		es[ttl] = et
		e = e + p*et
	return eS - e

def countof(node,chr1,ttl,chr2):
	n = title.index(node)
	m = title.index(ttl)
	count = 0
	for lists in d:
		if chr1 == lists[n]:
			if chr2 == lists[m]:
				count += 1
	return count

def dataset(node,char,ttl):
	p = title.index(node)
	q = title.index(ttl)
	r = title.index('PlayTennis')
	lt = []
	ls = []
	for data in d:
		lt = lt[0:0]
		if data[p] == char:
			lt.append(data[p])
			lt.append(data[q])
			lt.append(data[r])
			ls.append(lt)
	return ls

def entropyfor(num,n):
	p = num/n
	et = -(p*log(p))/(log(2))
	return et

def infogain(node,char,ttl):
	global dset
	dset = dataset(node,char,ttl)
	e = 0
	n = len(dset)
	cn = []
	count = []
	for r in classes[ttl]:
		cn.append(r)
		count.append([0,0])
	for dt in dset:
		if dt[0] == char:
			for r in cn:
				i = cn.index(r)
				if dt[1] == r:
					if dt[2] == 'Yes':
						count[i][0] += 1
					else:
						count[i][1] += 1
	eo = 0
	val = {}
	for ct in count:
		get = count.index(ct)
		m = ct[0]+ct[1]
		p = m/n
		if 0 not in ct:
			for tv in ct:
				et = entropyfor(tv,m)
				e = e + p*et
	return es[node]-e

def getnodes(node,cd,cn):
	global ig
	for g in ig:
		for gn in g:
			if gn == node:
				index = g.index(gn)
	eg = {}
	lst = {}
	for c in range(cn):
		i = index+c+1
		cl = ig[i][0]
		t = infogain(node,cd,cl)	
		if bool(lst) is False:
			lst[cl] = t
		elif not all(i>=t for i in list(lst.values())):	
			lst.clear()
			lst[cl] = t
		if lst[cl] == es[node]:
			cn = []
			count = []
			for r in classes[cl]:
				cn.append(r)
				count.append([0,0])
			for dt in dset:
				if dt[0] == cd:
					for r in cn:
						i = cn.index(r)
						if dt[1] == r:
							if dt[2] == 'Yes':
								count[i][0] += 1
							else:
								count[i][1] += 1
			l = {}
			for i in cn:
				index = cn.index(i)
				if count[index][0] == 0:
					l[i] = "No"
				else:
					l[i] = "Yes"
			lst[cl] = l
	return lst
			 
def developtree(node):
	cn = 0
	cnode = []
	for conn in classes[node]:
		nd = classes[node][conn]
		if 0 in nd:
			iid = nd.index(0)
			if iid is 0:
				tree[node][conn] = 'No'
			else:
				tree[node][conn] = 'Yes'	
		else:
			cn += 1
			cnode.append(conn)
			tree[node][conn] = getnodes(node,conn,cn)
	treetolist(tree)
	print ltree		

def printtree():
	for i in tree:
		print i
		for j in tree[i]:
			print "\t",j
			if type(tree[i][j]) is str:
				print "\t\t",tree[i][j]
			else:
				for k in tree[i][j]:
					print "\t\t",k
					if type(tree[i][j][k]) is dict: 
						for l in tree[i][j][k]:
							print "\t\t\t",l
							print "\t\t\t\t",tree[i][j][k][l]

def treetolist(d):
	for v in d:
		if type(d[v]) is dict:
			print v
			ltree.append(v)
			treetolist(d[v])
		else:
			print v
			ltree.append(v)
			ltree.append(d[v])

def enternewdataset():
	ds = []
	for i in range(len(title)):
		if title[i] != "PlayTennis":
			data = raw_input(title[i]+" : ")
			if title[i] in ltree:
				ds.append(title[i])
				ds.append(data)
	return ds

def getchild(ds):
	print ds
	return [ds].keys()[0]

def checkfor(data,tree):
	if data in tree:
		if type(tree[data]) is dict:
			d = checkfor(tree[data].iterkeys().next(),tree[data])
			return d
		else:
			return 1	

if __name__ == "__main__":
	classes = init_classes(classes,'PlayTennis')
	init = 0
	print "Iterative Dichotomiser 3 algorithm"
	print classes
	print "Length of dataset",n
	eS = find_entropy('PlayTennis')
	print "Entropy for PlayTennis:",eS
	for tt in classes:
		if tt != 'PlayTennis':
			ig[tt] = informationgain(tt)
	ig = sorted(ig.items(),key = operator.itemgetter(1),reverse = True)
	print "\nEntropy values :\n",ig
	print "\nRoot is :",ig[0][0]
	root = ig[0][0]
	tree[root] = {}
	developtree(root)
	print "\nOutput:\nThe Decision Learning Tree: \n",tree,"\n"
	printtree()
	n = int(raw_input("Enter Choice\n1: Enter new Dataset\n2. Exit \n"))							
	if n == 1:
		ds = enternewdataset()
		tmp_ds = []
		val = checkfor(ds[0],tree)
		if val is 0:
			print "Tennis cannot be played"
			tmp_ds.append('No')
		elif val is 1:
			print "Tennis can be played"
			tmp_ds.append('Yes')
		d.append(tmp_ds)	
	`elif n == 0:
		exit(0)		
