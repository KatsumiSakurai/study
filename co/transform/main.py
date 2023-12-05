import pulp


def main():
    suply = [250, 350]
    request = [200, 200, 200]
    cost = [
        [3.4, 2.2, 2.9],
        [3.4, 3.4, 2.5]
    ]
    v = [pulp.LpVariable(f'var_{i}_{j}', lowBound=0, cat=pulp.LpContinuous) for i in range(len(suply)) for j in range(len(request))]

    problem = pulp.LpProblem("輸送問題", pulp.LpMinimize)
    problem += pulp.lpSum([v[i*len(request)+j] * cost[i][j] for i in range(len(suply)) for j in range(len(request))])
    for i in range(len(suply)):
        problem += pulp.lpSum([v[i*len(request)+j] for j in range(len(request))]) <= suply[i]
    for j in range(len(request)):
        problem += pulp.lpSum([v[i*len(request)+j] for i in range(len(suply))]) == request[j]

    
    result = problem.solve()
    if result == pulp.LpStatusOptimal:
        print(pulp.value(problem.objective))
        for i in range(len(suply)):
            for j in range(len(request)):
                print(i, j, v[i*len(request)+j].value())



if __name__ == '__main__':
    main()
