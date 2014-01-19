import sys
from docopt import docopt
from statium_reformat import renumber
from statium_reformat import create_res 

def main(argv):
    
    helpdoc =   """
                usage: statium_wrapper.py renumber (IN_PDB) [OUT_PDB] [-v | --verbose]
                       statium_wrapper.py create_res (IN_PDB) [OUT_RES] [-v | --verbose]
                       statium_wrapper.py create_cfg (IN_RES) [-v | --verbose]
                       statium_wrapper.py run_statium (IN_CFG IN_RES IN_PDB) [-v | --verbose]
                       statium_wrapper.py calc_seq_energy (DIR SEQ) [-v | --verbose]
                       statium_wrapper.py [-h | --help]
                """
    
    options = docopt(helpdoc, argv, help = True, version = "2.0.0", options_first=False)
    
    if(options['renumber']):
        if(options['-v'] or options['--verbose']): print("Reformatting file: " + options['IN_PDB'])
        
        if(options['OUT_PDB'] == False):
            renumber(1, 1, options['IN_PDB'], options['IN_PDB'][:-4]+'_renumbered.pdb')
            if(options['-v'] or options['--verbose']): print("Done. Formatted file: " + options['IN_PDB'][:-4]+'_renumbered.pdb')
            
        else:
            renumber(1, 1, options['IN_PDB'], options['OUT_PDB'])
            if(options['-v'] or options['--verbose']): print("Done. Formatted file: " + options['OUT_PDB'])
        
    elif(options['create_res']):
        if(options['-v'] or options['--verbose']): print("Creating .res file for: " + options['IN_PDB'])
        
        if(options['OUT_RES'] == False):
            create_res(1, 1, options['IN_PDB'], options['IN_PDB'][:-4]+'_renumbered.pdb')
            if(options['-v'] or options['--verbose']): print("Done. .res file: " + options['IN_PDB'][:-4]+'.res')
            
        else:
            create_res(1, 1, options['IN_PDB'], options['OUT_PDB'])
            if(options['-v'] or options['--verbose']): print("Done. .res file: " + options['OUT_RES'])
        
    elif(options['run_statium']):
        if(options['-v'] or options['--verbose']): print("Running STATIUM with: " + options['IN_CFG'] + " " + options['IN_RES'] + " " + options['IN_PDB'])
        
    elif(options['calc_seq_energy']):
        if(options['-v'] or options['--verbose']): print("Calculating energy for sequence: " + options['SEQ'] + " with STATIUM output directory " + options['DIR'])
        
if __name__ == "__main__":
    main(sys.argv[1:])