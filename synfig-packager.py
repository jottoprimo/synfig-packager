#!python

# -*- coding: utf-8 -*-

import sys, os, shutil, re, zipfile, random

global parslist

parslist=[]
unparsed=[]
filelist=[]
zipfiles=[]
#parslist2=[]

def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id,16))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#x([a-zA-Z0-9]+)(;|(?=\s))", _callback, data)

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
a1=os.path.basename(a)	
a1=a1[:a1.find('.sif')]
a1="/tmp/"+a1+'_'+"%d" % (random.randint(1,100))#a[:a.find('.sif')]
if os.path.exists(a1):
	print "error: %s already exists" % (a1)
	sys.exit(1)
else:
	os.mkdir(a1)

unparsed.append(a)
filename=os.path.basename(a)
#co=a1+'/'+dirname
#shutil.copy(a, co)
#flag_filename=False
dname=a[:a.find(filename)]
#fname=dirname
#filedit(co)
#sifparse(a)
while len(unparsed)>0:
	filepath=unparsed.pop()
	print "Parsing file: %s" %(filepath)
	parslist.append(filepath)
	sifdir=filepath[:filepath.find(os.path.basename(filepath))]
	file=open(filepath)
	filename=os.path.basename(filepath)
	co=a1+'/'+filename
	shutil.copy(a, co)
	flag_filename=False
	#fname=a[:a.find(filename)]
	fname=filename
	a1="/tmp/"+os.path.basename(a1)
	print "---",a1+'/'+fname
	file2=open(a1+'/'+fname, 'w')
	massiv=file.readlines()
	for i, line in enumerate(massiv):
		if line.find('<param name="filename">')<>-1:
			flag_filename=True
			file2.write(line)
		elif line.find('</param>')<>-1:
			flag_filename=False
			file2.write(line)
		elif flag_filename and line.find('<string>')<>-1:
			str=massiv[i]
			pos1=str.find('<string>')+len('<string>')
			pos2=str.find('</string>')
			fnamenotsif=str[pos1:pos2]
			#print "       Join input:",sifdir,fn 
			fn=os.path.join(sifdir ,fnamenotsif)
			#print "+++",sifdir,"___",fnamenotsif
			fn=os.path.abspath(fn)
			if fn.find('&#x')<>-1:
				#decoder=fn[fn.find('&#x')+3:fn.find(';')]
				#print decoder
				#decoder = decoder.decode('utf-8')
				#code=int(decoder, 16)
				#decoder=unichr(code)
				#fn=fn.replace(fn[fn.find('&#x'):fn.find(';')], decoder)
				fn=decode_unicode_references(fn)
				fn=fn.encode('utf-8')
			if not fn in filelist:
				print fn
				fnamenotsif=os.path.basename(fn)  
				co=a1+'/'+fnamenotsif
				#print 'aa'+co
				shutil.copy(fn, co)
			filelist.append(fn)
			file2.write('<string>'+fnamenotsif+'</string>'+"\n")
		elif line.find('<param name="')<>-1 and line.find('use=')<>-1 and line.find('.sif')<>-1:
			pos_param_name=line.find('<param name="')
			pos_use=line.find('use="')+len('use="')
			if line.find('#:')<>-1:
				pos_end_file=line.find('#:')
			if line.find('#"')<>-1:
				pos_end_file=line.find('#"')
			#if line[pos_param_name:pos_use].find('canvas')<>-1:
			#	pos_end_file=line.find('#"/>')
			fname=line[pos_use:pos_end_file]
			fn=os.path.join(dname, fname)
			#print fname, '  ', dname
			print fn
			if not fn in parslist:
				unparsed.append(fn)
				fname=os.path.basename(fname)
				co=a1+'/'+fname
				#shutil.copy(fn, co)
				file2.write(line[0:pos_use]+fname+line[pos_end_file:len(line)]+"\n")
		else:
			file2.write(line)
	file2.close()
	print "End parsing file %s..." % (filename)
	file.close()

Zip=zipfile.ZipFile(a1+'.zip', 'w')	
zipfiles=os.listdir(a1)
for zipname in zipfiles:
	print "Add to archive --- "+a1+'/'+zipname
	Zip.write(a1+'/'+zipname,zipname)
	os.remove(a1+'/'+zipname)
Zip.close()
os.removedirs(a1)
