import os, sys
from getpass import getuser

# In the following list, please ensure you have chosen what you want to install.  By default everything is selected
# If you are installing on a non icse machine, only merlin will install. Recommend turning off all other installations,
# except possibly 'vmd default settings' if you have vmd installed properly

INSTALL_EVERYTHING=False
to_install = {
'vmd':1,
'ovito':1,
'debyer':1,
'pysub':1,
'qwatch':1,
'gcube':1,
'jsub':1,
'jdel':1,
'chkDFT':1,
'chkMD':1,
'view_lmp':1,
'scanDFT':1,
'junest (formerly juju)':0,
'anaconda':0, 				# a Python 2.7.9 distribution that installs to ~/anaconda
'vmd default settings':0,	# improves the default settings of vmd
'file_browser':1, 			# set the file browser not to open a new window per folder
'merlin':1,
'sublime_text_3_build_3083':0,
'prnt':1, # ONLY install if lpstat -p -d returns no available printers
'chrome':1
}

####################################################################################################################
if INSTALL_EVERYTHING:
	for x in to_install:
		to_install[x] = 1

if to_install['file_browser']:
	os.system('gconftool-2   --type bool --set /apps/nautilus/preferences/always_use_browser true')

# Use HOMEDIR instead of /fs/home/USERNAME in order to install on non icse machines
USERNAME = getuser()
HOMEDIR = os.path.expanduser('~')

INSTALLDIR = os.getcwd()
if INSTALLDIR[-1] != '/': INSTALLDIR += '/' # Ensure there is a trailing slash
ZSHRC = HOMEDIR+'/.zshrc'
ZSH_CLANCELOT = HOMEDIR + '/.zsh_clancelot'
BASHRC = HOMEDIR+'/.bashrc'
temp=open(ZSHRC)
zshrc_string=temp.read()
temp.close()

def zshrc_check_add(st,path,zshrc_contents):
	if st not in zshrc_contents:
		f=open(ZSHRC,'a')
		f.write('\n'+st+'\n')
		f.close

if 'source ~/.zsh_clancelot' not in zshrc_string:
	f=open(ZSHRC,'a')
	f.write('''\n# The following loads the Clancelot Config File
if [ -f ~/.zsh_clancelot ]; then
    source ~/.zsh_clancelot
else
    print '404: ~/.zsh_clancelot not found.'
fi
''')
	f.close()
	f=open(BASHRC,'a')
	f.write('''\n# The following loads the Clancelot Config File
if [ -f ~/.zsh_clancelot ]; then
    source ~/.zsh_clancelot
else
    print '404: ~/.zsh_clancelot not found.'
fi
''')
	f.close()


os.system('mkdir -p '+INSTALLDIR) # Ensure the install directory is made
for key in to_install: # Make directories for what we want to install
	if key == 'chkDFT': continue
	if key == 'chkMD': continue
	if key == 'jdel': continue
	if key == 'jsub': continue
	if key == 'vmd': continue
	if key == 'ovito': continue
	if key == 'debyer': continue
	if key == 'view_lmp': continue
	if key == 'scanDFT': continue
	if key == 'pysub': continue
	if key == 'qwatch': continue
	if key == 'gcube': continue
	if key == 'junest (formerly juju)': continue
	if key == 'python 2.7.10': continue
	if key == 'numpy': continue
	if key == 'scipy': continue
	if key == 'cython-0.22': continue
	if key == 'vmd default settings': continue
	if key == 'file_browser': continue
	if key == 'matplotlib': continue
	if key == 'anaconda': continue
	if key == 'sublime_text_3_build_3083': continue
	if key == 'merlin': continue
	if key == 'prnt': continue
	if key == 'chrome': continue
	if to_install[key]: os.system('mkdir -p '+INSTALLDIR+key+'/')


