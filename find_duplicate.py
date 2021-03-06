'''
find duplicate files on a specific directory
TO DO: 
	- check file size first		OK
	- sort file size		OK	
	- check files that have the same size 	OK
	- calculate MD5			
	- finally check file content with regard to bytes		
'''

import os, sys, stat
import hashlib
import math
from functools import partial 
from collections import defaultdict


def find_dupplicate(root):
	# get summary information about all files
	summary = "summary.txt"	
	list_files(root, summary)	
	
	# sort according to size
	summarysorted = "summary_sorted.txt"
	sort_size(summary,summarysorted)
	
	# scan the sorted file, group files with respect to their sizes
	res = []
	refsize = 0
	fnlist = []
	for line in open(summarysorted):
		token = line.split() # must be sure each line has two tokens
		size = int(token[0])
		if size > refsize :	# 
			# do md5 comparing on this set 
			md5_dup_list = detect_md5_dup(fnlist)
			for g in md5_dup_list:
				res.append(g)
			del fnlist[:]
			refsize = size
		
		filename = line[len(token[0]):].strip()
		fnlist.append(filename)
	return res

# Given a list of file names, export names of the files that have the same md5s
def detect_md5_dup(fnlist):
  d = {}
  v = map(calc_md5, fnlist)
  for i in range(len(v)):
    d.setdefault(v[i],[]).append(fnlist[i])
  return filter(lambda x:len(x)>1, d.values())
	
# Calculate MD5 of each file, based on its filename	
def calc_md5(filename):
	if os.path.isfile(filename) == False:
	 	return 0
	res = ''
	with open(filename, mode = 'rb') as f:
		d = hashlib.md5()
		for buf in iter(partial(f.read, 128), b''):
			d.update(buf)
		res = d.hexdigest()
	return res
	
	
# list all the file names in the root folder and store to file 
def list_files(root, outfilename):
	summary = open(outfilename, 'w') 
	for(thisdir, subshere, fileshere) in os.walk(root):
		summary.write('[' + thisdir + ']\n')
		for fname in fileshere:
			path = os.path.join(thisdir,fname)
			if os.path.isfile(path):
				info = os.stat(path);
				filesize = info[stat.ST_SIZE];
				summary.write(str(filesize) + "\t" + path   + "\n");
		
def sort_size(inname, outname):
	# sort according to file size 
	sizedict = {}
	for line in open(inname):
		token = line.split()
		if len(token) >= 2:
			try:
				size = int(token[0]);
				line = line[len(token[0]):]
				fname = line.strip()
				
				if sizedict.get(size) == None:
					sizedict[size] = [fname]
				else:
					sizedict[size].append(fname)
			except ValueError:
				pass

	sizekeys = list(sizedict.keys())
	sizekeys.sort()
	
	#Write result to output file
	out = open(outname, "w")
	for s in sizekeys:
		listfiles = sizedict[s]
		for file in listfiles:
			out.write(str(s) + "\t" + file + "\n")
								
if __name__ == "__main__":
	fn1 = "summary.txt"
	dupp_file_group = 	find_dupplicate (sys.argv[1])
	print("***RESULT***")
	for g in dupp_file_group:
		print("---")
		for fn in g:
			print(fn)
