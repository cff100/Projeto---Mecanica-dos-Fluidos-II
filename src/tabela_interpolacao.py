import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

horarios = ['03:00', '09:00', '15:00', '21:00']

def altura_para_pressao(altura):
  # Constantes
  PA = 101.325  # Pressão atmosférica ao nível do mar em kPa
  k = 1.21e-5   # Constante em s²/m²
  g = 9.81      # Aceleração gravitacional em m/s²

  p = P_h = PA * np.exp(-altura * k * g )
  return p * 10

def brasilia_para_utc(hour_brasilia):
  brasilia_time = datetime.strptime(hour_brasilia, '%H:%M')
  utc_time = brasilia_time + timedelta(hours=3)
  return utc_time.strftime('%H:%M')

def celsius_para_kelvin(celsius):
  return celsius + 273.15


def interpolacao(dicionario_argumentos):
  df_para_interpolacao = dicionario_argumentos['df_para_interpolacao']
  plataforma = dicionario_argumentos['plataforma']



  df_interpolado = pd.DataFrame()

  for d in df_para_interpolacao['Data'].unique():
    df_dia = df_para_interpolacao[df_para_interpolacao['Data'] == d]

    # Loop para iterar pelos horários definidos
    for c, horario in enumerate(horarios):

      # Filtra dados para o horário específico
      df_hora = df_dia[df_dia["Horário_Brasília"] == horario]
      # Ordena os dados filtrados pela coluna que contém as alturas, garantindo que os valores de altura estejam em ordem crescente
      df_hora = df_hora.sort_values("Altitude_m")

      # Coluna de alturas para o eixo Y do gráfico
      Y = df_hora["Altitude_m"]

      # Gera uma sequência de valores suavizados para Y, a ser usada para interpolação nos gráficos
      Y_smooth = np.linspace(Y.min(), Y.max(), 400)

      # Coluna de velocidade do vento para o eixo X do gráfico
      X_velocidade = df_hora['Velocidade_Vento_resultante_m/s']
      X_temperatura = df_hora["Temperatura_C"]

      # Interpolação suave dos valores de velocidade do vento em relação aos valores suavizados de altura
      X_smooth_velocidade = make_interp_spline(Y, X_velocidade)(Y_smooth)
      X_smooth_temperatura = make_interp_spline(Y, X_temperatura)(Y_smooth)

      df_local = pd.DataFrame()
      df_local["Altitude_m"] = Y_smooth
      df_local["Nível_de_Pressão_hPa"] = altura_para_pressao(Y_smooth)
      df_local['Estação_do_Ano'] = df_dia['Estação_do_Ano'].iloc[0]
      df_local["Horário_Brasília"] = horario
      df_local["Horário_UTC"] = brasilia_para_utc(horario)
      df_local["Data"] = d
      df_local['Velocidade_Vento_resultante_m/s'] = X_smooth_velocidade
      df_local['Plataforma'] = plataforma
      df_local["Temperatura_C"] = X_smooth_temperatura
      df_local["Temperatura_K"] = celsius_para_kelvin(X_smooth_temperatura)

      # CONTINUAR A PARTIR DAQUI
      df_local = df_local[df_local[nome_altura] <= 350]
      #print(f'df_local_1: {df_local}')

      df_local[nome_pressao] = df_local[nome_pressao].round()
      #print(f'df_local_2: {df_local}')
      #print('\n \n')

      categorias_agrupar = ['Nível_de_Pressão_hPa', 'Horário_Brasília', 'Data']
      colunas_ordem = ['Plataforma', 'Nível_de_Pressão_hPa', 'Altitude_m', 'Estação_do_Ano',
                      'Horário_Brasília', 'Horário_UTC', 'Data', 'Velocidade_Vento_resultante_m/s', 'Temperatura_C', 'Temperatura_K']

      df_local = df_local.groupby(categorias_agrupar).agg({
      'Velocidade_Vento_resultante_m/s': 'mean',
      'Temperatura_C': 'mean',
      'Temperatura_K': 'mean',
      'Altitude_m': 'mean',
      'Horário_UTC': 'first',
      'Estação_do_Ano': 'first',
      'Plataforma': 'first'
      }).reset_index()

      df_local.reset_index(drop=True, inplace=True)
      df_local = df_local[colunas_ordem]

      #print(f'df_local_3: {df_local}')

      '''n = 3
      df_local = df_local.iloc[::n]  # Mantém apenas 1 a cada 'n' linhas

      print(f'df_local_4: {df_local}')'''


      df_interpolado = pd.concat([df_interpolado, df_local],ignore_index=True)



  #df_local = df_local[df_local[nome_pressao] % 1 == 0]  # Mantém apenas valores inteiros de pressão
  #print(f'df_local: {df_local}')
  #df_local = df_local.groupby(nome_pressao, as_index=False).mean()


  #print(f'df_interpolado: {df_interpolado}')



  df_interpolado.to_csv('df_interpolado.csv', index=False)