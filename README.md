<b>STATIUM: smart scoring. promising proteins.</b><br>
STATIUM is an ongoing project at the Keating Lab to quantitatively understand favorable protein-protein interactions. This repository contains a user-friendly implementation of the structure-based statistical-potential STATIUM algorithm that scores how well two or more proteins bind at their interacting positions. Specifically, STATIUM scores how well a certain sequence would bind to another main protein structure (e.g. variable residue positions of a ligand binding to a receptor). There are three main parts of analysis with STATIUM: <br>

1. <b> Potentials calculations </b>. STATIUM first calculates energy potentials for each position in your binding sequence. `quickrun` is the simplest command that does this. If you'd like more advanced control over your arguments, use the advanced commands with more parameters (`renumber`, `create_res`, `run_statium`) <br>

2. <b>Sequence scoring </b>. Using the above potentials, the `energy` command scores the binding potential of sequence. <br>

3. <b>Miscellaneous </b>. Finding sequences with lowest STATIUM binding energy (`calc_top_seqs`). Plotting ROC curve given STATIUM energies and experimentally determined binding classifications (`roc`).

For more information on the mechanics of STATIUM's analysis, please refer to the paper http://dx.doi.org/10.1016/j.jmb.2012.05.022

***
<b>Installation</b><br>
If you are on a 'nix machine with `git` installed obtaining STATIUM and all its data should be as simple as: `git clone https://github.com/skoppula/statium.git` to obtain all necessary files and running `./install.sh`.

***
<b>Quickstart!</b><br>
If you, for example, wanted to score sequences for chain B of some protein described in 1YCR.pdb, you could run:<br>
1. `python wrapper.py quickrun --in_pdb=1YCR.pdb --position_pairs=B --lib=data/` to calculate potentials<br>
2. `python wrapper.py energy --in_pdb=1YCR.pdb --probs_dir=1YCR --in_seqs=AMLTGTMMXX<br>` to score a sequence<br>

***
<b>1. Potentials calculation</b>: <i>Quick commands</i><br>
<b>`quickrun`</b>:<br>
<i>Template</i> `python wrapper.py quickrun (--in_pdb --position_pairs --lib) [--out]`<br>

<i>Example</i> `python wrapper.py quickrun --in_pdb=1mph_HLA.pdb --position_pairs=H31-56,L --lib=dists/ --out_dir=testing/1mph_HLA.out` <br>

Generates residue potentials required for sequence scoring. `--in_pdb` identifies the structure whose sequence you want to analyze. The --position_pairs argument specifies which set of positions to be included as binder/ligand sequences in the STATIUM analysis. The argument is a set of comma seperated terms which represent continuous sequence of residues to be included in the ligand sequence (inclusive). If you want the entirety of a chain, simply put the name of chain in the list (e.g. --position_pairs=H). In the first example above, residues on the L chain, position 1-20, and a residue on the H chain, position 33 will be included in the output residues file.

`--lib` should recieve the directory with the 20 library files with inter-atomic distances, one for each amino acid (provided in the `data` folder or output from `preprocess`). The files containing output residue potentials are placed into the `--out_dir` argument. Note that this is the same as running `renumber`, `create_res`, and `run_statium` with appropriate (default) parameters.<br>

<i>Dependencies</i>: `fsolve` from `scipy.optimize` if there are glycine residues in any of the interacting pair positions
***
<b>1. Potentials calculation</b>: <i>Advanced commands</i><br>
<b>`renumber`</b>:<br>
<i>Template</i> `python wrapper.py renumber (--in_pdb) [--out_pdb --SRN --SAN --chains]`<br>

<i>Example</i> `python wrapper.py renumber --in_pdb=testing/1mph_HLA.pdb --out_pdb=testing/1mph_AHL.pdb --chains=H,L` <br>

<i>Specifics</i>: Takes a PDB file, strips away the meta-data, and renumbers the residues and atoms, retaining atom coordinate positions and removing the occupancy and temperature factors. Renumbering starts on the first valid line of the PDB file, at starting atom number = SAN and starting residue number = SRN. 'Valid line' is any PDB line with 'ATOM' or 'HETATM' with 'MSE' (selenomethionine).

