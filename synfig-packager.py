#!python
# -*- coding: utf-8 -*-

import sys, os, shutil, re, zipfile, random, gzip

global parslist

parslist=[]
unparsed=[]
filelist=[] # список файлов которые уже скопировали
filelist2=[] # список скопированных имён файлов чтобы не повторялись
filelist_path=[]
zipfiles=[]
siflist=[]
siflist2=[]
lst_image_file=''
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

def copy_image(inputt, outputt):
	print "=== Copy image called! ==="
	global lst_image_file
	if not inputt in filelist:
		input_name=os.path.basename(inputt)
		output_name=outputt+'/'+input_name
		count1=0
		while output_name in filelist2:
			count1=count1+1
			output_name=input_name[:input_name.find('.')] +'-'+ '%d' % count1
			output_name=output_name+input_name[input_name.find('.'):]
		print '% ', output_name
		filelist.append(inputt)
		filelist2.append(output_name)
		while output_name.find('/')<>-1:
			output_name=output_name[output_name.find('/')+1:]
			print '%%%%%% ', output_name
		print '-------',inputt
		shutil.copy(inputt, outputt+'/'+output_name)
		lst_image_file=output_name
		if output_name.find('.lst')<>-1:
			#file2.write('<string>'+output_name+'</string>'+"\n")
			file_lst=open(inputt)
			if not os.path.exists(outputt+'/sequences/'):
				os.mkdir(outputt+'/sequences/')
			output_path=outputt+'/sequences/'+output_name[:output_name.find('.')]
			os.mkdir(outputt+'/sequences/'+output_name[:output_name.find('.')]+'/')
			output_name='sequences/'+output_name[:output_name.find('.')]+'/'+output_name
			filelist_path.append(output_name)
			file_lst_out=open(outputt+'/'+output_name, 'w')
			lst_files=file_lst.readlines()
			for ii, image_name in enumerate(lst_files):
				if image_name.find('.')<>-1:
					print "!!!",inputt
					image_path=inputt[:inputt.find('.lst')-len(input_name)+4]+image_name[:len(image_name)-1]
					#co=a1+'/'+image_name
					#copy_image(image_path, a1)
					print '+++' + image_path
					file_lst_out.write(copy_image(image_path, output_path[:len(output_path)]) + "\n")
					#shutil.copy(image_path, co)
				else:
					file_lst_out.write(image_name)
		else:
			filelist_path.append(output_name)
		print '######### ',output_name
		return output_name
	else:
		return filelist_path[filelist.index(inputt)]
#def lst(inputt, outputt):

def copy_font(inputt, outputt):
	print '\\\\\\\\ copy_font called ///////'
	if not os.path.exists(outputt+'/font/'):
				os.mkdir(outputt+'/font/')
	if not inputt in filelist:
		input_name=os.path.basename(inputt)
		output_name=outputt+'/'+input_name
		count1=0
		while output_name in filelist2:
			count1=count1+1
			output_name=input_name[:input_name.find('.')] +'-'+ '%d' % count1
			output_name=output_name+input_name[input_name.find('.'):]
		while output_name.find('/')<>-1:
			output_name=output_name[output_name.find('/')+1:]
		print '% ', output_name
		filelist.append(inputt)
		filelist2.append(output_name)
		print '-------',inputt
		output_name='font/'+output_name
		shutil.copy(inputt, outputt+'/'+output_name)
		filelist_path.append(output_name)
		print '######### ',output_name
		return output_name
	else:
		return filelist_path[filelist.index(inputt)]
	
	
		
def copy_sif(inputt, outputt):
	#if inputt.find('.sifz'):
	#	sifz=gzip.open(inputt)
	#	path = inputt
	#	while path[len(path)-1]<>'/':
	#		path=path[:len(path)-2]
	#	sifz.read(path)
	#	#print '------------- ',sifzfile
	#	sifz.close()
	#	inputt=inputt[:len(inputt)-1]
	if not inputt in siflist:
		input_name=os.path.basename(inputt)
		output_name=input_name
		count1=0
		while output_name in siflist2:
			count1=count1+1
			output_name=input_name[:input_name.find('.')] +'-'+ '%d' % count1
			output_name=output_name+input_name[input_name.find('.'):]
		siflist.append(inputt)
		siflist2.append(output_name)
		shutil.copy(inputt, outputt+'/'+output_name)
		return output_name
	else:
		return siflist2[siflist.index(inputt)]
		
		
		

