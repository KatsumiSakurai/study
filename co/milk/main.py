import pulp
from pulp.pulp import LpConstraint, LpVariable


def main():
    data = {
        'エスプレッソアイス': { '牛乳': 100, '作業時間': 7, '儲け': 250 },
        'ラズベリーアイス': { '牛乳': 150, '作業時間': 5, '儲け': 300 },
    }

    v = {}
    for k in data.keys():
        v[k] = pulp.LpVariable(f'v_{k}', lowBound=0, cat=pulp.LpInteger)

    problem = pulp.LpProblem("アイス生産問題", pulp.LpMaximize)
    problem += pulp.lpSum([v[x] * data[x]['儲け'] for x in data.keys()])
    problem += pulp.lpSum([v[x] * data[x]['牛乳'] for x in data.keys()]) <= 8000
    problem += pulp.lpSum([v[x] * data[x]['作業時間'] for x in data.keys()]) <= 360
    solver = pulp.PULP_CBC_CMD(msg=False)
    result = problem.solve(solver)

    print(pulp.value(result))

    if result == pulp.LpStatusOptimal:
        print(pulp.value(problem.objective))
        for k in data.keys():
            print(pulp.value(v[k]))


if __name__ == '__main__':
    main()