# Give Bash Capabilities to ZSH
f = open(ZSH_CLANCELOT,'w+')
f.write('''###############################################################
############### THE FOLLOWING IS FOR CLANCELOT ################
###############################################################
# Append Path
export PYTHONPATH=$$$$$$/tools:$PYTHONPATH
export PATH=/fs/europa/g_pc/orca_3_0_3_linux_x86-64/:$PATH

# Aliases for our tools
alias get_ext_list='python $$$$$$/tools/get_ext_list.py'
alias get_gauss_list='python $$$$$$/tools/get_gauss_list.py'
alias get_orca_list='python $$$$$$/tools/get_orca_list.py'
alias get_jlist='python $$$$$$/tools/get_jlist.py'

# Bind keys
bindkey '^[[3~' delete-char
bindkey '^[OH' beginning-of-line
bindkey '^[OF' end-of-line
bindkey ';5C' emacs-forward-word
bindkey ';5D' emacs-backward-word

'''.replace('$$$$$$/',INSTALLDIR))

f.close()
f = open(ZSH_CLANCELOT,'a')
f.write('''autoload bashcompinit # Let us use bash commands
bashcompinit

# Note, we will provide an explanation of how these functions work using _jAutoTab, but the rest
# of these functions will be largely uncommented

# This function provides auto-tab for the jlist
_jAutoTab() # By convention, the function name starts with an underscore.
{
local cur # Pointer to current completion word.
local JLIST # Pointer to a variable that will hold your list
COMPREPLY=() # Array variable storing the possible completions.
cur=${COMP_WORDS[COMP_CWORD]}
# Note, you can get the list however you choose. In this example, we call an aliased python file and pass it
# the current working directory so that it can return a list. These lists are in the format of space
# separated strings. For example: 'file1 file2 file3'. Note, we just need to print the list to screen from
# this python file, not return it.
JLIST=$(get_jlist)
# This is the function that will determine what words from your JLIST will be displayed for autocomplete
case "$cur" in
*)
COMPREPLY=( $( compgen -W '$JLIST' $cur ) );; # You need to enter your list here
esac
return 0
}

_pyAutoTab()
{
local cur 
local PYLIST 
COMPREPLY=() 
cur=${COMP_WORDS[COMP_CWORD]}
PYLIST=$(get_ext_list .py $PWD)
case "$cur" in
*)
COMPREPLY=( $( compgen -W '$PYLIST' $cur ) );;
esac
return 0
}

_nbsAutoTab()
{
local cur 
local NBSLIST 
COMPREPLY=() 
cur=${COMP_WORDS[COMP_CWORD]}
NBSLIST=$(get_ext_list .nbs $PWD)
case "$cur" in
*)
COMPREPLY=( $( compgen -W '$NBSLIST' $cur ) );;
esac
return 0
}

_gaussAutoTab()
{
local cur 
local GAUSSLIST 
COMPREPLY=() 
cur=${COMP_WORDS[COMP_CWORD]}
GAUSSLIST=$(get_gauss_list $PWD)
case "$cur" in
*)
COMPREPLY=( $( compgen -W '$GAUSSLIST' $cur ) );;
esac
return 0
}

_orcaAutoTab()
{
local cur 
local ORCALIST 
COMPREPLY=() 
cur=${COMP_WORDS[COMP_CWORD]}
ORCALIST=$(get_orca_list $PWD)
case "$cur" in
*)
COMPREPLY=( $( compgen -W '$ORCALIST' $cur ) );;
esac
return 0
}

''')
f.close


f = open(ZSH_CLANCELOT,'a')
f.write('\n\n')

