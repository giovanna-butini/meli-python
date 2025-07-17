#!/usr/bin/env python
# coding: utf-8

# Dicionário de Dados
# 
# | Campo                     | Tipo     | Descrição                                                                 |
# |:--------------------------|:---------|:--------------------------------------------------------------------------|
# | **alert_id**              | string   | Identificador único do alerta.                                            |
# | **creation_datetime**     | datetime | Data e hora em que o alerta foi gerado.                                   |
# | **impact_level**          | string   | Nível de impacto para a organização/equipe.                               |
# | **status**                | string   | Status do alerta.                                                         |
# | **assigned_to**           | string   | Time/equipe responsável.                                                  |
# | **type_of_alert**         | string   | Tipo do alerta.                                                           |
# | **resolutation_datetime** | datetime | Data e hora da resolução/finalização do alerta.                           |
# | **conclusion**            | string   | Conclusão da análise.                                                     |

# 1. Varredura e Extração de Dados de uma API
# 1.1. Bibliotecas utilizadas:
# - flask: Microframework web. Utilizado para simular a API.
# - threading: Para rodar o servidor flask em background no Jupyter.
# - pandas: Para manipulação de dados.
# - random: Para gerar dados aleatórios.
# - datetime: Para manipulação de datas.
# - uuid: Para gerar identificadores únicos.
# - csv: Para salvar os dados em arquivo.

# **1.2. Mapeamento dos Campos**
# alert_id: Identificador único gerado de forma aleatória.
# creation_date: Foi definida uma fórmula para determinar um datetime aleatório do passado, com até 365 dias e 24 horas atrás, a partir do dia atual.
# impact_level: Baixo; Médio; Alto; Crítico. 
# status: Aberto; Em análise; Concluído. 
# assigned_to: Monitoramento, TI, Financeiro, Compliance ou Logística;
# type_of_alert: Cada equipe possui tipos específicos de alertas, conforme especificado abaixo.
#  1. Monitoramento: Movimentação financeira suspeita; Login suspeito.<br>
#  2. TI: Backup não executado; Registro incompleto no sistema; Atualização de sistema pendente.<br>
#  3. Financeiro: Relatório financeiro com erro; Conformidade fiscal incompleta; Pagamento para fornecedor não homologado.<br>
#  4. Compliance: Conflito de interesse; Código de conduta violado.<br>
#  5. Logística: Entrega fora do prazo; Produto sem rastreamento; Falha no controle de estoque.
# resolutation_date: Foi definida uma fórmula para determinar um datetime aleatório (em um intervalo de execução de 7 dias - 168 horas) a partir da data de criação do alerta (*creation_date*), caso o alerta estiver com o status igual a "Concluído". 
# conclusion: Positivo; Falso Positivo e Necessita de monitoramento. O campo só irá conter dado se o alerta já possuir uma análise concluída. 

from flask import Flask, jsonify, request
from threading import Thread
from datetime import datetime, timedelta
import pandas as pd, random, uuid, csv

status = ["Aberto", "Em análise", "Concluído"]
type_of_alert_by_teams = {
    "Monitoramento": [
        "Movimentação financeira suspeita", 
        "Login suspeito"
    ],
    "TI": [
        "Backup não executado",
        "Registro incompleto no sistema",
        "Atualização de sistema pendente"
    ],
    "Financeiro": [
        "Relatório financeiro com erro",
        "Conformidade fiscal incompleta",
        "Pagamento para fornecedor não homologado"
    ],
    "Compliance": [
        "Conflito de interesse",
        "Código de conduta violado"
    ],
    "Logística": [
        "Entrega fora do prazo",
        "Produto sem rastreamento",
        "Falha no controle de estoque"
    ]
}
impact_level = ["Baixo", "Médio", "Alto", "Crítico"]
conclusions = ["Positivo", "Falso positivo", "Necessita monitoramento"]
alerts = {}
for i in range(1, 201): #Geração de 200 registros.
  alert_id = str(uuid.uuid4()) #uuid4 diz respeito a versão 4 da função. Gera um identificador único de forma aleatória. 
  creation_date = datetime.now() - timedelta(days = random.randint(0, 365), hours = random.randint(0, 24)) #Definindo um datetime aleatório do passado, com até 365 dias e 24 horas atrás, a partir do dia atual.
  assigned_to = random.choice(list(type_of_alert_by_teams.keys())) #Retorna as equipes de forma randômica.
  type_of_alert = random.choice(type_of_alert_by_teams[assigned_to]) #Retorna o tipo de alerta com base na respectiva equipe/time.
  resolved = random.choice([True, False])
  resolutation_date = (creation_date + timedelta(hours = random.randint(0, 168))).strftime("%Y-%m-%d %H:%M:%S") if resolved else None #Definindo um datetime aleatório (em um intervalo de execução de 7 dias - 168 horas) a partir da data de criação do alerta (*creation_date*), caso o alerta estiver com o status igual a "Concluído". 
  #Abaixo, estou atribuindo cada valor para sua respectiva chave dentro do dicionário. 
  alert = {
      "alert_id": alert_id,
      "creation_datetime": creation_date.strftime("%Y-%m-%d %H:%M:%S"),
      "type_of_alert": type_of_alert,
      "impact_level": random.choice(impact_level),
      "status": "Concluído" if resolved else random.choice(["Aberto", "Em análise"]),
      "assigned_to": assigned_to,
      "resolutation_datetime": resolutation_date,
      "conclusion": random.choice(conclusions) if resolved else None
  }
  alerts[alert_id] = alert #Incrementando o dicionário a cada loop.  

# 1.3. Simulação da API:
app = Flask(__name__) #Criação da instância da aplicação Flask. 
@app.route('/api/alerts', methods = ['GET']) #Definindo a rota que retornará todos os dados da base de alertas. 
def list_alerts(): 
  return jsonify(alerts) #jsonify é uma função do Flask para retornar dados no formato JSON.

@app.route('/api/alerts/<alert_id>', methods=['GET']) #Definindo rota que retornará dados do ID especificado.
def search_alert(alert_id):
    alert = alerts.get(alert_id) 
    #Verifica se o ID especificado está presente no dicionário, se estiver, retornará as respectivas informações, caso contrário exibirá que a mensagem "Alerta não encontrado".
    if alert:
        return jsonify(alert)
    else:
        return jsonify({"erro": "Alerta não encontrado"}), 404

def run_flask_app():
    app.run(port = 5000) #Definição da porta para a chamada da API.

flask_thread = Thread(target = run_flask_app) #Definindo a Thread paralela para conseguir executar a aplicação do microframework Flask. Importante: Essa etapa foi desenvolvida pois o desenvolvido e teste foram realizados via Jupyter Notebook. 
flask_thread.start()

#http://localhost:5000/api/alerts

# 2. Escrita e Desnormalização de Resultados
# 2.1. Envio dos resultados para um arquivo .csv:
def save_csv(name_file = "alerts.csv"): #Nome do arquivo: "alerts.csv".
    with open(name_file, mode = 'w', newline = '', encoding = 'utf-8') as csvfile:
        fieldnames = ["alert_id", "creation_datetime", "type_of_alert", "impact_level", "status", "assigned_to", "resolutation_datetime", "conclusion"] #Especificando os campos. 
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for alert in alerts.values():
            writer.writerow(alert) #Incrementando o registro no .csv. 
            
save_csv()
# 2.2. Desnormalização do JSON:
alerts_list = list(alerts.values())
df = pd.json_normalize(alerts_list) #Normalizando o retorno JSON para exibição na forma tabular. 