import cPickle as pickle
from merlin import *

def test_xyz_cml():
	molecule = utils.Molecule('acetone')
	atoms = files.read_xyz('PbCl_24')
	for filetype in ['xyz', 'cml']:
		if os.path.isfile('out.'+filetype): os.remove('out.'+filetype)
		if filetype=='xyz': files.write_xyz(atoms)
		else: files.write_cml(molecule)
		if open('out.'+filetype).read() != open('target_out.'+filetype).read():
			raise Exception(filetype+' filetype test failed')

def test_orca():
	result = orca.read('PbCl2_0_vac')
	target_result = pickle.load(open('orca.pickle'))
	if result.energy != target_result.energy:
		raise Exception('Wrong orca energy: %f vs %f' % (result.energy, target_result.energy))

def test_files():
	os.chdir('unit_tests/test_files')
	test_xyz_cml()
	test_orca()
	os.chdir('..')

test_files()

print "All pre-commit tests succeeded"