a=sys.argv[1]
a1=os.path.basename(a)	
a1=a1[:a1.find('.sif')]
a1="/tmp/"+a1+'_'+"%d" % (random.randint(1,100))#a[:a.find('.sif')]
a1=sys.argv[2]
a1=a1[:a1.find('.')]
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
flag_font=False
while len(unparsed)>0:
	filepath=unparsed.pop()
	print "Parsing file: %s" %(filepath)
	parslist.append(filepath)
	sifdir=filepath[:filepath.find(os.path.basename(filepath))]
	if filepath.find('.sifz')<>-1:
		file=gzip.open(filepath)
	else:
		file=open(filepath)
	filename=os.path.basename(filepath)
	co=a1+'/'+filename
	shutil.copy(a, co)
	flag_filename=False
	#fname=a[:a.find(filename)]
	fname=filename
	#a1="/tmp/"+os.path.basename(a1)
	#print "---",a1+'/'+fname
	file2=open(a1+'/'+fname, 'w')
	massiv=file.readlines()
	for i, line in enumerate(massiv):
		if line.find('<param name="filename">')<>-1:
			flag_filename=True
			file2.write(line)
		elif line.find('</param>')<>-1:
			flag_filename=False
			flag_font=False
			file2.write(line)
		elif flag_filename and line.find('<string')<>-1:
			print 'line=',line
			str=massiv[i]
			pos1=str.find('>')+1
			pos2=str.find('</string>')
			#print "+++ ",str[pos1:pos2]
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
				#print '+++ ', fn
				#print 'aa'+co
				#shutil.copy(fn, co)
				#if line.find('.lst')<>-1:
				#	file_lst=open(fn)
				#	lst_files=file_lst.readlines()
				#	for ii, image_name in enumerate(lst_files):
				#			if image_name.find('.')<>-1:
				#				image_path=fn[:fn.find('.lst')-len(fnamenotsif)+4]+image_name[:len(image_name)-1]
				#				co=a1+'/'+image_name
								#print '--- ',co
				#				shutil.copy(image_path, co)
			result_filename=copy_image(fn,a1)
			print '************',result_filename
			file2.write('<string>'+result_filename+'</string>'+"\n")
			#filelist.append(fn)
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
				result_filename=copy_sif(fn,a1)
				#shutil.copy(fn, co)
				file2.write(line[0:pos_use]+result_filename+line[pos_end_file:len(line)]+"\n")
		elif line.find('<param name="family"')<>-1:
			flag_font=True
			file2.write(line)
			print '---------------------------------------------'
		elif flag_font and line.find('<string')<>-1 and line.find('.ttf')<>-1:
			print 'line=',line
			str=massiv[i]
			pos1=str.find('>')+1
			pos2=str.find('</string>')
			#print "+++ ",str[pos1:pos2]
			font_name=str[pos1:pos2]
			#print "       Join input:",sifdir,fn 
			fn=os.path.join(sifdir ,font_name)
			#print "+++",sifdir,"___",fnamenotsif
			fn=os.path.abspath(fn)
			if fn.find('&#x')<>-1:
				fn=decode_unicode_references(fn)
				fn=fn.encode('utf-8')
			if not fn in filelist:
				print fn
				fnamenotsif=os.path.basename(fn)  
				co=a1+'/'+fnamenotsif
			result_filename=copy_font(fn,a1)
			print '************',result_filename
			file2.write('<string>'+result_filename+'</string>'+"\n")
			#filelist.append(fn)
		else:
			file2.write(line)
	file2.close()
	print "End parsing file %s..." % (filename)
	file.close()

#Zip=zipfile.ZipFile(a1+'.zip', 'w')	
#zipfiles=os.listdir(a1)
#for zipname in filelist2:
#	print "Add to archive --- "+a1+'/'+zipname
#	Zip.write(zipname,zipname)
#	os.remove(zipname)
#for zipname in siflist2:
#	print "Add to archive --- "+a1+'/'+zipname
#	Zip.write(a1+'/'+zipname,zipname)
#	os.remove(a1+'/'+zipname)

#Zip.close()
#os.removedirs(a1)
