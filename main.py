import map


mp = map.Map(50)


def question3():
    r1iterations = []
    r2iterations = []

    for i in range(100):
        mp.resetMap()
        mp.resetBelief()
        mp.resetTarget()
        t1 = mp.bayesianSearchRule1()
        mp.resetBelief()
        t2 = mp.bayesianSearchRule2()
        r1iterations.append(t1)
        r2iterations.append(t2)
        print(str(i) + ': Number of iterations: ' + str(t1) + ', ' + str(t2))


    print('Mean for Rule #1: ' + str(sum(r1iterations) / len(r1iterations)))
    print('Mean for Rule #2: ' + str(sum(r2iterations) / len(r2iterations)))

def question4():
    print(mp.bayesianSearchQ4())

question3()