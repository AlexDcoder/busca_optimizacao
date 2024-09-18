from utils.gen import AlgoGenCont


# Cromossomo canônico
gen1 = AlgoGenCont(10, 20, 5, -10, 10, 0.85)

# Cromossomo não canônico
gen2 = AlgoGenCont(10, 20, 5, -10, 10, 0.85, False, 2)

for i in range(100):
    gen1.execute()
    gen2.execute()
