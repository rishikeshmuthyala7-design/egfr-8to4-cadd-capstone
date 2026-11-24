# Methods and interpretation

## Ligand screening

I collected PubChem CIDs and SMILES for emetine, artemether, azadirone, nimbolide, and nicotinamide, submitted the SMILES to SwissADME, and visualized compound structures in PyMOL. The capstone marks each of the four Lipinski checks as passing for all five compounds. The source table records check marks. Exact per-rule descriptor values and rotatable bond counts are unavailable in the table, so the ligand CSV preserves the reported outcomes. Lipinski compliance is a screening heuristic for oral drug-likeness.

## Receptor preparation

I started from the experimental [8TO4 entry](https://www.rcsb.org/structure/8TO4), an X-ray structure at 2.99 Å of human EGFR(T790M/V948R) in complex with FRF-06-057. The entry also contains the ATP analogue ANP and magnesium. I kept author chain D, removed the other chains and crystallographic water, removed unwanted heteroatoms, and used Chimera Dock Prep to add hydrogens and assign charges. I saved the prepared structure as `8TO4_prepared.pdb` and compared the before-and-after structures in PyMOL. The preparation log identifies Gasteiger charges. Both the [prepared PDB](../structures/8TO4_prepared.pdb) and the [docking receptor PDBQT](../docking/8TO4_prepared.pdbqt) are archived. Their coordinate records contain only protein atoms from author chain D.

In RCSB's entity table the protein instance labeled A has author chain D. The legacy PDB chain identifier and the pocket export both use the author chain identifier D.

## Predicted pocket

I submitted the experimental structure to DoGSiteScorer and selected author chain D. The capstone records pocket P_0 with a volume of 1,330.37 Å³, surface area of 1,923.72 Å², and druggability score of 0.81.

The [pocket export records](../data/pocket_p0_records.pdb) contain 304 atom records from 59 unique residues. The residue table was generated from the PDB chain, residue number, insertion code, and residue name fields. The capstone's preliminary entries such as ARG 3 describe residue-type counts. Examples of real positions include ARG705, ASP770, CYS775, MET790, and MET793. Each atom count in the CSV refers to records included in the export. The header's geometric center is (6.04, 2.13, 24.17) Å. This is useful for identifying the predicted pocket in the deposited coordinate frame.

## ADMET predictions

I profiled the five SMILES in ADMETlab 3.0. The [results CSV](../data/admet_predictions.csv) transcribes the ten endpoints present in the report. Sign codes such as `---` and `++` are preserved as reported. The capstone omits units for Caco-2 permeability, half-life, and clearance. The CSV preserves the reported numbers without inferring units or converting categories.

| Compound | Predicted hERG | Predicted DILI | CYP3A4 inhibitor | BBB |
| --- | ---: | ---: | --- | --- |
| Emetine | 0.733 | 0.112 | `---` | `---` |
| Artemether | 0.228 | 0.580 | `---` | `---` |
| Azadirone | 0.248 | 0.836 | `++` | `+` |
| Nimbolide | 0.210 | 0.845 | `+++` | `--` |
| Nicotinamide | 0.168 | 0.607 | `---` | `++` |

Emetine had the highest predicted hERG signal in this panel. Azadirone and nimbolide had the highest predicted DILI values and plasma protein binding above 93%. Artemether and nicotinamide had lower relative hERG and CYP inhibition signals, alongside predicted DILI values near 0.6. These comparisons describe the model outputs for this set.

## AlphaFold 3 comparison

I submitted the [328-residue deposited sequence](../data/8to4_chain_d.fasta) to AlphaFold 3 and aligned the resulting model to prepared experimental 8TO4 chain D in PyMOL. The capstone records an RMSD of 0.965 Å and 2,289 aligned atoms. The report includes a visual observation of locally lower confidence. Quantitative pLDDT and alignment coverage by residue require the original model and confidence files. Atom selection, alignment cycles, and outlier handling affect RMSD and should be recorded when repeating the comparison.

## Sources and software

- [RCSB PDB entry 8TO4](https://www.rcsb.org/structure/8TO4) · [8TO4 validation report](https://files.rcsb.org/pub/pdb/validation_reports/to/8to4/8to4_full_validation.pdf)
- [PubChem](https://pubchem.ncbi.nlm.nih.gov/) · [SwissADME](https://www.swissadme.ch/)
- [UCSF Chimera Dock Prep](https://www.cgl.ucsf.edu/chimera/docs/ContributedSoftware/dockprep/dockprep.html) · [PyMOL](https://pymol.org/)
- [ProteinsPlus](https://proteins.plus/) · [DoGSiteScorer method](https://doi.org/10.1093/bioinformatics/bts310)
- [ADMETlab 3.0](https://admetlab3.scbdd.com/) · [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w)
- [PyRx](https://pyrx.sourceforge.io/) · [AutoDock Vina](https://vina.scripps.edu/)
