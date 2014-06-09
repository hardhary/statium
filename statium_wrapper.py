import sys
from docopt import docopt
from statium_reformat import renumber
from statium_reformat import create_res
from statium_analysis import statium_pipeline
from statium_analysis import calc_seq_energy
from statium_reformat import get_orig_seq
from statium_reformat import generate_random_seqs
from statium_analysis import generate_random_distribution
from statium_analysis import calc_seq_zscore
from statium_analysis import calc_seq_percentile
from statium_analysis import calc_top_seqs
from statium_analysis import classify
from statium_analysis import get_confusion_matrix
from statium_analysis import calc_auroc
from statium_analysis import plot_roc_curve
from util import list2file
from util import filelines2list

def main(argv):
	
	helpdoc =   """
				usage: statium_wrapper.py precompute (--in_pdb --in_pdb_lib_dir --in_ip_lib_dir) [--out_dir]
					   statium_wrapper.py renumber (IN_PDB) [OUT_PDB] [-v | --verbose]
					   statium_wrapper.py create_res (IN_PDB_ORIG IN_PDB_RENUMBERED) [OUT_RES] [-v | --verbose]
					   statium_wrapper.py run_statium (IN_RES IN_PDB IN_PDB_LIB_DIR IN_IP_LIB_DIR) [OUT_DIR] [-v | --verbose]
					   statium_wrapper.py [-f] calc_energy (IN_RES PROBS_DIR SEQ_OR_FILE) [OUT_FILE] [--IN_PDB_ORIG=None] [-z | --zscores] [-p | --percentiles] [-v | --verbose] [-d | --draw_histogram]
					   statium_wrapper.py get_orig_seq (IN_PDB_ORIG) [-v | --verbose]
					   statium_wrapper.py [-f] generate_random_seqs (SEQ_LENGTH NUM_SEQS) [--OUT_FILE=None] [--TOTAL_PROTEIN_LIBRARY=None] [-v | --verbose]
					   statium_wrapper.py calc_top_seqs (IN_RES PROBS_DIR N) [OUT_FILE] [-v | --verbose]
					   statium_wrapper.py classify (RESULTS_FILE) [OUT_FILE] [ALPHA_THRESHOLD] [-v | --verbose]
					   statium_wrapper.py get_confusion_matrix (IN_RES CLASS_RESULTS TRUE_CLASS) [OUT_FILE] [--IN_PDB_ORIG=None] [-v | --verbose]
					   statium_wrapper.py [-i] calc_auroc (IN_RES RESULTS_FILE TRUE_CLASS) [OUT_FILE] [--IN_PDB_ORIG=None] [--CLASS_RESULTS=None] [-v | --verbose]
					   statium_wrapper.py [-i] plot_roc_curve (IN_RES RESULTS_FILE TRUE_CLASS) [--IN_PDB_ORIG=None] [--CLASS_RESULTS=None] [-v | --verbose]
					   statium_wrapper.py [-h | --help]
				"""
	
	options = docopt(helpdoc, argv, help = True, version = "2.0.0", options_first=False)
	verbose = !(options['-nv'] or options['--noverbose'])
	zscores = options['-z'] or options['--zscores']
	percentiles = options['-p'] or options['--percentiles']
	histogram = options['-d'] or options['--draw_histogram']
   
	if(options['precompute']):

		in_pdb = options['--in_pdb']
		in_ip_lib_dir = options['--in_ip_lib_dir']
		in_pdb_lib_dir = options['--in_pdb_lib_dir']
		out_dir = options['--out_dir'] if options['--out_dir'] != None else in_pdb[:-4]
		pdb_renumbered = in_pdb[:-4]+'renumbered.pdb'
		res = in_pdb[:-4]+'.res'

		if(verbose): print("Renumbering file " + in_pdb)
		renumber(1, 1, in_pdb, pdb_renumbered)
		if(verbose): print("Finished reformatting PDB file into: " + pdb_renumbered)
			
		if(verbose): print("Creating .res file to store PDB's chain B positions: ")
		create_res(in_pdb, pdb_renumbered, res)
		if(verbose): print("Finished creating .res file: " + res)

		if(verbose): print("Running STATIUM with: " + res + " " + in_pdb + " " + in_pdb_lib_dir + " " + in_ip_lib_dir)
		statium_pipeline(res, pdb_renumbered, in_pdb_lib_dir, in_ip_lib_dir, out_dir, verbose)
		if(verbose): print("Done. STATIUM probabilities in output directory: " + out_dir);
			
		(sequence, length, start, end) = get_orig_seq(options['IN_PDB'])
		print("For reference, native chain B peptide sequence is " + str(sequence) + " of length " + str(length) + " from position " + str(start) + " to " + str(end))


	if(options['renumber']):
		if(verbose): print("Reformatting file: " + options['IN_PDB'])
		
		if(options['OUT_PDB'] == None):
			renumber(1, 1, options['IN_PDB'], options['IN_PDB'][:-4]+'_renumbered.pdb')
			if(verbose): print("Done. Formatted file: " + options['IN_PDB'][:-4]+'_renumbered.pdb')
			
		else:
			renumber(1, 1, options['IN_PDB'], options['OUT_PDB'])
			if(verbose): print("Done. Formatted file: " + options['OUT_PDB'])
	
		
	elif(options['create_res']):
		if(verbose): print("Creating .res file using: " + options['IN_PDB_ORIG'] + " and " + options['IN_PDB_RENUMBERED'])
		
		if(options['OUT_RES'] == None):
			create_res(options['IN_PDB_ORIG'], options['IN_PDB_RENUMBERED'], options['IN_PDB_RENUMBERED'][:-4]+'.res')
			if(verbose): print("Done. .res file: " + options['IN_PDB_RENUMBERED'][:-4]+'.res')
			
		else:
			create_res(options['IN_PDB_ORIG'], options['IN_PDB_RENUMBERED'], options['OUT_RES'])
			if(verbose): print("Done. .res file: " + options['OUT_RES'])
	
	elif(options['run_statium']):
		
		if(verbose): print("Running STATIUM with: " + options['IN_RES'] + " " + options['IN_PDB'] + " " + options['IN_PDB_LIB_DIR'] + " " + options['IN_IP_LIB_DIR'])
		
		if(options['OUT_DIR'] == None):   
			statium_pipeline(options['IN_RES'], options['IN_PDB'], options['IN_PDB_LIB_DIR'], options['IN_IP_LIB_DIR'], options['IN_RES'][:-4], verbose)
			if(verbose): print("Done. STATIUM probabilities in output directory: " + options['IN_RES'][:-4]);
			
		else:
			statium_pipeline(options['IN_RES'], options['IN_PDB'], options['IN_PDB_LIB_DIR'], options['IN_IP_LIB_DIR'], options['OUT_DIR'], verbose)
			if(verbose): print("Done. STATIUM probabilities in output directory: " + options['OUT_DIR']);

	elif(options['calc_energy']):
		
		#solely for neat code
		in_res = options['IN_RES']
		probs_dir = options['PROBS_DIR']
		seq_or_file = options['SEQ_OR_FILE']
		outfile = options['OUT_FILE']
		
		if(verbose): print("Writing to file: ", options['-f'], ". Calculating z-score: ", options['-z'], ". Calculating percentile: ", options['-p'])
		
		if(zscores or percentiles):
			if(verbose): print('Generating random distribution of energies...')
			distribution = generate_random_distribution(in_res, probs_dir)
			if(histogram):
				if(verbose): print('Drawing histogram...')
				import matplotlib.pyplot as plt
				import numpy as np

				hist, bins = np.histogram(distribution[2], bins=50)
				width = 0.7 * (bins[1] - bins[0])
				center = (bins[:-1] + bins[1:]) / 2
				plt.bar(center, hist, align='center', width=width)
				plt.show()
			if(verbose): print('Done generating random distribution.')
					
		if(options['-f']):
			lines = filelines2list(seq_or_file)
			out_lines = []
			
			for line in lines:
				if(line != '' and line[0] != '#'):
					(energy, seq) = calc_seq_energy(in_res, probs_dir, line, options['--IN_PDB_ORIG'])
					line = seq + "\t" + str(energy)
					
					if(zscores):
						line += "\t" + str(calc_seq_zscore(distribution[3], distribution[4], energy))
					
					if(percentiles):
						line += "\t" + str(calc_seq_percentile(distribution[2], energy))
					
				out_lines.append(line)
					
			list2file(out_lines, outfile)
			print('Done.')
		
		else:
			(energy, seq) = calc_seq_energy(in_res, probs_dir, seq_or_file, options['--IN_PDB_ORIG'])
			print("Sequence energy for " + seq + " is: " + str(energy))
			
			if(zscores):
				zscore = calc_seq_zscore(distribution[3], distribution[4], energy)
				print('Z-score is ' + str(zscore))
				
			if(percentiles):
				percentile = calc_seq_percentile(distribution[2], energy)
				print('Percentile is ' + str(percentile))


	#Get the original AA sequence of chain B, along with stats like the length and position of that chain
	elif(options['get_orig_seq']):
		(sequence, length, start, end) = get_orig_seq(options['IN_PDB_ORIG'])
		print("Native chain B peptide sequence is " + str(sequence) + " of length " + str(length) + " from position " + str(start) + " to " + str(end))
	
	
	#Generate n random sequences of length j, possibly in outfile o if -f flag present
	elif(options['generate_random_seqs']):
		
		if(verbose): print("Generating " + options['NUM_SEQS'] + " random sequences of length " + options['SEQ_LENGTH'])
		sequences = generate_random_seqs(int(options['SEQ_LENGTH']), int(options['NUM_SEQS']), options['--TOTAL_PROTEIN_LIBRARY'])
		
		if(not options['-f']):
			for sequence in sequences:
				print(sequence)
		else:
			outfile = 'random_seqs.txt' if (options['--OUT_FILE'] == None) else options['--OUT_FILE']
			list2file(sequences, outfile)
			if(verbose): print("Random sequences written to " + outfile)
   
	elif(options['calc_top_seqs']):
		if(verbose): print('Calculating ' + options['N'] + ' sequences with lowest energy.')
		outfile = 'top_' + str(options['N']) + '_sequences.txt' if (options['OUT_FILE'] == None) else options['OUT_FILE']
		calc_top_seqs(options['IN_RES'], options['PROBS_DIR'], int(options['N']), outfile)
		if(verbose): print("Done. Results written to " + outfile)
	
	elif(options['classify']):
		threshold = 0.05 if options['ALPHA_THRESHOLD'] == None else float(options['ALPHA_THRESHOLD'].split('=')[1])
		if(verbose): print('Classifying ' + options['RESULTS_FILE'] + ' with dummy (i.e. not considered right now in analysis) threshold ' + str(threshold))
		outfile = 'classify_results_' + options['RESULTS_FILE'] + '_' + str(options['N']) + '.txt' if (options['OUT_FILE'] == None) else options['OUT_FILE']
		classify(options['RESULTS_FILE'], outfile, threshold)
		if(verbose): print('Done. Results in ' + outfile)
	
	elif(options['get_confusion_matrix']):
		if(verbose): print('Calculating confusion matrix for ' + options['CLASS_RESULTS'] + ' with true classifications in ' + options['TRUE_CLASS'])
		(TP, FP, TN, FN) = get_confusion_matrix(options['IN_RES'], options['CLASS_RESULTS'], options['TRUE_CLASS'], options['--IN_PDB_ORIG'])
		outfile = options['CLASS_RESULTS'] + '_confusion_matrix.txt' if (options['OUT_FILE'] == None) else options['OUT_FILE']
		out_str = 'TP: ' + str(TP) + '\t FN: ' + str(FN) + '\nFP: ' + str(FP) + '\tTN: ' + str(TN)
		out = [out_str]
		list2file(out, outfile)
		print(out_str)
		if(verbose): print('Confusion matrix written out to ' + outfile)
	
	#by default, analysis includes tentative inconclusives. the -i flag removes them from analysis 
	elif(options['calc_auroc']):
		if(verbose): print('Calculating AUROC for ' + options['RESULTS_FILE'] + ' with true classifications in ' + options['TRUE_CLASS'])
		
		class_results = options['--CLASS_RESULTS']
		if(verbose):
			if(options['-i']):
				print('Discarding tentative \'inconclusive sequences\' in ROC analysis')
			else:
				print('Including tentative \'inconclusive sequences\' in ROC analysis')
		
			  
		auroc = calc_auroc(options['IN_RES'], options['RESULTS_FILE'], options['TRUE_CLASS'], class_results, options['--IN_PDB_ORIG'])
		outfile = options['CLASS_RESULTS'] + '_auroc.txt' if (options['OUT_FILE'] == None) else options['OUT_FILE']
		list2file([str(auroc)], outfile)
		print(auroc)
		if(verbose): print('AUROC written out to ' + outfile)
		
	elif(options['plot_roc_curve']):
		if(verbose): print('Plotting ROC curve for ' + options['RESULTS_FILE'] + ' with true classifications in ' + options['TRUE_CLASS'])
		if(verbose):
			if(options['-i']):
				print('Discarding tentative \'inconclusive sequences\' in ROC analysis')
				class_results = options['--CLASS_RESULTS']
			else:
				print('Including tentative \'inconclusive sequences\' in ROC analysis')
				class_results = None
				
		plot_roc_curve(options['IN_RES'], options['RESULTS_FILE'], options['TRUE_CLASS'], class_results, options['--IN_PDB_ORIG'])
		if(verbose): print('Done.')
	
if __name__ == "__main__":
	main(sys.argv[1:])
