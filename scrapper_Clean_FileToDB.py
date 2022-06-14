import datetime
import re
import pandas as pd


data = datetime.datetime.now()
checaDia = data.day
checaMes = data.month
diaMes = str(checaDia) + "_" + str(checaMes) + ".csv"
filename = "Scrapper " + diaMes
df = pd.read_csv(filename, encoding='latin-1')


pat = re.compile(r'^[^a-zA-Z]+|[\"*?\[\'R$]|[\'\]\"]')  # regex pra selecionar os valores da str a ser trocado
check = re.compile(r'^CERVEJA')
repl = ["", "."]


def clean_dframe(df):
    df = df.replace([pat, r","], repl, regex=True)
    df['Nome'] = df['Nome'].str.upper()
    df = df.sort_values('Nome')
    df["Precos"] = round(df["Precos"].astype(float), 2)
    df = df[df["Nome"].str.contains(check)]
    df['Data'] = str(data.day) + "/" + str(data.month)
    return df


df = clean_dframe(df)
df.to_csv(path_or_buf=f"ADG_DTB {data.day}_{data.month}.csv", index=False)

df = pd.read_csv('Scrapper Pao de Ac ' + diaMes, encoding='latin-1')
df = clean_dframe(df)
df.to_csv(path_or_buf=f"PDA_DTB {data.day}_{data.month}.csv", index=False)

