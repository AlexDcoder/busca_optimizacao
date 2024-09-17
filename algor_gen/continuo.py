from utils.gen import AlgoGenCont
from pprint import pprint
import numpy as np

# Cromossomo canônico
# gen1 = AlgoGenCont(10, 20, 5, -10, 10, 0.85)
# pprint(gen1.population[0])
# pprint(gen1.phi(np.split(gen1.population[0, :], gen1.nd)))
# Cromossomo não canônico
gen2 = AlgoGenCont(10, 20, 5, -10, 10, 0.85, False, 2)
pprint(gen2.torneio())

# for i in range(100):
#     # gen1.execute()
#     gen2.execute()
