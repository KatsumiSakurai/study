import pulp


def main():
    makeFrom = {
        'I': {'A': 2, 'B': 5},
        'II': {'A': 7, 'B': 3},
    }
    produceCost = {
        'I': 75,
        'II': 50,
    }
    stockCost = {
        'I': 8,
        'II': 7,
    }
    request = [
        {'I': 30, 'II': 20},
        {'I': 60, 'II': 50},
        {'I': 80, 'II': 90},
    ]
    material = [
        {'A': 920, 'B': 790},
        {'A': 750, 'B': 600},
        {'A': 500, 'B': 480},
    ]

    terms = [0, 1, 2]
    product = ['I', 'II']

    v = []
    vs = []
    for t in terms:
        v.append({})
        vs.append({})
        for p in product:
            v[t][p] = {}
            for s in ['p', 's']:
                v[t][p][s] = pulp.LpVariable(f'var_{t}_{p}_{s}', lowBound=0, cat=pulp.LpInteger)
                # v[t][p][s] = pulp.LpVariable(f'var_{t}_{p}_{s}', lowBound=0, cat=pulp.LpContinuous)

    problem = pulp.LpProblem("多期間計画問題", pulp.LpMinimize)

    problem += pulp.lpSum([v[t][p]['p'] * produceCost[p] for t in terms for p in product]) + pulp.lpSum([v[t][p]['s'] * stockCost[p] for t in terms for p in product])
    
    for t in terms:
        for m in ['A', 'B']:
            problem += pulp.lpSum([v[t][p]['p'] * makeFrom[p][m] for p in product]) <= material[t][m]

    for p in product:
        problem += v[0][p]['p'] - v[0][p]['s'] == request[0][p]
        problem += v[1][p]['p'] - v[1][p]['s'] + v[0][p]['s'] == request[1][p]
        problem += v[2][p]['p'] + v[1][p]['s'] == request[2][p]

    result = problem.solve()

    print(result)
    print(pulp.value(problem.objective))
    for t in terms:
        for p in product:
            for s in ['p', 's']:
                print(t, p, s, pulp.value(v[t][p][s]))


if __name__ == '__main__':
    main()
