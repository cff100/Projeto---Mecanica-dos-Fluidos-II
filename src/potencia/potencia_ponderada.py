import pjenergy.main as mp
import src.auxiliares.caso_zero as cz
import pandas as pd
from .grafico_potencia_ponderada import pond_potencia


def potencia(pressao, estacao, ano, horario):

  # Lista de caminhos para os arquivos CSV
  arquivos_csv = ['/content/pjenergy/data/dados_interpolados/df_interpolado_Verao.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Outono.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Inverno.csv', '/content/pjenergy/data/dados_interpolados/df_interpolado_Primavera.csv']
  # Lista para armazenar os DataFrames
  dataframes = [pd.read_csv(arquivo) for arquivo in arquivos_csv]
  # Concatenar todos os DataFrames em um único
  df_base = pd.concat(dataframes, ignore_index=True)

  variaveis_dict = {'Pressão': pressao, 'Estação': estacao, 'Ano': ano, 'Horário': horario}

  # Substituindo valores '0' usando cz.zero_para_todos
  for chave, valor in variaveis_dict.items():
    if valor == '0':
      variaveis_dict[chave] = cz.zero_para_todos(valor, chave)
  #print(estacao)
  df_mestre = pd.DataFrame(columns=['Pressão', 'Estação', 'Ano', 'Horário', 'Dataframe_Probabilidade'])

  df_base['Data'] = pd.to_datetime(df_base['Data'])
  df_base['Ano'] = df_base['Data'].dt.year

  contagem_todos = 0

  for chave, valor in variaveis_dict.items():
    #print(f'1 -> chave: {chave}, valor: {valor}')
    if valor in ['Todos', 'Todas']:
      #print(f'2 -> chave: {chave}, valor: {valor}')
      if chave == 'Pressão':
        pressao_lista = df_base['Nível_de_Pressão_hPa'].unique().tolist()
      elif chave == 'Estação':
        estacao_lista = df_base['Estação_do_Ano'].unique().tolist()
      elif chave == 'Ano':
        ano_lista = df_base['Ano'].unique().tolist()
      elif chave == 'Horário':
        horario_lista = df_base['Horário_Brasília'].unique().tolist()

      contagem_todos += 1

    else:
      #print(f'3 -> chave: {chave}, valor: {valor}')
      if chave == 'Pressão':
        pressao_lista = [float(valor)]
      elif chave == 'Estação':
        estacao_lista = [valor]
      elif chave == 'Ano':
        ano_lista = [int(valor)]
      elif chave == 'Horário':
        horario_lista = [valor]

  print(f'pressao_lista: {pressao_lista}')
  print(f'estacao_lista: {estacao_lista}')
  print(f'ano_lista: {ano_lista}')
  print(f'horario_lista: {horario_lista}')

  if contagem_todos > 2:
    return 'Variáveis demais com o valor "Todas" ou "0". Precisam ser no máximo duas.'

  for p in pressao_lista:
    for est in estacao_lista:
      #print(est)
      #print(estacao_lista)
      for an in ano_lista:
        for hor in horario_lista:
          df_prob_local = mp.prob(perguntas = False, pressao = p, estacao = est, ano = an, horario = hor, exibir_grafico=False)
          nova_linha = {'Pressão': p, 'Estação': est, 'Ano': an, 'Horário': hor, 'Dataframe_Probabilidade': df_prob_local}

          df_mestre = pd.concat([df_mestre, pd.DataFrame([nova_linha])], ignore_index=True)

  return df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista












def usuario_potencia(perguntas, pressao, estacao, ano, horario):

  '''Inicia a busca pelos argumentos do usuário'''

  if perguntas == True:
    pressao = input('Qual pressão deseja observar (em HPa)? Escolha um número inteiro entre 972 e 1000. Escreva Todas ou 0 para não filtrar nenhuma pressão específica. \n')
    estacao = input('Qual estação deseja observar? Escolha entre Verão, Outono, Inverno ou Primavera. Escreva Todas ou 0 para não filtrar nenhuma estação específica. \n')
    ano = input('Qual ano deseja observar? Escolha um número inteiro entre 2010 e 2023. Escreva Todos ou 0 para não filtrar nenhum ano específico. \n')
    horario = input('Qual horário deseja observar? Escolha entre 03:00, 09:00, 15:00 ou 21:00. Escreva Todos ou 0 para não filtrar nenhum horário específico. \n')

  else:
    pass

  try:
    df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista = potencia(pressao, estacao, ano, horario)
  except:
    print('Variáveis demais com o valor "Todas" ou "0". Precisam ser no máximo duas.')
    return

  pond_potencia(df_mestre, pressao_lista, estacao_lista, ano_lista, horario_lista)
