import sys

from ggakey import energy

if sys.argv[1] == 'b3lypg':
    gga1 = 'hf=.2 vwn3i=0.19 lyp=0.81 becke=0.72 slater=0.8'.split()
else:
    gga1 = sys.argv[1].split()
gga2 = sys.argv[2].split()

e1 = energy(gga1, 'heh')
e2 = energy(gga2, 'heh')

print(f"({gga1})-({gga2})", e1-e2)
