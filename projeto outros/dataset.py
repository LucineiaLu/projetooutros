import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Carregar o dataset
url = "https://www.kaggle.com/datasets/joaoassaoka/taxas-de-rendimento-escolar-inep?select=Taxas_de_Rendimento_Escolar_2013_2023.csv"
df = pd.read_csv("Taxas_de_Rendimento_Escolar.csv")

# Filtrar apenas o ano de 2023 e os estados desejados
estados_selecionados = ["Minas Gerais", "Rio de Janeiro", "São Paulo"]
df_2023 = df[(df["Ano"] == 2023) & (df["Unidade_Geográfica"].isin(estados_selecionados))]

# Verificar as primeiras linhas
print(df_2023.head())

import seaborn as sns
import matplotlib.pyplot as plt

# Criar gráfico de barras
plt.figure(figsize=(10, 6))
sns.barplot(x="Unidade_Geográfica", y="Taxa de Aprovação", data=df_2023, color="green", label="Aprovação")
sns.barplot(x="Unidade_Geográfica", y="Taxa de Reprovação", data=df_2023, color="red", label="Reprovação")
sns.barplot(x="Unidade_Geográfica", y="Taxa de Abandono", data=df_2023, color="blue", label="Abandono")

plt.title("Comparação das Taxas de Aprovação, Reprovação e Abandono (2023)")
plt.xlabel("Unidade_Geográfica")
plt.ylabel("Percentual (%)")
plt.legend()
plt.show()

# Criar gráfico de pizza
plt.figure(figsize=(8, 8))
plt.pie(df_2023["Taxa de Abandono"], labels=df_2023["Unidade_Geográfica"], autopct="%1.1f%%", colors=["blue", "red", "green"])
plt.title("Proporção do Abandono Escolar por Estado (2023)")
plt.show()

import plotly.express as px

fig = px.bar(df_2023, x="Unidade_Geográfica", y="Taxa de Abandono", color="Etapa de Ensino", title="Taxa de Abandono Escolar por Etapa de Ensino (2023)")
fig.show()

