from Bio.PDB import PDBParser, PDBIO, Superimposer
from Bio.PDB.Structure import Structure 
from copy import deepcopy

parser = PDBParser()

structure = parser.get_structure('initial', '../PDBFiles/1NEW_1PED_fitted_one_domain.pdb')
result = Structure('result')

#ranges = list(range(3, 111)) + list(range(261, 313)) + list(range(328, 334)) + list(range(389, 403))

#3- 110A, 261- 312A, 328- 333A
#def interpolate(initial, final, indexes, steps, startEndInclusive):
def interpolate(initial, final, steps, startEndInclusive):
	if startEndInclusive:
		yield initial	

	newModel = deepcopy(initial)

	for index in range(1, steps+1):
		newModel.id = index
		#iteration = -1

		for chain, chain2, chain3 in zip(initial, final, newModel):
			for residue, residue2, residue3 in zip(chain, chain2, chain3):
				for atom, atom2, atom3 in zip(residue, residue2, residue3):
					#iteration = iteration + 1

					#if (iteration not in ranges):
						#continue

					# The distances between each point's coordinates in cartasian space
					xDistance = abs(atom.coord[0] - atom2.coord[0])
					yDistance = abs(atom.coord[1] - atom2.coord[1])
					zDistance = abs(atom.coord[2] - atom2.coord[2])
					intervals = steps + 1

					xDistancePerStep = xDistance / intervals
					yDistancePerStep = yDistance / intervals
					zDistancePerStep = zDistance / intervals

					if atom.coord[0] < atom2.coord[0]:
						atom3.coord[0] += xDistancePerStep
					elif atom.coord[0] > atom2.coord[0]:
						atom3.coord[0] -= xDistancePerStep

					if atom.coord[1] < atom2.coord[1]:
						atom3.coord[1] += yDistancePerStep
					elif atom.coord[1] > atom2.coord[1]:
						atom3.coord[1] -= yDistancePerStep	

					if atom.coord[2] < atom2.coord[2]:
						atom3.coord[2] += zDistancePerStep
					elif atom.coord[2] > atom2.coord[2]:
						atom3.coord[2] -= zDistancePerStep

		yield newModel

	if startEndInclusive:
		final.id = steps + 1

		yield final

for model in interpolate(structure[0], structure[1], 10, True):
#for model in interpolate(structure[0], structure[1], ranges, 10, True):
	result.add(deepcopy(model))

io = PDBIO()
io.set_structure(result)
io.save('out.pdb')