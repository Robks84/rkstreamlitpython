import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sqlalchemy as sqa

# Leitura dos dados do banco
engine = sqa.create_engine("sqlite:///df_novo.db", echo=True)
conn = engine.connect()

# Definindo os tipos das colunas
df_time = pd.read_sql('times.db', con=conn)
df_time = pd.DataFrame(df_time, columns=['Ranking', 'Time', 'Pontos', 'Pontos_anteriores', 'Porcentagem'])

df_time['Ranking'] = df_time['Ranking'].astype(int)
df_time['Time'] = df_time['Time'].astype(str)
df_time['Pontos'] = df_time['Pontos'].astype(float)
df_time['Pontos_anteriores'] = df_time['Pontos_anteriores'].astype(float)
df_time['Porcentagem'] = df_time['Porcentagem'].str.replace('+', '').str.replace('-', '0').astype(float)


# Filtrar os top 10 times
df_top10 = df_time.head(10)

# Título do App Cotação
st.header('APP TIME')

# Imagem do aplicativo
st.sidebar.image('https://static.vecteezy.com/ti/vetor-gratis/p1/14470969-logotipo-oficial-da-fifa-design-de-simbolo-branco-e-azul-ilustracao-abstrata-do-gratis-vetor.jpg')

# Título do aplicativo
st.title("Análise de Rankings de Futebol")

# 1. Tabela de Classificação
st.header("Tabela de Classificação - Top 10 Times")
st.dataframe(df_top10)

# 2. Gráfico de Barras - Pontos por Time
st.header("Pontos por Time - Top 10 Times")
fig, ax = plt.subplots()
ax.bar(df_top10['Time'], df_top10['Pontos'], color='skyblue')
ax.set_xlabel("Times")
ax.set_ylabel("Pontos")
ax.set_title("Pontos por Time")
plt.xticks(rotation=45)
st.pyplot(fig)

# 3. Gráfico de Linha - Variação de Pontos
st.header("Variação de Pontos - Top 10 Times")
fig, ax = plt.subplots()
ax.plot(df_top10['Time'], df_top10['Pontos'], marker='o', label='Pontos Atuais')
ax.plot(df_top10['Time'], df_top10['Pontos_anteriores'], marker='o', linestyle='--', label='Pontos Anteriores')
ax.set_xlabel("Times")
ax.set_ylabel("Pontos")
ax.set_title("Variação de Pontos")
ax.legend()
plt.xticks(rotation=45)
st.pyplot(fig)

# 4. Gráfico de Pizza - Distribuição de Pontos
st.header("Distribuição de Pontos - Top 10 Times")
fig, ax = plt.subplots()
ax.pie(df_top10['Pontos'], labels=df_top10['Time'], autopct='%1.1f%%', startangle=90)
ax.set_title("Distribuição de Pontos entre os Times")
st.pyplot(fig)

# 5. Tabela de Diferença de Pontos
st.header("Diferença de Pontos Atuais e Anteriores - Top 10 Times")
df_top10['Diferença'] = df_top10['Pontos'] - df_top10['Pontos_anteriores']
st.dataframe(df_top10[['Time', 'Pontos', 'Pontos_anteriores', 'Diferença']])

# 6. Visão interativa com st.slider
st.header("Filtrar Times por Pontuação")

# Adicionando o controle deslizante para selecionar o intervalo de pontuação
min_pontos = int(df_top10['Pontos'].min())
max_pontos = int(df_top10['Pontos'].max())
pontos_selecionados = st.slider("Selecione a faixa de pontos", min_pontos, max_pontos, (min_pontos, max_pontos))

# Filtrando os dados com base na faixa de pontos selecionada
df_filtrado = df_top10[(df_top10['Pontos'] >= pontos_selecionados[0]) & (df_top10['Pontos'] <= pontos_selecionados[1])]

# Exibindo a tabela filtrada
st.dataframe(df_filtrado)

# Exibindo o gráfico de barras atualizado com os dados filtrados
fig, ax = plt.subplots()
ax.bar(df_filtrado['Time'], df_filtrado['Pontos'], color='skyblue')
ax.set_xlabel("Times")
ax.set_ylabel("Pontos")
ax.set_title("Pontos por Time (Filtrados)")
plt.xticks(rotation=45)
st.pyplot(fig)

# Fechar a conexão com o banco de dados
conn.close()

# Executar o comando para iniciar o Streamlit
# streamlit run nome_do_arquivo.py
