import pulp
from pulp.constants import LpStatusOptimal


def main():
    big = 1000
    forBread = {
        'X': {'X': big, 'A':  12.0, 'B':  10.0, 'C': big, 'Y': big, 'Z': big},
        'A': {'X': big, 'A': big, 'B': big, 'C':   4.0, 'Y':  11.0, 'Z': big},
        'B': {'X': big, 'A':   6, 'B': big, 'C':  11.0, 'Y': big, 'Z': big},
        'C': {'X': big, 'A': big, 'B': big, 'C': big, 'Y':   9.0, 'Z': big},
        'Y': {'X': big, 'A': big, 'B': big, 'C': big, 'Y': big, 'Z': big},
        'Z': {'X': big, 'A': big, 'B': big, 'C': big, 'Y': big, 'Z': big},
    }
    forNoodle = {
        'X': {'X': big, 'A':  11.0, 'B':  12.0, 'C': big, 'Y': big, 'Z': big},
        'A': {'X': big, 'A': big, 'B': big, 'C':   5.0, 'Y': big, 'Z': big},
        'B': {'X': big, 'A':   7.0, 'B': big, 'C':   9.0, 'Y': big, 'Z': big},
        'C': {'X': big, 'A': big, 'B': big, 'C': big, 'Y': big, 'Z':   5.0},
        'Y': {'X': big, 'A': big, 'B': big, 'C': big, 'Y': big, 'Z': big},
        'Z': {'X': big, 'A': big, 'B': big, 'C': big, 'Y': big, 'Z': big},
    }
    limit = {
        'X': {'X':   0, 'A':  15, 'B':  12, 'C':   0, 'Y':   0, 'Z':   0},
        'A': {'X':   0, 'A':   0, 'B':   0, 'C':  18, 'Y':   3, 'Z':   0},
        'B': {'X':   0, 'A':   3, 'B':   0, 'C':  10, 'Y':   0, 'Z':   0},
        'C': {'X':   0, 'A':   0, 'B':   0, 'C':   0, 'Y':  10, 'Z':  15},
        'Y': {'X':   0, 'A':   0, 'B':   0, 'C':   0, 'Y':   0, 'Z':   0},
        'Z': {'X':   0, 'A':   0, 'B':   0, 'C':   0, 'Y':   0, 'Z':   0},
    }

    city = ['X', 'A', 'B', 'C', 'Y', 'Z']

    vB = {}
    vN = {}
    for i in city:
        for j in city:
            # if forBread[j][j] == big and forNoodle[j][j] == big:
            #     continue
            vB[(i, j)] = pulp.LpVariable(f'var_b_{i}_{j}', lowBound=0, cat=pulp.LpContinuous)
            vN[(i, j)] = pulp.LpVariable(f'var_n_{i}_{j}', lowBound=0, cat=pulp.LpContinuous)

    problem = pulp.LpProblem("多品種流通問題", pulp.LpMinimize)
    problem += pulp.lpSum([vB[(i, j)] * forBread[i][j] + vN[(i, j)] * forNoodle[i][j] for i in city for j in city])

    for i in city:
        for j in city:
            problem += vB[(i, j)] + vN[(i, j)] <= limit[i][j]

    for k in city:
        if k == 'X':
            problem += pulp.lpSum([vB[(k, j)] for j in city]) == 8
            problem += pulp.lpSum([vN[(k, j)] for j in city]) == 13
        elif k == 'Y':
            problem += pulp.lpSum([vB[(i, k)] for i in city]) == 8
        elif k == 'Z':
            problem += pulp.lpSum([vN[(i, k)] for i in city]) == 13
        else:
            problem += pulp.lpSum([vB[(k, j)] - vB[(i, k)] for i in city for j in city]) == 0
            problem += pulp.lpSum([vN[(k, j)] - vN[(i, k)] for i in city for j in city]) == 0

    
    result = problem.solve()
    print(result)

    if result == pulp.LpStatusOptimal:
        print(pulp.value(problem.objective))
        for i in city:
            for j in city:
                if vB[(i, j)].value() > 0 or vN[(i, j)].value() > 0:
                    print(i, j, vB[(i, j)].value(), vN[(i, j)].value())


if __name__ == '__main__':
    main()
