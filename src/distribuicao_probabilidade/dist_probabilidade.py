import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import weibull_min
import numpy as np

horarios = ['03:00', '09:00', '15:00', '21:00']
plataforma_escolhida = "PETROBRAS XXXIII"

def plot_weibull_velocidade(pressao, estacao, ano):

  # Lista para armazenar os DataFrames temporariamente
  dfs = []

  if estacao == "Verão":
    est = "Verao"
  elif estacao in ["Outono", "Inverno", "Primavera"]:
    est = estacao
  elif estacao == "Todas":
    # Loop para carregar e armazenar os DataFrames
    for est in ["Verao", "Outono", "Inverno", "Primavera"]:
      df_cada_estacao = pd.read_csv(f'/content/pjenergy/data/dados_interpolados/df_interpolado_{est}.csv')
      dfs.append(df_cada_estacao)  # Adiciona cada DataFrame à lista

      # Junta todos os DataFrames da lista em um só
      df = pd.concat(dfs, ignore_index=True)
      
  if estacao != "Todas":
    df = pd.read_csv(f'/content/pjenergy/data/dados_interpolados/df_interpolado_{est}.csv')

  #print(df)

  if ano not in ['Todos', 0]:
    df['Data'] = pd.to_datetime(df['Data'])
    df_ano = df[df['Data'].dt.year == int(ano)]
  else:
    df_ano = df
    if ano == 0:
      ano = 'Todos'

  if pressao not in ['Todas', 0]:
    df_pressao = df_ano[df_ano['Nível_de_Pressão_hPa'] == pressao]
  else:
    df_pressao = df_ano
    if pressao == 0:
      pressao = 'Todas'

  #print(df_ano)

  # Criando um DataFrame para armazenar as probabilidades
  tabela_probabilidades = pd.DataFrame()

  # Criando subplots para 4 horários
  fig, axs = plt.subplots(2, 2, figsize=(15, 10))  # Cria uma grade 2x2 para os gráficos

  for i, horario in enumerate(horarios):
    # Filtrar os dados por horário
    df_horario = df_pressao[df_pressao['Horário_Brasília'] == horario]['Velocidade_Vento_resultante_m/s']
    #print(df_horario)
    # Verificar se existem dados suficientes para o horário
    if df_horario.empty:
        print(f'Nenhum dado disponível para {horario}')
        continue

    # Seleciona o eixo correspondente
    ax = axs[i//2, i % 2]  # Coloca na posição correta o gráfico

    # Plotar a distribuição (histograma com estimativa de densidade)
    sns.histplot(df_horario, kde=False, stat='density', ax=ax, color='lightgray', alpha=0.5, bins = 20)

    # Ajustar a distribuição de Weibull
    params = weibull_min.fit(df_horario)
    x = np.linspace(min(df_horario), max(df_horario), 100)
    weibull_pdf = weibull_min.pdf(x, *params)

    # Plotar a curva ajustada sobre o histograma
    ax.plot(x, weibull_pdf, label='Ajuste de Weibull', color='r')
    ax.set_xlabel('Velocidade do Vento (m/s)')
    ax.set_ylabel('Densidade de Probabilidade')

    if pressao or estacao:
      if not estacao:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Pressão: {pressao} hPa - Ano: {ano}')
      elif not pressao:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Estação: {estacao} - Ano: {ano}')
      else:
        ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Pressão: {pressao} hPa - Estação: {estacao} - Ano: {ano}')
    else:
      ax.set_title(f'Ajuste de Distribuição Weibull - {horario} - Ano: {ano}')


    texto = plataforma_escolhida
    ax.text(0.73, 0.95, f'Plataforma: {texto}', transform=ax.transAxes, fontsize=9, verticalalignment='top')

    # Criar tabela de probabilidades
    df_tabela = pd.DataFrame({
      'Velocidade do Vento (m/s)': x,
      'Densidade de Probabilidade': weibull_pdf
      })
    df_tabela['Horário'] = horario
    df_tabela['Pressão'] = pressao
    df_tabela['Estação'] = estacao
    df_tabela['Ano'] = ano
    tabela_probabilidades = pd.concat([tabela_probabilidades, df_tabela], ignore_index=True)

  # Ajustar espaçamento entre os subplots
  plt.tight_layout()
  plt.show()

  print('\n')

  # Exibir a tabela de probabilidades
  print(tabela_probabilidades)


  # Salvar a tabela em um arquivo CSV, se desejado
  tabela_probabilidades.to_csv(f'Velocidade_Tabela_Probabilidades_Weibull.csv', index=False)

  return tabela_probabilidades