One requirement of STATIUM as implemented here is that the input PDB has the receptor sequence listed before the peptide/mutant binder sequences in the file. The `renumber` function outputs a PDB that follows this requirement by reading the chains you wish to designate as the ligand sequence from the --chains option. In the example above, the heavy and light chain that we want to mutate were pushed after chain A (*HLA to *AHL).<br>

<b>`create_res`</b>:<br>
<i>Template</i> `python wrapper.py create_res (--in_pdb_orig --in_pdb_renum) [--out_res --position_pairs]`<br>

<i>Example</i> `python wrapper.py create_res --in_pdb_orig=testing/1mph_AHL_orig.pdb --in_pdb_renum=testing/1mph_AHL_renum.pdb --out_res=testing/1mph_AHL.res --position_pairs=L1-20,H33`<br>
<i>Example 2</i> `python wrapper.py create_res --in_pdb_orig=testing/1mph_AHL_orig.pdb --in_pdb_renum=testing/1mph_AHL_renum.pdb --out_res=testing/1mph_AHL.res --position_pairs=H`<br>

<i>Specifics</i>: Takes in both the original and renumbered PDB files (see 'renumber'). It translates pairs of (chain identifier, number) uniquely demarcating a residues on the original PDB file to a number uniquely demarcating a residue in the renumbered file. These set of numbers are written to a file and used as the positions to be analyzed by the STATIUM algorithm.

The --position_pairs argument specifies which the set of positions to be included as binder/ligand sequences in the STATIUM analysis. The argument is a set of comma seperated terms which represent continuous sequence of residues to be included in the ligand sequence (inclusive). If you want the entirety of a chain, simply put the name of chain in the list (e.g. --position_pairs=H). In the first example above, residues on the L chain, position 1-20, and a residue on the H chain, position 33 will be included in the output residues file.

If you fail to include a --position_pairs argument, the function will assume you mean to create a *.res file with the entirety of chain <i>B</i>.<br>

<b>`preprocess`</b>:<br>
<i>Template</i> `python wrapper.py preprocess (--in_dir) [--out_dir --preprocess_type --ip_dist_cutoff --correct]`<br>

<i>Example</i> `python wrapper.py create_res --in_pdb_orig=testing/1mph_AHL_orig.pdb --in_pdb_renum=testing/1mph_AHL_renum.pdb --out_res=testing/1mph_AHL.res --position_pairs=L1-20,H33`<br>

<i>Specifics</i>: Takes a directory containing PDB files and processes the directory to create a inter-atomic distance library suitable for the `quickrun` or `run_statium` function.

`preprocess_type` can be one of five values, depending on what type of library you want to create (one for each term in STATIUM): `long_fixed_variable`, `short_fixed_variable`, `long_variable_variable`, `short_variable_variable` and `all`. Long in the name denotes modeling long-range interactions. Short denotes short-range interactions, between fixed and/or variable residues.

Note that currently, STATIUM defaults to not including the backbone N and C2 atoms, and only considers all of each residue's sidechain atoms instead of the subset of key atoms defined in the `get_sidechain_atoms` function in `util.py` (you may use the untested parameters `--backbone` and `--nofilter` to include backbone atoms, and not filter any atoms, respectively).

<b>`run_statium`</b>:<br>
<i>Template</i> `python wrapper.py run_statium (--in_pdb --in_res --lib)  [--out --ip_dist_cutoff --matching_res_dist_cutoffs --counts]`<br>

<i>Example</i> `python wrapper.py run_statium --in_pdb=testing/1mhp_AHL_new.pdb --in_res=testing/1mhp_AHL.res --lib=data/` <br>

<i>Specifics</i>: Takes in a renumbered PDB file (see `renumber`), the directory of the library PDBs (`--pdb_lib`) and IPs (`--ip_lib`).

Optional parameters include: `--out_dir` (the directory where STATIUM outputs its results; default value is value of `--in_pdb` without the .pdb extension), `--counts` (whether to print out STATIUM's intermediate analysis outputs; note that this takes no argument; simply including the flag issues printing!), `--ip_dist_cutoff` (the threshold distance in Angstroms between two atoms, below which the atom's residues are deemed 'interacting'; default is 6.0).