if to_install['chrome']: f.write('''
# Chrome Alias
alias chrome="/fs/europa/g_pc/chrome/opt/google/chrome/google-chrome --no-sandbox"

## Dependencies
# DOXYGEN
export PATH=/fs/home/hch54/Programs/doxygen/build/bin/:$PATH

# Binutils
export PATH=/fs/home/hch54/Programs/binutils/bin/:$PATH
export LIBRARY_PATH=/fs/home/hch54/Programs/binutils/lib/:$LIBRARY_PATH
export INCLUDE_PATH=/fs/home/hch54/Programs/binutils/include/:$INCLUDE_PATH

# Updated GCC and G++
export PATH=/fs/home/hch54/Programs/gcc_build/bin/:$PATH
export LIBRARY_PATH=/fs/home/hch54/Programs/gcc_build/lib/:$PATH
export LIBRARY_PATH=/fs/home/hch54/Programs/gcc_build/lib64/:$LIBRARY_PATH
export LD_LIBRARY_PATH=/fs/home/hch54/Programs/gcc_build/lib64/:$LD_LIBRARY_PATH
export INCLUDE_PATH=/fs/home/hch54/Programs/gcc_build/include/:$PATH

export LD_LIBRARY_PATH=/fs/home/hch54/Programs/gmp/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/fs/home/hch54/Programs/mpfr/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/fs/home/hch54/Programs/mpc/lib/:$LD_LIBRARY_PATH



''')
if to_install['vmd']: f.write("alias vmd='/fs/europa/g_pc/vmd/bin/vmd'\n\n")
if to_install['qwatch']: f.write("alias qwatch='python "+INSTALLDIR+"console_scripts/qwatch.py'\n\n")
if to_install['pysub']:
	f.write("alias pysub='"+INSTALLDIR+"console_scripts/pysub.sh'\n")
	f.write('complete -F _pyAutoTab '+INSTALLDIR+'console_scripts/pysub.sh\n\n')
	g = open(INSTALLDIR+'console_scripts/pysub.sh','w')
	g.write('python '+INSTALLDIR+'''console_scripts/pysub.py $PWD'/' $@''')
	g.close()
	g = open(INSTALLDIR+'console_scripts/pysub.py','w')

        g.write('''#!/usr/bin/env python
from sys import argv, exit
from os import system

# Default Documentation
help = \'\'\'
pysub
---------
A command line tool to submit jobs to the queue.

pysub [script.py] [Options]

    Flag          Default     Description
-help, -h     :            :  Print this help menu
-n            :     1      :  Number of processors to use
-q            :    batch   :  Which queue to submit to
-xhost, -x    :            :  If needed, specify computer

Default behaviour is to generate a job with the same name
as the python script and to generate a .log file with the
same name as well.  NOTE! If using xhost, make sure it is
the last flag used as we assume all remaining inputs are
the desired computers.
 \'\'\'

# Parse Arguments
if '-h' in argv or '-help' in argv or len(argv) < 3:
	print help
	exit()

# Parse Arguments
nprocs = '1'
queue = 'batch'
xhost = None
debug = False
path = argv[1]
job_name = argv[2]
if ".py" in job_name: job_name = job_name.split(".py")[0]

if "-n" in argv[2:]: nprocs = argv[argv.index('-n')+1]
if "-q" in argv[2:]: queue = argv[argv.index('-q')+1]
if "-x" in argv[2:]: xhost = argv[argv.index('-x')+1:]
elif "-xhost" in argv[2:]: xhost = argv[argv.index('-xhost')+1:]
if "-debug" in argv[2:]: debug = True
elif "-d" in argv[2:]: debug = True

# Setup nbs script
NBS = \'\'\'##NBS-name: "$JOB_NAME$"
##NBS-nproc: $NPROCS$
##NBS-queue: "$QUEUE$"
$XHOST$
source '''+HOMEDIR+'''/.zshrc

'''+HOMEDIR+'''/anaconda/bin/python2.7 -u $PY_NAME1$.py >> $PY_NAME2$.log 2>&1
\'\'\'

NBS = NBS.replace("$JOB_NAME$",job_name)
NBS = NBS.replace("$NPROCS$",nprocs)
NBS = NBS.replace("$QUEUE$",queue)
NBS = NBS.replace("$PY_NAME1$",path + job_name)
NBS = NBS.replace("$PY_NAME2$",path + job_name)

if xhost is None:
	NBS = NBS.replace("$XHOST$","")
else:
	xhosts = ", ".join( map(lambda x: '"' + x + '"', xhost) )
	NBS = NBS.replace("$XHOST$","##NBS-xhost: %s" % xhosts)

NBS_fptr = open(job_name+".nbs",'w')
NBS_fptr.write(NBS)
NBS_fptr.close()

# Submit job
system('jsub ' + job_name + '.nbs')

''')
	g.close()
	os.system('chmod 755 '+INSTALLDIR+'console_scripts/pysub.sh')
