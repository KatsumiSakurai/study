import pandas as pd
import random

d = {}

d['A'] = [x for x in range(10)]
d['B'] = [x * x for x in range(10)]
d['C'] = [random.random() * x for x in range(10)]

df = pd.DataFrame(d)

print(df)
print(df.corr())