`--optimize_match_res_cutoff` is a parameter that defaults to 100 and allows us to vary the threshold by which we deem a RMSD between the `--in_pdb` and library protein as 'matching'. STATIUM finds the minimum RMSD threshold that results in the parameter specified number of matches. Alternatively, you leave the aforementioned parameter out and specify `--matching_res_dist_cutoff` (a dictionary with all twenty amino acids [in single character representation] each mapped to a constant RMSD threshold). Example [the default]: `--matching_res_dist_cutoff={'A':0.2, 'C':0.4, 'D':0.4, 'E':0.4, 'F':0.4, 'G':0.2, 'H':0.4, 'I':0.4, 'K':0.4, 'L':0.4, 'M':0.4, 'N':0.4, 'P':0.4, 'Q':0.4, 'R':0.4, 'S':0.4, 'T':0.4, 'V':0.4, 'W':0.4, 'Y':0.4}`

`--lib` should recieve the directory with the 20 library files with inter-atomic distances, one for each amino acid (provided in the `data` folder or output from `preprocess`). The files containing output residue potentials are placed into the `--out_dir` argument. Note that this is the same as running `renumber`, `create_res`, and `run_statium` with appropriate parameters.<br>

Note that currently, STATIUM defaults to not including the backbone N and C2 atoms, and only considers all of each residue's sidechain atoms instead of the subset of key atoms defined in the `get_sidechain_atoms` function in `util.py` (you may use the untested parameters `--backbone` and `--nofilter` to include backbone atoms, and not filter any atoms, respectively).

The function creates a file with twenty probabilities (one for each possible amino acid) per interacting pair, describing how likely it is for that identity would exist at that position on the sidechain, given the main chain's amino acid identity at the position.<br>

<i>Dependencies</i>: `fsolve` from `scipy.optimize` if there are glycine residues in any of the interacting pair positions
***
<b>2. Sequence scoring</b>: <i>Quick commands</i><br>
<b>`energy`</b>:<br>
<i>Template</i> `python wrapper.py energy (--in_res | --in_pdb) (--in_probs) [-f] (--in_seqs) [--out --short_intrapep --long_intrapep] [-z | --zscores] [--histogram]`<br>
<i>Example One</i> `python wrapper.py --in_res=testing/1mhp_AHL.res --in_probs=testing/1mhp_AHL.probs --in_seqs=AAAGGGM,LLAA -z --histogram='hist.jpg'`<br>
<i>Example Two</i> `python wrapper.py --in_res=testing/1mhp_AHL.res --in_probs=testing/1mhp_AHL.probs -f --in_seqs=testing/seqs.txt`<br>

<i>Specifics</i>: Calculates STATIUM's binding score for a given sequence of amino acids in the positions listed in the input *.res file (see `create_res` or `quick_run`)*. The `--in_probs` input is the STATIUM probabilities directory computed in `run_statium`. The presence of `-f` indicates that `--in_seqs` is a file (else just [possibly a set of] sequences, corresponding to the chains/position-pairs used to create the *.res file). For example, you might have a --in_seqs=AAA,L if your `--position_pairs` argument in `create_res` was 10-12,13 (note that an in_seqs without a comma is also acceptable: e.g. AAAL). A file would contain similarly formatted argument, one sequence (set) on each line.

`--short_intrapep` and `--long_intrapep` are arguments to weight the scores from these computations, relative to a weight of '1' for peptide-receptor scores.

`--out` specifies an output file. If this is option is left out, results will be printed to the console. The presence of the z-score flags finds the z-scores of the input sequences' energy on a distribution of random sequences. The presence of the `--histogram=X` saves a histogram of the random distribution of scores generated for use in z-score calculations.

If you wish to adjust the number of random sequences in the distribution, you can modify the `generate_random_distribution` function. Currently, 100,000 random-sequence scores are used to create the distribution.

*The alternative argument to `--in_res`, `--in_pdb`, still requires a *.res file to be present (with the same base file name as the PDB file).

