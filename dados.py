# Arquivo para importar dados da cotação DI-Futuro:
# Bibliotecas:
import pandas as pd
import numpy as np
import json,requests
import json 

import datetime

# API banco de dados 
url = requests.get('https://cotacao.b3.com.br/mds/api/v1/DerivativeQuotation/DI1')
# ler conteúdo da resposta:
text = url.text
#carregar o conteúdo da resposta:
data = json.loads(text)
#normalizando dados em json
df = pd.json_normalize(data['Scty'])

#redefinir os nomes das colunas:
df = df.rename(columns = { 'symb': 'simbolo',
                          'SctyQtn.bottomLmtPric': 'limite_inferior',
                          'SctyQtn.prvsDayAdjstmntPric': 'ajuste_anterior', 
                          'SctyQtn.topLmtPric': 'limite_superior',
                          'SctyQtn.opngPric': 'preco_abertura',
                          'SctyQtn.minPric': 'preco_minimo',
                          'SctyQtn.maxPric': 'preco_maximo',
                          'SctyQtn.avrgPric': 'preco_medio',
                          'SctyQtn.curPrc': 'ultimo_preco',
                          'asset.AsstSummry.grssAmt': 'volume',
                          'asset.AsstSummry.mtrtyCode': 'vencimento',
                          'asset.AsstSummry.opnCtrcts': 'contrato_aberto',
                          'asset.AsstSummry.tradQty': 'numero_negociado',
                          'asset.AsstSummry.traddCtrctsQty': 'contrato_negociado',
                          'asset.code': 'codigo',
                          'buyOffer.price': 'ultima_oferta_compra',
                          'sellOffer.price': 'ultima_oferta_venda'
                          })
difuturo = df.sort_values(by = 'vencimento')
difuturo = difuturo.dropna()
difuturo['vencimento'] = pd.to_datetime(difuturo['vencimento'], format = 'mixed')
difuturo = difuturo.loc[difuturo['vencimento'] < '2028-08-01']
# criar código para nomear arquivo:
hoje = datetime.datetime.today()
hoje = hoje.strftime("%d-%m-%Y")
nome = "di" + hoje + ".csv"
difuturo.to_csv(nome)


