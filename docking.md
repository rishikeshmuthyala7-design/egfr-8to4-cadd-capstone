# Independent docking and pose visualization

I docked emetine, artemether, azadirone, nimbolide, and nicotinamide against the prepared 8TO4 chain D receptor using PyRx / AutoDock Vina, then visualized the poses. This was an independent extension to the assigned training capstone.

## Run records

| Record | Contents |
| --- | --- |
| [Prepared receptor PDBQT](../docking/8TO4_prepared.pdbqt) | Author chain D with AutoDock atom types and partial charges |
| [Vina search configuration](../docking/conf.txt) | Grid center, box dimensions, and exhaustiveness from the run |
| [Original PyRx score export](../docking/8TO4DOCK.csv) | Scores and RMSD bounds for nine poses per ligand |
| [Tidy pose scores](../docking/pose_scores.csv) | All 45 results cross-checked against the Vina remarks in the pose files |
| [Docked ligand outputs](../docking/poses/) | One multi-model PDBQT for each compound |
| [Pose 1 residue distances](../docking/pose_1_neighbors.csv) | Minimum heavy-atom distances to chain D residues within 4.0 Å |

The ligand filenames identify the PubChem CID and indicate UFF preprocessing. The archived run files establish the receptor, poses, scores, and RMSD bounds. The saved Vina configuration specifies a box centered at (7.118, −4.927, 27.006) Å with dimensions of 23.512 × 30.078 × 29.236 Å and exhaustiveness 8. The DoGSiteScorer centroid is a separate measurement from the docking box. An exact rerun would also require the prepared ligand input PDBQTs, the engine version, and the random seed.

## Scores and pose inspection

| Compound | Best Vina score (kcal/mol) | Nearest chain D residue in pose 1 |
| --- | ---: | --- |
| Nimbolide | -7.5 | ASN808 (2.81 Å) |
| Azadirone | -7.0 | TYR813 (2.93 Å) |
| Emetine | -6.9 | ARG999 (2.97 Å) |
| Artemether | -6.6 | TYR813 (2.69 Å) |
| Nicotinamide | -5.1 | GLN812 (2.88 Å) |

The upper and lower RMSD bounds in the score table report each mode's deviation from that ligand's top mode. For the residue table, the minimum distance was calculated over heavy atoms in each ligand's first model and each receptor residue, using the saved coordinates. Nimbolide's three nearest residues were ASN808 (2.81 Å), TYR813 (2.97 Å), and TYR801 (3.06 Å). These are geometric proximities. Determining hydrogen bonds would also require checking donor and acceptor identity, geometry, and protonation.

Vina ranked nimbolide highest in this five-ligand run. The score differences describe this setup. Biochemical binding or inhibition assays would be needed to test the ranking experimentally. Redocking the co-crystallized inhibitor FRF-06-057 would provide a benchmark for pose recovery in this receptor.
