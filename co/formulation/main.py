import pulp


def main():
    alloy = [
        {'lead': 20, 'zinc': 30, 'tin': 50, 'cost': 7.3},
        {'lead': 50, 'zinc': 40, 'tin': 10, 'cost': 6.9},
        {'lead': 30, 'zinc': 20, 'tin': 50, 'cost': 7.3},
        {'lead': 30, 'zinc': 40, 'tin': 30, 'cost': 7.5},
        {'lead': 30, 'zinc': 30, 'tin': 40, 'cost': 7.6},
        {'lead': 60, 'zinc': 30, 'tin': 10, 'cost': 6.0},
        {'lead': 40, 'zinc': 50, 'tin': 10, 'cost': 5.8},
        {'lead': 10, 'zinc': 30, 'tin': 60, 'cost': 4.3},
        {'lead': 10, 'zinc': 10, 'tin': 80, 'cost': 4.1},
    ]
    N = len(alloy)

    v = [pulp.LpVariable(f'var_{i}', lowBound=0, cat=pulp.LpContinuous) for i in range(N)]

    problem = pulp.LpProblem("配合問題", pulp.LpMinimize)
    problem += pulp.lpSum([v[x] * alloy[x]['cost'] for x in range(N)])
    problem += pulp.lpSum([v[x] * alloy[x]['lead'] for x in range(N)]) == 30
    problem += pulp.lpSum([v[x] * alloy[x]['zinc'] for x in range(N)]) == 30
    problem += pulp.lpSum([v[x] * alloy[x]['tin'] for x in range(N)]) == 40

    solve = problem.solve()
    if solve == pulp.LpStatusOptimal:
        print(pulp.value(problem.objective))
        for i in v:
            print(i.value())

if __name__ == '__main__':
    main()
