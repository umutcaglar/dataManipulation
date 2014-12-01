from os import listdir, system
from os.path import isfile, join, splitext
import re, sys, os


def createMergeCommand( bname, files, read, destdir ):
	uniques = []
	for f in files:
		m = re.match( bname.encode('unicode-escape') + r'_(.*)_' + read + r'_(\d+)\.fastq', f )
		if m:
			tokens = m.group(1).split('_')
			tokens.append( m.group(2) )
			if tokens[0] == 'xr':
				tokens.pop(0)
			for i in xrange( len( tokens ) ):
				if i >= len( uniques ):
					uniques.append([])
				if ( not tokens[i] in uniques[i] ):
					uniques[i].append( tokens[i] )
	for l in uniques:
		l.sort()
	new_tokens = [ '+'.join(l) for l in uniques ]
	new_name = bname+'_' + '_'.join(new_tokens) + '_' + read + '.fastq' 
	print new_name
	command = 'zcat ' + ' '.join(files) + ' > ' + destdir + new_name
	print command
	return command
	
def createMergeCommand_old( bname, files, read, destdir ):
	uniques = []
	for f in files:
		m = re.match( bname.encode('unicode-escape') + r'_(.*)_' + read + r'_(\d+)\.fastq', f )
		if m:
			tokens = m.group(1).split('_')
			tokens.append( m.group(2) )
			for i in xrange( len( tokens ) ):
				if i >= len( uniques ):
					uniques.append([])
				if ( not tokens[i] in uniques[i] ):
					uniques[i].append( tokens[i] )
	new_tokens = [ '+'.join(l.sort()) for l in uniques ]
	new_name = bname+'_' + '_'.join(new_tokens) + '_' + read + '.fastq' 
	print new_name
	command = 'zcat ' + ' '.join(files) + ' > ' + destdir + new_name
	print command
	return command


##workdir = '/scratch/02159/ds29583/data/sample*/RNA/*depleted.raw/'
workdir = sys.argv[1]
saved_path = os.getcwd() # save current path
os.chdir(workdir) # change to workdir

(root, ext) = splitext(workdir.rstrip('/'))
destdir = root+".processed/"

all_files = [ f for f in listdir(workdir) if isfile(join(workdir,f)) ]

basenames = {}
for f in all_files:
	m = re.match( r'(MURI_\d+)_.*', f )
	if m:
		bname = m.group(1)
		if ( bname in basenames ):
			basenames[bname].append( f )
		else:
			basenames[bname]=[f]
			

for ( bname, files ) in basenames.items():
	R1_files = [f for f in files if re.match( r'.*_R1_\d+\.fastq', f )]
	R2_files = [f for f in files if re.match( r'.*_R2_\d+\.fastq', f )]
	print bname
	print R1_files
	print R2_files
	print files
	print   
	
	R1_command = createMergeCommand( bname, R1_files, 'R1', destdir )
	R2_command = createMergeCommand( bname, R2_files, 'R2', destdir )
	
	system('mkdir ' + destdir)
	
	system(R1_command)
	system(R2_command)
	
	
os.chdir( saved_path ) # restore previously saved path
