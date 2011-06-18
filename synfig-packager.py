#!python

import sys, os, shutil

global parslist

parslist=[]
filelist=[]
parslist2=[]

def sifparse(filename):
	#print "Parsing file %s..." % (filename)
	sifdir=filename[:filename.find(os.path.basename(filename))]
	file=open(filename)
	parslist.append(filename)
	massiv=file.readlines()
	for i, line in enumerate(massiv):
		if line.find('<param name="filename">')<>-1:
			str=massiv[i+1]
			pos1=str.find('<string>')+len('<string>')
			pos2=str.find('</string>')
			fname=str[pos1:pos2]
			#print "       Join input:",sifdir,fn 
			fn=os.path.join(sifdir ,fname)
			fn=os.path.abspath(fn)
			if not fn in filelist:
				print fn
				fname=os.path.basename(fname)
				co=a1+'/'+fname
				shutil.copy(fn, co)
			filelist.append(fn)
		if line.find('<param name="canvas" use=')<>-1:
			pos1=line.find('<param name="canvas" use="')+len('<param name="canvas" use="')
			pos2=line.find('#"/>')
			fname=line[pos1:pos2]
			fn=os.path.abspath(fname)
			print fn
			if not fn in parslist:
				fname=os.path.basename(fname)
				co=a1+'/'+fname
				shutil.copy(fn, co)
				filedit(co)
				sifparse(fn)

def filedit(cname):
	file2=open(cname)
	parslist2.append(cname)
	massiv2=file2.readlines()
	for j, line2 in file2.readline():
		if line2.find('<param name="filename">')<>-1:
			str2=massiv2[j+1]
			pos1=str2.find('<string>')+len('<string>')
			pos2=str2.find('</string>')
			fname2=str2[pos1:pos2] 
			fname2=os.path.basename(fname2)
			massiv2[j+1]='<string>'+fname2+'</string>'
		if line2.find('<param name="canvas" use=')<>-1:
			pos1=line2.find('<param name="canvas" use="')+len('<param name="canvas" use="')
			pos2=line2.find('#"/>')
			fname2=line2[pos1:pos2]
			fname2=os.path.basename(fname2)
			file2.write='<param name="canvas" use='+fname2+'#"/>'
			file2.close()
			if not fname2 in parslist2:
				filedit(fname2)
	file2.close()

a=sys.argv[1]
a1=a[:a.find('.sif')]
os.mkdir(a1)
co=a1+'/'+a
shutil.copy(a, co)
filedit(co)
sifparse(a)
