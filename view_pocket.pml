# Run from the repository root with the RCSB legacy PDB saved as 8TO4.pdb.
load 8TO4.pdb, experiment
load data/pocket_p0_records.pdb, pocket_atoms
select receptor, experiment and polymer.protein and chain D
select pocket, receptor and byres (receptor in pocket_atoms)
hide everything, all
show cartoon, receptor
color gray70, receptor
show sticks, pocket
util.cbag pocket
color yellow, pocket and name C*
show spheres, pocket and resi 790 and name CA
color orange, pocket and resi 790 and name CA
bg_color white
orient pocket
zoom pocket, 7
