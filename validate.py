#!/usr/bin/env python3

import json
import sys

if len(sys.argv) != 2:
    print("validate.py: test output correctness and extract performance for the UK-NNSS Grid benchmark.")
    print("Usage: validate.py <result_json_file>")
    sys.exit(1)


jsonfile = sys.argv[1]

with open(jsonfile, 'r') as file:
    data = json.load(file)

valid = True

print("\n# DOLFINx benchmark validation\n")

# Get the inputs
p = data['input']['p']
ndof = data['input']['ndofs_local_requested']
nreps = data['input']['nreps']
fp = data['input']['scalar_size']
is_mat_comp = data['input']['mat_comp']
is_cg = data['input']['cg']
print(f'                   P : {p}')
print(f'                ndof : {ndof}')
print(f'               nreps : {nreps}')
print(f'         scalar size : {fp}')

if not is_mat_comp and not is_cg:
    print(f'\n  Benchmark must be run with exactly one of --mat_comp and --cg')
    valid = False

if fp != 64:
    print(f'\n  Benchmark must be run with 64-bit precision')
    valid = False

if valid and ndof == 10000 and p == 3:
    print(f'\n  ===========================================')
    print(f'  CORRECTNESS TEST CASE                      ')
    y_norm = data['output']['y_norm']
    z_norm = data['output']['z_norm']
    print(f'              y_norm : {y_norm}')
    print(f'              z_norm : {z_norm}')
    if abs(y_norm - 1.141577508) > 1e-09 or abs(z_norm - 1.141577508) > 1e-09:
        print(f'  INCORRECT VALUES REPORTED                  ')
        valid = False
    print(f'  ===========================================')

gdofs = data['output']['gdof_per_second']

if valid and is_mat_comp:
    print(f'   MAT COMP performance: {gdofs} Gflops/s')
if valid and is_cg:
    print(f'   CG performance: {gdofs} Gflops/s')

print("\n  Validation:", ("PASSED" if valid else "FAILED") )
print()

