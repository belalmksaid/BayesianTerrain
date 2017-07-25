import map


mp = map.Map(50)


def question3():
    mp = map.Map(25)
    r1iterations = []
    r2iterations = []

    for i in range(1000):
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

def question4p2():
    mp = map.Map(20)
    r1iterations = []
    r2iterations = []
    r3iterations = []
    r4iterations = []

    for i in range(300):
        mp.resetMap()
        mp.resetBelief()
        mp.resetTarget()
        t1 = mp.bayesianSearchRule1()
        mp.resetBelief()
        t2 = mp.bayesianSearchRule2()
        mp.resetBelief()
        t3 = mp.bayesianSearchQ4()
        r1iterations.append(t1)
        r2iterations.append(t2)
        r3iterations.append(t3[0])
        r4iterations.append(t3[1])
        print(str(i) + ': Number of iterations: ' + str(t1) + ', ' + str(t2) + ', ' + str(t3[0]) + ', ' + str(t3[1]))


    print('Mean for Rule #1: ' + str(sum(r1iterations) / len(r1iterations)))
    print('Mean for Rule #2: ' + str(sum(r2iterations) / len(r2iterations)))
    print('Mean for Moves: ' + str(sum(r3iterations) / len(r3iterations)))
    print('Mean for Visits: ' + str(sum(r4iterations) / len(r4iterations)))

question4p2()