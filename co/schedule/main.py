from re import sub
import pulp
import sys

from pulp.pulp import lpSum

subjects = {
    '国語': 30,
    '算数': 30,
    '理科': 20,
    '社会': 20,
    '英語': 20
}

tests = {
    '国語': [10, 20, 30],
    '算数': [10, 20, 30],
    '理科': [10, 20],
    '社会': [10, 20],
    '英語': [10, 20],
}

rooms = ['a', 'b', 'c']

days = range(30)
timeslot = range(4)


def main():
    # 変数
    # タイムスロット　6*n * 教科 5

    total_slot = sum(subjects.values())

    v = {}
    for s in subjects.keys():
        v[s] = {}
        for x in days:
            v[s][x] = {}
            for y in timeslot:
                v[s][x][y] = {}
                for r in rooms:
                    v[s][x][y][r] = pulp.LpVariable(f'var_{s}_{x}_{y}_{r}', lowBound=0, upBound=1, cat=pulp.LpInteger)

    problem = pulp.LpProblem("時間割", pulp.LpMinimize)

    problem += lpSum([v[s][x][y][r]*x for s in subjects.keys() for x in days for y in timeslot for r in rooms])

    # 各教科は必要コマ数実施
    for s in subjects.keys():
        for r in rooms:
            problem += lpSum([v[s][x][y][r] for x in days for y in timeslot]) == subjects[s]

    # 同一教科は同一コマに一つのみ
    for s in subjects.keys():
        for x in days:
            for y in timeslot:
                problem += pulp.lpSum([v[s][x][y][r] for r in rooms]) <= 1
	# 同一コマ+同一クラスは1教科のみ
    for x in days:
        for y in timeslot:
            for r in rooms:
                problem += pulp.lpSum([v[s][x][y][r] for s in subjects.keys()]) <= 1
	# クラスの一日の同一教科は２まで
    for s in subjects.keys():
        for x in days:
            for r in rooms:
                problem += pulp.lpSum([v[s][x][y][r] for y in timeslot]) <= 2


    solver = pulp.PULP_CBC_CMD(msg=False)
    result = problem.solve(solver)

    print(pulp.LpStatus[result])
    # print(pulp.value(problem.objective))

    if result == pulp.LpStatusOptimal:
        for x in days:
            print(x, end=": ")
            for y in timeslot:
                print(y, end="(")
                for r in rooms:
                    for s in subjects.keys():
                        if pulp.value(v[s][x][y][r]) == 1:
                            print(r, s, end=",")
                print(")", end=', ')
            print()


if __name__ == '__main__':
    main()