if to_install['gcube']:
	f.write("alias gcube='"+INSTALLDIR+"console_scripts/gcube.sh'\n")
	f.write('complete -F _gaussAutoTab '+INSTALLDIR+'console_scripts/gcube.sh\n\n')
	g = open(INSTALLDIR+'console_scripts/gcube.sh','w')
	g.write('python '+INSTALLDIR+'''console_scripts/gcube.py $PWD'/' $@''')
	g.close()
	g = open(INSTALLDIR+'console_scripts/gcube.py','w')
	g.write('''from merlin import *
from subprocess import Popen

old_job = sys.argv[2]

if not os.path.exists('gaussian/%s.chk' % old_job):
	print 'Fatal error: file "gaussian/%s.chk" does not exist.' % old_job
	exit()

if not g09.parse_atoms(old_job):
	print 'Fatal error: "%s" is not converged. gcube does not work on unconverged jobs.' % old_job
	exit()

# Get the file to check
if not os.path.exists('gaussian/%s.fchk' % old_job):
	print 'Making gaussian/%s.fchk' % old_job
	Popen('/usr/local/gaussian/g09/g09/formchk gaussian/%s.chk gaussian/%s.fchk' % (old_job,old_job), shell=True).wait()

# Make the density and potential cube files
if not os.path.exists('gaussian/%s.cube' % (old_job+'_d')):
	print 'Making gaussian/%s.cube' % (old_job+'_d')
	Popen('/usr/local/gaussian/g09/g09/cubegen 0 density gaussian/%s.fchk gaussian/%s.cube 0 h'% (old_job,old_job+'_d'), shell=True).wait()

if not os.path.exists('gaussian/%s.cube' % (old_job+'_p')):
	print 'Making gaussian/%s.cube' % (old_job+'_p')
	Popen('/usr/local/gaussian/g09/g09/cubegen 0 potential gaussian/%s.fchk gaussian/%s.cube 0 h'% (old_job,old_job+'_p'), shell=True).wait()

if not (os.path.exists('gaussian/%s.cube' % (old_job+'_p')) and os.path.exists('gaussian/%s.cube' % (old_job+'_d')) ):
	print 'Fatal error: cube files not created'
	exit()

vmd_file = \'\'\'# Type logfile console into console to see all commands

# Get data
mol new gaussian/$$FPTR$$_d.cube
mol addfile gaussian/$$FPTR$$_p.cube

# Adjust first rep
mol modcolor 0 0 element
mol modstyle 0 0 CPK

# Adjust second rep
mol addrep 0
mol modcolor 1 0 Volume 1
mol modstyle 1 0 Isosurface 0.040000 0 0 0 1 1
mol modmaterial 1 0 Transparent\'\'\'.replace('$$FPTR$$',old_job)

f = open('tmp.vmd','w')
f.write(vmd_file)
f.close()

Popen('/fs/europa/g_pc/vmd-1.9 -e tmp.vmd', shell=True)\n''')
	g.close()
	os.system('chmod 755 '+INSTALLDIR+'console_scripts/gcube.sh')
