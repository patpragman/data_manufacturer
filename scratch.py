import os

modes = ["--random", "--balance --random"]

all_varieties = [
    size/100 for size in range(35, 45, 10)
]

for frac in all_varieties:
    for mode in modes:
        s = f"{mode} --frac {frac}"
        cmd = f"python data_manufacturer.py {s}"
        print('Running Command:', cmd)
        os.system(cmd)

