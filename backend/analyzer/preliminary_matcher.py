import pandas as pd

epsilon = 30
matched = False

df1 = pd.read_csv('output1.csv')
df2 = pd.read_csv('output2.csv')

points = 0

for category in list(df1):
    if category in list(df2):
        if abs(df1[category] - df2[category]) < epsilon: points = points + 1

if points >= 5:
    matched = True
