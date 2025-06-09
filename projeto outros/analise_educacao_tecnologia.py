import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 1. Carregar e filtrar os dados
df = pd.read_csv('taxas_de_rendimento_escolar.csv')

# Ajustar nomes, se necessário
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Filtro para 2023 e Sudeste
estados_sudeste = ['Minas Gerais', 'São Paulo', 'Rio de Janeiro']
df_sudeste = df[(df['Ano'] == 2023) & (df['Unidade_Geografica'].isin(estados_sudeste))]

# 2. Plot 1 – Barras com Percentuais
df_plot1 = df_sudeste.groupby('Unidade_Geográfica')[['Taxa_de_Aprovação', 'Taxa_de_Reprovação', 'Taxa_de_Abandono']].mean().reset_index()
df_plot1_melt = df_plot1.melt(id_vars='Unidade_Geográfica', var_name='Indicador', value_name='Percentual')

plt.figure(figsize=(10, 6))
sns.barplot(data=df_plot1_melt, x='Unidade_Geografica', y='Percentual', hue='Indicador')
plt.title('Taxas de Rendimento Escolar por Estado - 2023 (%)')
plt.savefig('plot1_taxas_percentuais.png')
plt.close()

# 3. Plot 2 – Pizza de Abandono
df_plot2 = df_sudeste.groupby('Unidade_Geografica')['Número_de_Alunos_que_Abandonaram'].sum().reset_index()
plt.figure(figsize=(8, 6))
plt.pie(df_plot2['Número_de_Alunos_que_Abandonaram'], labels=df_plot2['Unidade_Geográfica'], autopct='%1.1f%%')
plt.title('Proporção de Abandono Escolar por Estado - 2023')
plt.savefig('plot2_pizza_abandono.png')
plt.close()

# 4. Plot 3 – Gráfico Interativo com Botões (Plotly)
fig = px.bar(df_sudeste, 
             x='Unidade_Geografica', 
             y='Taxa_de_Abandono', 
             color='Etapa_do_Ensino', 
             barmode='group',
             title='Taxa de Abandono Escolar por Etapa de Ensino - 2023')

fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(label="Abandono",
                     method="update",
                     args=[{"y": [df_sudeste['Taxa_de_Abandono']]}]),
                dict(label="Aprovação",
                     method="update",
                     args=[{"y": [df_sudeste['Taxa_de_Aprovação']]}]),
                dict(label="Reprovação",
                     method="update",
                     args=[{"y": [df_sudeste['Taxa_de_Reprovação']]}]),
            ]),
            direction="down",
            showactive=True,
        ),
    ]
)
fig.write_image("plot3_interativo_abandono.png")
fig.show()

# 5. Criar PDF com análise
c = canvas.Canvas("relatorio_visualizacao.pdf", pagesize=letter)
width, height = letter

c.setFont("Helvetica-Bold", 16)
c.drawCentredString(width / 2.0, height - 50, "Relatório - Análise Educacional (Sudeste, 2023)")

c.setFont("Helvetica", 12)
c.drawString(50, height - 100, "O projeto analisa as taxas de rendimento escolar nos estados de MG, SP e RJ em 2023,")
c.drawString(50, height - 115, "considerando aprovação, reprovação e abandono no Ensino Fundamental e Médio.")

c.drawImage("plot1_taxas_percentuais.png", 50, height - 400, width=500, height=250)
c.drawImage("plot2_pizza_abandono.png", 50, height - 700, width=500, height=250)
c.save()
