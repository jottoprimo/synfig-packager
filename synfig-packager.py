#!python
# -*- coding: utf-8 -*-

import sys, os, shutil, re, zipfile, random, gzip, tempfile
import subprocess

global parslist

parslist=[]
unparsed=[]
filelist=[] # список файлов которые уже скопировали
filelist2=[] # список скопированных имён файлов чтобы не повторялись
filelist_path=[]
zipfiles=[]
siflist=[]
siflist2=[]
zip_dirs=[]
lst_image_file=''
#parslist2=[]

def myabspath(path):
	proc = subprocess.Popen('pwd', shell = True, stdout=subprocess.PIPE)
	pwd = proc.stdout.read()
	return os.path.normpath(os.path.join(pwd, path))

def _callback(matches):
    id = matches.group(1)
    try:
        return unichr(int(id,16))
    except:
        return id

def decode_unicode_references(data):
    return re.sub("&#x([a-zA-Z0-9]+)(;|(?=\s))", _callback, data)


def copy_image(inputt, outputt, t):
	#print "=== Copy image called! ==="
	global lst_image_file
	if not os.path.exists(inputt):
		print 'Warning! File "', inputt, '"', 'not found';
		return ''
	else:
		if not inputt in filelist:
			input_name=os.path.basename(inputt)
			output_name=outputt+'/'+input_name
			count1=0
			while output_name in filelist2:
				count1=count1+1
				output_name=input_name[:input_name.find('.')] +'-'+ '%d' % count1
				output_name=output_name+input_name[input_name.find('.'):]
			#print '% ', output_name
			filelist.append(inputt)
			filelist2.append(output_name)
			while output_name.find('/')<>-1:
				output_name=output_name[output_name.find('/')+1:]
				#print '%%%%%% ', output_name
			#print '-------',inputt
			if not t: #or  output_name.find('.lst')<>-1:
				shutil.copy(inputt, outputt+'/'+output_name)
				#print '----------'
			if t and output_name.find('.lst')==-1:
				#print '+++++++ ' ,t
				if not os.path.exists(outputt+'/images/'):
					os.mkdir(outputt+'/images/')
				shutil.copy(inputt, outputt+'/images/'+output_name)
			lst_image_file=output_name
			if t and output_name.find('.lst')==-1:
				output_name='images/'+output_name
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
						#print "!!!",inputt
						image_path=inputt[:inputt.find('.lst')-len(input_name)+4]+image_name[:len(image_name)-1]
						#co=a1+'/'+image_name
						#copy_image(image_path, a1)
						#print '+++' + image_path
						file_lst_out.write(copy_image(image_path, output_path[:len(output_path)], False) + "\n")
						#shutil.copy(image_path, co)
					else:
						file_lst_out.write(image_name)
			else:
				filelist_path.append(output_name)
			#print '######### ',output_name
			x=outputt[outputt.find(a1):]
			x=x[x.find('/')+1:]
			if x.find('/')==-1:
				x=''
			else:
				x=x+'/'
			#if t and output_name.find('.lst')==-1:
			#	print 'not_lst'
			#	output_name='images/'+output_name
			#print '################# ', output_name
			info_file.write(inputt+"\n"+x+output_name+2*"\n")
			#filelist_path.append(output_name)
			return output_name
		else:
			return filelist_path[filelist.index(inputt)]
#def lst(inputt, outputt):

def copy_font(inputt, outputt):
	#print '\\\\\\\\ copy_font called ///////'
	if not os.path.exists(inputt):
		print 'Warning! File "', inputt, '"', 'not found';
		return ''
	else:
		if not os.path.exists(outputt+'/fonts/'):
					os.mkdir(outputt+'/fonts/')
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
			#print '% ', output_name
			filelist.append(inputt)
			filelist2.append(output_name)
			#print '-------',inputt
			output_name='fonts/'+output_name
			shutil.copy(inputt, outputt+'/'+output_name)
			filelist_path.append(output_name)
			#print '######### ',output_name
			info_file.write(inputt+"\n"+output_name+2*"\n")
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
	#print '+-+-+-+-+-+-+-+-+-+-+-+-+-+- ', inputt in siflist, ' ',inputt
	if not os.path.exists(inputt):
		print 'Warning! File "',inputt,'"', 'not found';
		return ''
	else:
		unparsed.append(inputt)
		if not inputt in siflist:
			print '----'
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
			info_file.write(inputt+"\n"+output_name+2*"\n")
			return output_name
		else:
			return siflist2[siflist.index(inputt)]
		
if len(sys.argv)==1:
	print ''
	print 'USAGE: synfig-packager.py FILENAME.sif'
	print ''
	sys.exit(1)
a=sys.argv[1]
a1=os.path.basename(a)	
a1=a1[:a1.find('.sif')]
a1="/tmp/"+a1#"%d" % (random.randint(1,100))#a[:a.find('.sif')]
tempdir=tempfile.mkdtemp()
prefix=''
if len(sys.argv)==3:
	a2=sys.argv[2]