<i>Dependencies</i>: `matplotlib.pyplot` and `numpy` in order to use `--histogram`
***
<b>3. Miscellaneous</b>: <i>Quick commands</i><br>
<b>`calc_top_seqs`</b><br>
<i>Template</i> `python wrapper.py calc_top_seqs (--in_res --in_probs --N) [--out]`<br>
<i>Example</i> `python wrapper.py calc_top_seqs --in_probs=testing/1mph_AHL_probs --out=testing/top_100_seqs.txt --N=100`

<i>Specifics</i>: Calculates the top `N` sequences with the lowest STATIUM energies (best predicted binders). `--in_probs` is the output of the `run-statium` function and `--in_res` the *.res file produced by `create_res`.<br>

<b>`roc`</b><br>
<i>Template</i> `python wrapper.py roc (--scores --true) [--curve --auroc]`<br>
<i>Example</i> `python wrapper.py roc --scores=testing/energies.txt --true=testing/true-classification.txt --auroc=testing/auroc.txt --curve=testing/roc-curve.png`<br>

<i>Specifics</i>: Given a file (output of `energy`) with containing ligand sequences and their energies (`--scores`), a file with those sequences' true binding classification as strong, weak, or inconclusive (`--true`), outputs the corresponding ROC curve (if `--curve` is listed with an output file path) and/or the AUROC (if `--auroc` is listed with an output file path).<br>

<i>Dependencies</i>: `matplotlib` for plotting ROC curves<br>
***
<b>3. Miscellaneous</b>: <i>Advanced commands</i><br>
<b>`print_merged`</b><br>
<i>Template</i> `python wrapper.py print_merged (--scores --true) [--out]`<br>
<i>Example</i> `python wrapper.py print_merged --scores=testing/energies.txt --true=testing/true-classifcation.txt --out=testing/scores-and-true.txt`<br>

<i>Specifics</i>: Combines STATIUM scores and true binding classification files into one output file, with each line containing a sequence, its score, and true classification. Sequences in the scores file but not in the classification file will not appear in the file. Conversely, scores in the classification but not in the scores file will be listed as with score infinity.<br>

<b>`random`</b>:<br>
<i>Template</i> `python wrapper.py random (--seq_length --num_seqs) [--out]`<br>
<i>Example</i>`python wrapper.py random --seq_length=8 --num_seqs=10 --out=testing/random-sequences.txt`<br>

<i>Specifics</i>: Generates `--num_seqs` random sequences of '--seq_length' length. If you include a `--out=X` option, the random sequences will be printed to the specified file. Sequences are randomly drawn from the collection of all known protein sequences contained in `data/all_protein_sequences.txt'. If you choose to modify this (e.g. adjust it so that certain amino acids occur with certain frequencies, ensure that only amino acid in their character representation are present).<br>

<b>`get_orig_seq`</b>:<br>
<i>Template</i> `python wrapper.py get_orig_seq (--in_res --in_pdb_orig --in_pdb_renum)`<br>
<i>Example</i> `python wrapper.py get_orig_seq ---in_res=testing/1mph_AHL.res -in_pdb_orig=testing/1mph_AHL_orig.pdb --in_pdb_renum=testing/1mph_AHL_renum.pdb 

Reverse of the `renumber` function. From *.res file and the renumbered and original PDBs (see `renumber`) outputs the list of residues with original chain and position information.
***
<b>Helpful Hints</b>:
+ Python 2.7+ is required
+ Verbose output is turned on by default. To turn verbose output off, include the '-nv' or '--noverbose' flag.
+ Arguments wrapped in parenthesis () are required; arguments wrapped in square brackets [] are optional.
+ `python wrapper.py -h` or `python wrapper.py --help` brings up an in-console summary of program arguments. <br>
+ Make sure that all sequences you query are in the right frame as the residue positions specified in the *.res file! You can insert X's in the beginning of a sequence to shift it to the correct frame. <br>
+ The PDB libraries are named `culled_90` because they are a curated set of PDBs with at maximum ninety-percent sequence similarity.

<br>
<b>Thanks for using STATIUM! Feel free to contact skoppula@mit.edu with issues.</b>
<br>
[![BSD License](http://img.shields.io/badge/license-MIT-yellow.svg)](http://opensource.org/licenses/MIT)
