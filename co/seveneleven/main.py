import pandas as pd
import pulp


class MyOptimize:
    def __init__(self):
        self.df = self.load()

        self.N = len(self.df)
        self.names = self.df['商品名'].tolist()
        self.prices = self.df['税込価格'].tolist()
        self.calorie = self.df['カロリー'].tolist()

    def load(self):
        df = pd.read_csv('data.csv')
        df['税込価格'] = df['メニュー名（税込価格）'].replace('.*[(（]([0-9]*)円[)）]', r'\1', regex=True).astype(int)
        df['商品名'] = df['メニュー名（税込価格）'].replace('[(（][0-9]*円[)）]', '', regex=True)
        df = df.drop(['メニュー名（税込価格）', 'タンパク質', '脂質', '糖質'], axis=1)
        return df

    def optimize(self, price):
        # 変数定義
        x = [pulp.LpVariable(f'var_{x}', lowBound=0, upBound=1, cat=pulp.LpInteger) for x in range(self.N)]

        problem = pulp.LpProblem('カロリー最大化', sense=pulp.LpMaximize)
        problem += pulp.lpSum([x[i] * self.calorie[i]] for i in range(self.N))
        problem += pulp.lpSum([x[i] * self.prices[i]] for i in range(self.N)) <= price

        # solver = pulp.COIN_CMD(msg=0)
        solver = pulp.PULP_CBC_CMD(msg=0, mip=1)
        solve = problem.solve(solver)
        print(pulp.LpStatus[solve])
        print('objective value = {}'.format(pulp.value(problem.objective)))
        if solve == pulp.LpStatusOptimal:
            y = [i for i in x if i.value() == 1]
        total_price = 0
        total_calorie = 0
        for yy in y:
            _, i = str(yy).split('_')
            i = int(i)
            print(f'{self.names[i]}:\t{self.prices[i]}円:\t{self.calorie[i]}Kcal')
            total_price += self.prices[i]
            total_calorie += self.calorie[i]
            print(f'TOTAL\t\t{total_price}円:\t{total_calorie}Kcal')


def main():
    mo = MyOptimize()
    #for p in range(100, 900, 100):
    #    mo.optimize(p)
    mo.optimize(500)


if __name__ == '__main__':
    main()
