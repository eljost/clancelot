import os, sys
import subprocess
import g09, orca
import units, utils, sysconst, constants, files

# One can easily change defaults here (if they do, probably change the
# help text below accordingly).
dft, u1, u2, scale, out_name, vmd = 'g09', 'Ha', 'Ha', 1.0, 'out', False
dft_list = [dft,'orca']

if '-h' in sys.argv or '-help' in sys.argv:
	print('''
chkDFT
---------
A command to quickly get a glimpse of a DFT simulation.
chkDFT [Sim_Name] [Options]

    Flag        Default     Description
-help, -h     :        :  Print this help menu
-dft          :  g09   :  Specify what type of dft simulation you want to
                          parse. By default it is 'g09', but can be
                          'orca' also.
-units, -u    :  Ha    :  Specify the units you want the output to be in.
                          By default this is Hartree.
-scale        :  1.0   :  Scale all energies by this value
-out, -o      :  out   :  Make an output file with this name holding all xyz
                          coordinates. If no xyz data is available this will
                          not run. Default output name is 'out.xyz' but user
                          can choose their own using this command. 
-vmd, -v      :        :  Opens output xyz file in vmd. Flag turns on.

ex. chkDFT water -dft orca -u kT_300
''')
	sys.exit()

# Get simulation name
run_name = sys.argv[1]
# Get the dft type
if '-dft' in sys.argv:
	dft = sys.argv[sys.argv.index('-dft') + 1].lower()
	if dft not in dft_list:
		print("Error - %s not recognized for dft." % dft)
		sys.exit()
# Get units
if '-u' in sys.argv or '-units' in sys.argv:
	s = '-u' if '-u' in sys.argv else '-units'
	u2 = sys.argv[sys.argv.index(s) + 1]
	if u2 not in constants.ENERGY:
		print("Error - Energy unit not available. Consider using -scale.")
		sys.exit()
# Get scale
if '-scale' in sys.argv:
	scale = float(sys.argv[sys.argv.index('-scale') + 1])
# Get output name
if '-out' in sys.argv or '-o' in sys.argv:
	s = '-o' if '-o' in sys.argv else '-out'
	out_name = sys.argv[sys.argv.index(s) + 1].replace(' ','_')
if len(out_name) < 5 or out_name[-4:] != '.xyz': out_name += '.xyz'
# Get VMD display status
if '-vmd' in sys.argv or '-v' in sys.argv:
	vmd = True
	
# Read in data
if dft == 'g09':
	try:
		data = g09.read(run_name)
	except IOError:
		print("Error - g09 simulation %s does not exist. Are you sure -dft g09 is correct?" % run_name)
		sys.exit()
elif dft == 'orca':
	try:
		data = orca.read(run_name)
	except IOError:
		print("Error - orca simulation %s does not exist. Are you sure -dft orca is correct?" % run_name)
		sys.exit()
else:
	print("DFT type %s not available..." % dft)
	sys.exit()

# Get the header information
head = 'Job Name: %s\n' % run_name
head += 'DFT Simmulation in %s\n' % dft
head += 'Energy Data Points: %d\n' % len(data.energies)
if len(data.energies) > 2:
        Ener = str(units.convert_energy(u1, u2, data.energies[-2] - data.energies[-3]))
        head += 'dE 2nd last = %s %s\n' % (Ener,u2)
if len(data.energies) > 1:
        Ener = str(units.convert_energy(u1, u2, data.energies[-1] - data.energies[-2]))
        head += 'dE last = %s %s\n' % (Ener,u2)
if len(data.energies) > 0:
        Ener = str(units.convert_energy(u1, u2, data.energies[-1]))
        head += 'Last Energy = %s %s' % (Ener,u2)
body, tail = '', ''

if data.convergence != None:
	for line in data.convergence:
		body += '\t'.join([str(s) for s in line])+'\n'
	body = utils.spaced_print(body, delim='\t')

if data.converged:
	tail = 'Job converged in %.2e seconds' % data.time
else:
	tail = 'Job has not converged.'

length = max([len(tmp) for tmp in head.split('\n')] + [len(tmp) for tmp in body.split('\n')] + [len(tmp) for tmp in tail.split('\n')])
dash = '\n'+''.join(['-']*length)+'\n'

if body != '':
        print(dash+head+dash+body+dash+tail+dash)
else:
        print(dash+head+dash+tail+dash)

try:
	if len(data.frames) > 0:
		files.write_xyz(data.frames,out_name[:-4])
		if vmd:
			os.system('"'+sysconst.vmd_path + '" ' + out_name)
except TypeError:
	print("No atomic coordinates available yet...")
except:
	print("An unexpected error has occurred.")
	sys.exit()