if to_install['jsub']: f.write('complete -F _nbsAutoTab jsub\n\n')
if to_install['jdel']: f.write('complete -F _jAutoTab jdel\n\n')
if to_install['chkDFT']:
	f.write("alias chkDFT='python "+INSTALLDIR+"console_scripts/chkDFT.py'\n")
	f.write('''alias viewg='function _viewg(){chkDFT $1 -dft g09 -v $@};_viewg'
alias viewo='function _viewo(){chkDFT $1 -dft orca -v $@};_viewo'
alias chkg='function _chkg(){chkDFT $1 -dft g09 $@};_chkg'
alias ggedit='function _ggedit(){gedit orca/$1/$1.log &};_ggedit'
alias geditg='ggedit'
alias gtail='function _gtail(){tail orca/$1/$1.log $2 $3};_gtail'
alias tailg='gtail'
alias chko='function _chko(){chkDFT $1 -dft orca $@};_chko'
alias ogedit='function _ogedit(){gedit orca/$1/$1.out &};_ogedit'
alias gedito='ogedit'
alias otail='function _otail(){tail orca/$1/$1.out $2 $3};_otail'
alias tailo='otail'\n''')
if to_install['chkMD']:
	f.write("alias chkMD='python "+INSTALLDIR+"console_scripts/chkMD.py'\n")
	f.write('''alias chkl='function _chkg(){chkMD $1 -v $@};_chkg'
alias viewl='function _viewl(){chkDFT $1 -v $@};_viewl'
alias lgedit='function _lgedit(){gedit lammps/$1/$1.log &};_lgedit'
alias geditl='lgedit'\n''')
if to_install['merlin']: f.write("alias merlin='python -i "+INSTALLDIR+"tools/merlin.py'\n")
if to_install['view_lmp']: f.write("alias view_lmp='function _view_lmp(){python "+INSTALLDIR+"console_scripts/view_lmp.py $1 $@};_view_lmp'\n")
if to_install['scanDFT']: f.write("\nalias scanDFT='python "+INSTALLDIR+"console_scripts/scanDFT.py'\n")
if to_install['prnt']: f.write('''
function _prnt()
{
gs \
 -sOutputFile="'''+HOMEDIR+'''/tmp.pdf" \
 -sDEVICE=pdfwrite \
 -sPAPERSIZE=letter \
 -dCompatibilityLevel=1.4 \
 -dNOPAUSE \
 -dBATCH \
 -dPDFFitPage \
 "$1"

ssh asimov "lpr -P hplj4525-365 -o sides=two-sided-long-edge -o InputSlot=Tray2 '''+HOMEDIR+'''/tmp.pdf;logout"

rm '''+HOMEDIR+'''/tmp.pdf

echo "Done..."
}

alias prnt='_prnt'
''')
f.write('''\n###############################################################
################## END OF THE CLANCELOT CODE ##################
###############################################################''')
f.close()

downloaded_tarball=False

#####The following is modified from http://code.activestate.com/recipes/134892/
#####As opposed to raw_input(), getchar() does not wait for a new line (*enter*)
def getchar():
    import tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch
#####


def reinstall(str):
	while True:
		print(str+' y/n:')
		resp=getchar()
		if resp=='y':
			return True
		if resp=='n':
			return False

if to_install['vmd default settings']:
	if os.path.exists(HOMEDIR+'/.vmdrc'):
		if reinstall('Previous vmd settings found, backup old ~/.vmdrc to ~/.vmdrc_history?'):
			os.system('mv ~/.vmdrc ~/.vmdrc_history')
	os.system('cp vmdrc_default.txt ~/.vmdrc')

if to_install['ovito']:
	zshrc_check_add('export PATH=/fs/europa/g_pc/ovito-2.6.2-x86_64/bin/:$PATH',ZSHRC,zshrc_string)

if to_install['debyer']:
	zshrc_check_add('export PATH=/fs/europa/g_pc/debyer/debyer/:$PATH',ZSHRC,zshrc_string)

def anaconda_install():
	os.system('wget -P ~/lib/ https://repo.continuum.io/archive/Anaconda-2.2.0-Linux-x86_64.sh')
	os.system('bash ~/lib/Anaconda-2.2.0-Linux-x86_64.sh -fb')
	zshrc_check_add('export PATH=~/anaconda/bin:$PATH',ZSHRC,zshrc_string)
	#zshrc_check_add("export PYTHONPATH='"+INSTALLDIR+"/tools/'",ZSHRC,zshrc_string)
	os.system('rm ~/lib/Anaconda-2.2.0-Linux-x86_64.sh')

def sublime_install():
	os.system('mkdir -p '+HOMEDIR+'/lib')
	os.system('wget -P ~/lib/ http://c758482.r82.cf2.rackcdn.com/sublime_text_3_build_3083_x64.tar.bz2')
	os.system('tar xvf '+HOMEDIR+'/lib/sublime_text_3_build_3083_x64.tar.bz2 -C '+HOMEDIR+'/lib/')
	zshrc_check_add("alias sublime='~/lib/sublime_text_3/sublime_text",ZSHRC,zshrc_string)
	zshrc_check_add("alias subl='~/lib/sublime_text_3/sublime_text",ZSHRC,zshrc_string)

