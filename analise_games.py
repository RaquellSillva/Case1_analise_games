# Case 1 - Análise Exploratória de Dados
# Autora: Raquel Joana da Silva

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

sns.set(style="whitegrid")
plt.style.use("dark_background")
sns.set_theme(
    style="darkgrid",
    rc={
        "axes.facecolor": "#121212",
        "figure.facecolor": "#101010",
        "axes.edgecolor": "#333333",
        "grid.color": "#2a2a2a",
        "xtick.color": "#e6e6e6",
        "ytick.color": "#e6e6e6",
        "axes.labelcolor": "#e6e6e6",
        "text.color": "#e6e6e6",
    },
)
plt.rcParams["figure.figsize"] = (10, 6)

os.makedirs("resultados", exist_ok=True)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", 0)

# Carregar a base
df = pd.read_csv("vgsales.csv", encoding="utf-8")

print("Visualizando as primeiras linhas: \n")
print(df.head(), "\n")

print("Valores ausentes por coluna:\n")
display(df.isnull().sum().to_frame("Valores Ausentes"))

# Limpar dados:
df = df.dropna(subset=["Ano"])
df["Ano"] = df["Ano"].astype(int)

# Criar a coluna Década
def classificar_decada(ano: int) -> str:
    if 1990 <= ano <= 1999:
        return "Anos 90"
    elif 2000 <= ano <= 2009:
        return "Anos 2000"
    elif 2010 <= ano <= 2016:
        return "Anos 2010"
    else:
        return "Outro"

df["Década"] = df["Ano"].apply(classificar_decada)

print("\nColuna 'Década' criada:\n")
display(df[["Nome", "Ano", "Década"]].head())


# Tabela completa estilizada
fmt = {"Vendas Globais (milhões)": "{:,.2f}".format}

def styler_dark(s):
    return (
        s.format(fmt, thousands=".", decimal=",")
         .hide(axis="index")
         .set_properties(**{
             "text-align": "center",
             "white-space": "nowrap",
             "font-size": "13px",
             "color": "#E6E6E6",
             "background-color": "#121212",
             "padding": "8px 12px",
             "border": "1px solid #333333",
         })
         .set_table_styles([
             {"selector": "th", "props": [
                 ("text-align", "center"),
                 ("font-size", "13px"),
                 ("color", "#FFFFFF"),
                 ("background-color", "#1E1E1E"),
                 ("padding", "10px"),
                 ("border-bottom", "1px solid #333333")
             ]},
             {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#171717")]},
             {"selector": "tbody tr:nth-child(odd)",  "props": [("background-color", "#111111")]},
             {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]}
         ])
    )

# Tabela completa
styled_df = styler_dark(
    df.style.background_gradient(subset=["Vendas Globais (milhões)"], cmap="Greens", axis=None)
)
print("\n=== Tabela Completa (Dark) ===")
display(styled_df)

# Análises principais
col_vendas = "Vendas Globais (milhões)"

# Checagem para evitar erro de digitação no nome da coluna
if col_vendas not in df.columns:
    raise ValueError(f"Coluna esperada não encontrada: {col_vendas}. Colunas atuais: {list(df.columns)}")

# Gênero que mais vendeu globalmente
vendas_por_genero = (
    df.groupby("Gênero")[col_vendas]
      .sum()
      .sort_values(ascending=False)
)
genero_top = vendas_por_genero.idxmax()
venda_top = vendas_por_genero.max()

# Plataforma com mais jogos lançados - apenas contagem
plataforma_counts = df["Plataforma"].value_counts()
plataforma_mais_jogos = plataforma_counts.idxmax()
qtd_plataforma = plataforma_counts.max()

# Lançamentos por ano - para o gráfico de linha
lancamentos_por_ano = df["Ano"].value_counts().sort_index()

print(f"🎮 Gênero campeão em vendas globais: {genero_top} ({venda_top:.2f} milhões)")
print(f"🕹️ Plataforma com mais jogos lançados: {plataforma_mais_jogos} ({qtd_plataforma} jogos)\n")

# gráficos
# # #Top 5 gêneros mais vendidos

vendas_por_genero = (
    df.groupby("Gênero")["Vendas Globais (milhões)"]
      .sum()
      .rename_axis("Gênero")
      .reset_index(name="Vendas")    # garante que existe a coluna "Vendas"
      .sort_values("Vendas", ascending=False)
)

# selecionar os 5 maiores gêneros
top5 = vendas_por_genero.nlargest(5, "Vendas")

# criar o gráfico
ax = sns.barplot(data=top5, x="Vendas", y="Gênero", hue="Gênero", palette="Greens", legend=False)
ax.set_title("Top 5 Gêneros Mais Vendidos Globalmente", fontsize=14, color="#E6E6E6")
ax.set_xlabel("Vendas Globais (em milhões)", fontsize=12, color="#E6E6E6")
ax.set_ylabel("Gênero", fontsize=12, color="#E6E6E6")
plt.tight_layout()

# salvar e mostrar
plt.savefig("resultados/grafico_generos_dark.png", dpi=120)
plt.show()
plt.close()

# total de jogos lançados por ano
lanc_por_ano = df["Ano"].value_counts().sort_index()
ax = sns.lineplot(x=lanc_por_ano.index, y=lanc_por_ano.values, marker="o")
ax.set_title("Total de Jogos Lançados por Ano")
ax.set_xlabel("Ano")
ax.set_ylabel("Quantidade de Jogos")
plt.tight_layout()
plt.savefig("resultados/grafico_lancamentos_dark.png", dpi=120)
plt.show()
plt.close()

styled_df.to_html("resultados/tabela_completa.html")

# Conclusão automática
genero_top = vendas_por_genero.iloc[0, 0]
vendas_top = vendas_por_genero.iloc[0, 1]
plataforma_counts = df["Plataforma"].value_counts()
plataforma_top = plataforma_counts.idxmax()
qtd_plataforma = plataforma_counts.max()
ano_pico = lanc_por_ano.idxmax()
qtd_pico = lanc_por_ano.max()
top3_generos = ", ".join(vendas_por_genero.head(3)["Gênero"].tolist())

print("\n                 === CONCLUSÃO ===")
print(
    f"O gênero com maior volume de vendas globais foi {genero_top} ({venda_top:.2f} mi)\n mostrando uma preferência dos jogadores por jogos competitivos e dinâmicos. \n"
    f"Os gêneros mais fortes foram: {top3_generos}. \n"
    f"A plataforma com mais lançamentos foi {plataforma_mais_jogos} ({qtd_plataforma} jogos). \n"
    f"Observei um pico de lançamentos em {ano_pico} (com {qtd_pico} jogos), \n"
    "indicando maior aquecimento do mercado nesse período."
)

#Minha principal descoberta.
print(
    "\n A partir dos dados analisados,observei que essas tendências indicam \n que o setor de games é um setor maduro,competitivo e movido por avanços tecnológicos \n constantes,com forte influência do público que busca \n a conexão,desafio,sensação de imersão e evolução continua na área de jogos. "
)