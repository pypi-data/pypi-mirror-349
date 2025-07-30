import sys
import subprocess
import re

dalinp = """
**DALTON
.RUN WAVE
**WAVE FUN
.DFT
GGAKey {}
*DFT INPUT
.ULTRAFINE
*ORBITAL
.MOSTART
H1DIAG
*SCF INPUT
.MAX ERR
 1
.MAX DIIS
 1
.THRESH
 .99
**END OF
"""


def energy(keys, mol):
    x = "_".join(keys)
    ggaline = " ".join(keys)
    with open(f"gga={x}.dal", "w") as f:
        f.write(dalinp.format(ggaline))

    with open(f'gga={x}.log', 'w') as foo:
        subprocess.call(f'dalton gga={x} {mol}'.split(), stdout=foo)

    with open(f"gga={x}_{mol}.out", "r") as f:
        out = f.read()
        pat = r'.*Final.*energy:\s+([-\d.]+).*'
        e = re.search(pat, out, re.M).group(1)

    return float(e)


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('gga', nargs='+', help='GGAKey entries')
    parser.add_argument('--mol', default='heh', help='mol file')

    args = parser.parse_args()
    if args.gga[0].lower() == 'b3lypg':
        args.gga = 'hf=.2 vwn3i=0.19 lyp=0.81 becke=0.72 slater=0.8'.split()

    x = '_'.join(args.gga)
    print(x, energy(args.gga, args.mol))
