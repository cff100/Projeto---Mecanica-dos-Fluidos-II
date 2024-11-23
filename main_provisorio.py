import src.usuario as us
import src.numero_linhas_colunas as nlc

def main(perguntas = True, variavel = "Ambos", modo = "Original", componente_velocidade = "Resultante", plataforma = "7", estacao = "Geral", indicador = "Média", data = None, ano = "Todos"):

  dicionario_argumentos = us.argumentos_usuario(perguntas, variavel, modo, componente_velocidade, plataforma, estacao, indicador, data, ano)
  if dicionario_argumentos['data'] == None and dicionario_argumentos['estacao'] == None:
    print('Não é possível criar um gráfico com essa combinação de data e estação \n Dataframe gerado:')
    return dicionario_argumentos['df']
  a = nlc.linhas_colunas(dicionario_argumentos)

  return a
