import pulp
from pulp.constants import LpInteger
import numpy as np
import math
import time

x = 9
y = 10
bigM = 1000


def make_data():
    gap = 1
    data = [(i * gap, j * gap) for j in range(y) for i in range(x)]
    return data


def main():
    data = make_data()

    # 距離テーブルを作成する
    dist = np.zeros((x * y, x * y))
    for i in range(x * y):
        for j in range(x * y):
            dist[i, j] = math.sqrt((data[i][0] - data[j][0])**2 + (data[i][1] - data[j][1])**2)

    v = [pulp.LpVariable(f'var_{i}_{j}', lowBound=0, upBound=1, cat=LpInteger) for i in range(x) for j in range(y)]

    problem = pulp.LpProblem('ソーシャルディスタンス', pulp.LpMaximize)

    # 目的：椅子の数を最大にする
    problem += pulp.lpSum(v[i] for i in range(x * y))

    # 制約：椅子の間を1.4m以上空ける
    for i in range(x * y):
        for j in range(x * y):
            if i == j:
                continue
            # problem += ((2 - v[i] - v[j]) * bigM + dist[i, j]) >= 2.2
            problem += ((2 - v[i] - v[j]) * bigM + dist[i, j]) >= 3.1

    '''
    # 1列1人
    for i in range(x):
         problem += pulp.lpSum(v[j * x + i] for j in range(y)) <= 1

    # 1行1人
    for j in range(y):
         problem += pulp.lpSum(v[j * x + i] for i in range(x)) <= 1
    '''

    solver = pulp.PULP_CBC_CMD(msg=0)
    result = problem.solve(solver)

    print(pulp.LpStatus[result])

    if result == pulp.LpStatusOptimal:
        for j in range(y):
            for i in range(x):
                if v[j * x + i].value() == 1:
                    print(' o', end='')
                else:
                    print(' .', end='')
            print()
    print('椅子の個数 {} 個'.format(pulp.value(problem.objective)))


if __name__ == '__main__':
    start = time.perf_counter()
    main()
    end = time.perf_counter()
    print(f'実行時間: {end - start}')