else:
	#prefix='/tmp/'
	a1=a1[5:]
	a2=a1


	
#if len(a2)>0:
if a2.find('.zip')<>-1:
	a1=a2[:len(a2)-4]
else:
	a1=a2
#if os.path.exists(a1):
#	print "error: %s already exists" % (a1)
#	sys.exit(1)
#else:
#	os.mkdir(a1)
info_file=open(tempdir+'/'+'info', 'w')

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
os.mkdir(tempdir+'/'+a1)
tempdir=tempdir+'/'+a1
while len(unparsed)>0:
	filepath=unparsed.pop()
	#print "Parsing file: %s" %(filepath)
	#print "Parsing file: %s" %(filepath)
	parslist.append(filepath)
	sifdir=filepath[:filepath.find(os.path.basename(filepath))]
	if filepath.find('.sifz')<>-1:
		file=gzip.open(filepath)
	else:
		file=open(filepath)
	filename=os.path.basename(filepath)
	co=tempdir+'/'+filename
	shutil.copy(a, co)
	flag_filename=False
	#fname=a[:a.find(filename)]
	fname=filename
	#a1="/tmp/"+os.path.basename(a1)
	#print "---",a1+'/'+fname
	file2=open(tempdir+'/'+fname, 'w')
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
			#print 'line=',line
			str=massiv[i]
			pos1=str.find('>')+1
			pos2=str.find('</string>')
			#print "+++ ",str[pos1:pos2]
			fnamenotsif=str[pos1:pos2]
			#print "       Join input:",sifdir,fn 
			fn=os.path.join(sifdir ,fnamenotsif)
			#print "+++",sifdir,"___",fnamenotsif
			fn=myabspath(fn)
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
				#print fn
				fnamenotsif=os.path.basename(fn)  
				co=tempdir+'/'+fnamenotsif
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
			result_filename=copy_image(fn,tempdir, True)
			#print '1111************',result_filename,'<----->', filepath
			print fn,'--->',result_filename
			file2.write('<string>'+result_filename+'</string>'+"\n")
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
			#print fn
			if not fn in parslist:
				fname=os.path.basename(fname)
				co=tempdir+'/'+fname
				result_filename=copy_sif(fn,tempdir)
				#shutil.copy(fn, co)-
				if result_filename<>'':
					file2.write(line[:pos_use]+result_filename+line[pos_end_file:len(line)]+"\n")
					print fn,'--->',result_filename
		elif line.find('<param name="family"')<>-1:
			flag_font=True
			file2.write(line)
			#print '---------------------------------------------'
		elif flag_font and line.find('<string')<>-1 and line.find('.ttf')<>-1:
			#print 'line=',line
			str=massiv[i]
			pos1=str.find('>')+1
			pos2=str.find('</string>')
			#print "+++ ",str[pos1:pos2]
			font_name=str[pos1:pos2]
			#print "       Join input:",sifdir,fn 
			fn=os.path.join(sifdir ,font_name)
			#print "+++",sifdir,"___",fnamenotsif
			fn=myabspath(fn)
			if fn.find('&#x')<>-1:
				fn=decode_unicode_references(fn)
				fn=fn.encode('utf-8')
			if not fn in filelist:
				#print fn
				fnamenotsif=os.path.basename(fn)  
				co=tempdir+'/'+fnamenotsif
			result_filename=copy_font(fn,tempdir)
			#print '************',result_filename
			file2.write('<string>'+result_filename+'</string>'+"\n")
			#filelist.append(fn)
			print fn,'--->',result_filename
		else:
			file2.write(line)
	file2.close()
	#print "End parsing file %s..." % (filename)
	file.close()
	
info_file.close()


Zip=zipfile.ZipFile(prefix+a1+'.zip', 'w')	
zip_dirs.append(tempdir)
while len(zip_dirs)>0:
	zip_path=zip_dirs.pop()
	#print '++++++++++++++++++++ ', zip_path
	zipfiles=os.listdir(zip_path)
	for zipname in zipfiles:
		#print a1+'/'+zipname
		if not os.path.isdir(zip_path+'/'+zipname):
			in_zip_path=zip_path[zip_path.find(a1):]
			print "Add to archive --- "+zip_path+'/'+zipname
			Zip.write(zip_path+'/'+zipname,in_zip_path+'/'+zipname)
			#os.remove(zip_path+'/'+zipname)
		if os.path.isdir(zip_path+'/'+zipname):
			#print '------------------'
			zip_dirs.append(zip_path+'/'+zipname)
	#print len(zip_dirs)
	#os.remove(zip_path)
#Zip.write(a1,a1)
#for zipname in siflist2:
#	print "Add to archive --- "+a1+'/'+zipname
#	Zip.write(a1+'/'+zipname,zipname)
#	os.remove(a1+'/'+zipname)

Zip.close()
shutil.rmtree(tempdir)
#os.removedirs(a1)
