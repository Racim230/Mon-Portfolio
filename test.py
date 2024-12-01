import pandas as pd
df = pd.read_excel('Classeur1.xlsx', engine = 'openpyxl')
n = df.columns.get_loc("Mon")
df.insert(n,"écart",0)
df.insert(n,"conversion",0)
df.insert(n,"Mon HT",0)
df = df.sort_values(['Devise'],ascending=True)
i=0
c1 = int(input("donner le taux de conversion EUR : "))
c2 = int(input("donner le taux de conversion USD : "))
for i in range(len(df)) :
    if df.iloc[i,0] == 1 :
        df.iloc[i,2] = df.iloc[i,1] / 1.19
        df.iloc[i,3] = df.iloc[i,2]
        df.iloc[i,4] = df.iloc[i,2]- 1100
    elif df.iloc[i,0] == 2 :
        df.iloc[i,2] = df.iloc[i,1] / 1.19
        df.iloc[i,3] = df.iloc[i,2] * c1
        df.iloc[i,4] = df.iloc[i,3]- 1100
    else:
        df.iloc[i,2] = df.iloc[i,1] / 1.19
        df.iloc[i,3] = df.iloc[i,2] * c2
        df.iloc[i,4] = df.iloc[i,3]- 1100
df.to_excel("resultat.xlsx", index=False)