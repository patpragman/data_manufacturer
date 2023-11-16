import os

modes = ["--balance --random"]

for mode in modes:
    s = f"--frac 1.0"
    cmd = f"python data_manufacturer.py {s}"
    print('Running Command:', cmd)
    os.system(cmd)
