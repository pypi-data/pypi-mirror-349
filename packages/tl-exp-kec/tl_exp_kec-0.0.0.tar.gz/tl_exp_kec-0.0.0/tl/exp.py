from .experiments import exp1, exp2, exp3, exp4, exp5, exp6, exp7, exp8, exp9, exp10

def exp(n):
    experiments = {
        1: exp1.run,
        2: exp2.run,
        3: exp3.run,
        4: exp4.run,
        5: exp5.run,
        6: exp6.run,
        7: exp7.run,
        8: exp8.run,
        9: exp9.run,
        10: exp10.run,
    }

    if n not in experiments:
        raise ValueError("Invalid experiment number")
    
    experiments[n]()