def junest_install():
	os.system('git clone https://github.com/fsquillace/junest.git ~/juju --quiet')
	zshrc_check_add("export PATH=~/juju/bin:$PATH",ZSHRC,zshrc_string)
	zshrc_check_add("alias juju='junest'",ZSHRC,zshrc_string)

if to_install['anaconda']:
	if os.path.exists(HOMEDIR+'/anaconda') and os.path.isdir(HOMEDIR+'/anaconda'):
		if reinstall('Previous installation found, reinstall Anaconda (Python 2.7.9 and packages)?'):
			anaconda_install()
		else:
			print('...SKIPPING ANACONDA (RE)INSTALLATION...')
	else:
		anaconda_install()
else:
	if os.path.exists(HOMEDIR+'/anaconda') and os.path.isdir(HOMEDIR+'/anaconda'):
		zshrc_check_add('export PATH=~/anaconda/bin:$PATH',ZSHRC,zshrc_string)


if to_install['sublime_text_3_build_3083']:
	if os.path.exists(HOMEDIR+'/lib/sublime_text_3') and os.path.isdir(HOMEDIR+'/lib/sublime_text_3'):
		if reinstall('Previous installation found, reinstall Sublime Text 3?'):
			os.system('rm -rf '+HOMEDIR+'/lib/sublime_text_3')
			sublime_install()
			downloaded_tarball=True
		else:
			print('...SKIPPING SUBLIME (RE)INSTALLATION...')
	else:
		sublime_install()
		downloaded_tarball=True
else:
	if os.path.exists(HOMEDIR+'/lib/sublime_text_3') and os.path.isdir(HOMEDIR+'/lib/sublime_text_3'):
		zshrc_check_add("alias sublime='~/lib/sublime_text_3/sublime_text",ZSHRC,zshrc_string)
		zshrc_check_add("alias subl='~/lib/sublime_text_3/sublime_text",ZSHRC,zshrc_string)

if to_install['junest (formerly juju)']: 
	if os.path.exists(HOMEDIR+'/juju') and os.path.isdir(HOMEDIR+'/juju'):
		if reinstall('Previous installation found, reinstall juju/junest?'):
			os.system('mv '+HOMEDIR+'/juju '+HOMEDIR+'/.trash/')
			if os.path.exists(HOMEDIR+'/.junest') and os.path.isdir(HOMEDIR+'/.junest'):
				os.system('mv '+HOMEDIR+'/.junest '+HOMEDIR+'/.trash/')
			junest_install()
			print("\nTo finish installing 'junest' please run:\n'pacman -Syyu pacman-mirrorlist && pacman -S gtk2 avogadro grep make ttf-liberation gedit'\n\n(when prompted for GL version, pick option 2, nvidia)\n\n\n")
			os.system("zsh -c 'junest -f'")
		else:
			print('...SKIPPING JUJU/JUNEST (RE)INSTALLATION...')
	else:
		junest_install()
		print("\nTo finish installing 'junest' please run:\n'pacman -Syyu pacman-mirrorlist && pacman -S gtk2 avogadro grep make ttf-liberation gedit'\n\n(when prompted for GL version, pick option 2, nvidia)\n\n\n")
		print("\nNote, sometimes avogadro might not work even after this. Run 'pacman -S bumblebee' if this happens.\n\n\n")
		os.system("zsh -c 'junest -f'")
else:
	if os.path.exists(HOMEDIR+'/juju') and os.path.isdir(HOMEDIR+'/juju'):
		zshrc_check_add("export PATH=~/juju/bin:$PATH",ZSHRC,zshrc_string)
		zshrc_check_add("alias juju='junest'",ZSHRC,zshrc_string)

if downloaded_tarball:
	print('Removing previously downloaded tarballs')
	os.system('rm -i '+HOMEDIR+'/lib/*.tar.*')

os.system('cp pre-commit.sh .git/hooks/pre-commit') #copy pre-commit hook script to expected location
os.system('chmod +x .git/hooks/pre-commit') #make pre-commit hook script executable

print("\n\n--------------Installation Finished--------------\nPlease reopen Terminal to apply changes.")

