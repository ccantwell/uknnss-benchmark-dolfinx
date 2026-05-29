#!/usr/bin/env python3

import json
import sys


# Parse console output
def parse_output( json_fname, console_fname ):
    # Create dictionary for parsed values 
    d = dict()

    # Parse console file
    d['re'] = None
    f = open( console_fname, 'r' )
    for l in f:
        if("Relative norm of error = " in l ):
            s = l.split()
            d['re'] = float(s[5])
    f.close()
 
    # Parse JSON output file
    with open(json_fname, 'r') as file:
        data = json.load(file)
    # Get the inputs
    d['p'] = data['input'].get('p', None)
    d['ndof'] = data['input'].get('ndofs_local_requested', None)
    d['nreps'] = data['input'].get('nreps', None)
    d['fp'] = data['input'].get('scalar_size', None)
    d['is_mat_comp'] = data['input'].get('mat_comp', False)
    d['is_cg'] = data['input'].get('cg', False)
    d['gdofs'] = data['output'].get('gdof_per_second', None)
    d['y_norm'] = data['output'].get('y_norm', None)
    d['z_norm'] = data['output'].get('z_norm', None)

    return d

# ------------------------------------

if len(sys.argv) != 3:
    print("validate.py: test output correctness and extract performance for the UK-NNSS DOLFINx benchmark.")
    print("Usage: validate.py <result_json_file> <console_output_file>")
    sys.exit(1)


jsonfile = sys.argv[1]
consolefile = sys.argv[2]

d = parse_output(jsonfile, consolefile)

valid = True

print("\n# DOLFINx benchmark validation\n")

print(f'                    P : {d["p"]}')
print(f'                 ndof : {d["ndof"]}')
print(f'                nreps : {d["nreps"]}')
print(f'          scalar size : {d["fp"]}')

if not d["is_mat_comp"]:
    print(f'\n  ERROR: Benchmark must be run with --mat_comp')
    valid = False

if d["fp"] != 64:
    print(f'\n  ERROR: Benchmark must be run with 64-bit precision')
    valid = False

if d["nreps"] < 100:
    print(f'\n  ERROR: nreps too small, please run with at least 100')
    valid = False

if d['re'] is None:
    print("Error: could not find relative norm of error in {:}".format(
        consolefile ) )
    print("       should have found \"Relative norm of error =  \"" )
    valid = False
    
if valid and d["ndof"] == 10000 and d["p"] == 3:
    print(f'\n  ===========================================\n')
    print(f'  CORRECTNESS TEST CASE                      ')
    print(f'              y_norm : {d["y_norm"]}')
    print(f'              z_norm : {d["z_norm"]}')

    if d["is_cg"]:
        if abs(d["y_norm"] - 167.5924472) > 1e-07 or abs(d["z_norm"] - 167.5924472) > 1e-07:
            print(f'  ERROR: incorrect y_norm and z_norm values reported '
                  'for CG test')
            valid = False
    else:
        if abs(d["y_norm"] - 1.141577508) > 1e-09 or abs(d["z_norm"] - 1.141577508) > 1e-09:
            print(f'  ERROR: incorrect y_norm and z_norm values reported '
                  'for mat_comp test')
            valid = False
    print(f'\n  ===========================================')

if valid:
    if d["is_cg"]:
        if abs(d["re"]) > 1e-12:
            print(f'   Relative error norm too large: {d["re"]}')
            valid = False
    else:
        if abs(d["re"]) > 1e-14:
            print(f'   Relative error norm too large: {d["re"]}')
            valid = False

if d["is_cg"] and valid:
    print(f'\n  CG performance: {d["gdofs"]} Gdofs/s')
else:
    print(f'\n  MAT COMP performance: {d["gdofs"]} Gdofs/s')

print("\n  Validation:", ("PASSED" if valid else "FAILED") )
print()

