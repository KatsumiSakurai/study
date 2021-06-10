import pulp


def main():
	flow = [
		[0, 15, 12, 8, 7],
		[15, 0, 14, 2, 4],
		[12, 14, 0, 6, 6],
		[8, 2, 6, 0, 11],
		[7, 4, 6, 11, 0]
	]
	dist = [
		[0, 4, 7, 6, 10],
		[4, 0, 2, 5, 4],
		[7, 2, 0, 8, 7],
		[6, 5, 8, 0, 12],
		[10, 4, 7, 12, 0]
	]
	N = 5
	M = 5

	v = [pulp.LpVariable(f'var_{i}_{j}', lowBound=0, upBound=1, cat=pulp.LpInteger) for i in range(N) for j in range(M)]

	problem = pulp.LpProblem("二次割当問題", pulp.LpMinimize)
	problem += pulp.lpSum([v[i*M+j] * flow[i][j] * dist[i][j] for i in range(N) for j in range(M)])
	for i in range(N):
		problem += pulp.lpSum([v[i*M+j]] for j in range(M)) == 1
		problem += v[i*M+i] == 0
	for j in range(M):
		problem += pulp.lpSum([v[i*M+j]] for i in range(N)) == 1

	result = problem.solve()

	if result == pulp.LpStatusOptimal:
		print(pulp.value(problem.objective))

		for i in range(N):
			for j in range(M):
				if v[i * M + j].value() == 1:
					print(i, j)

if __name__ == '__main__':
	main()
