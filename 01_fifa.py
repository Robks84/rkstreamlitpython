# Roberto K.Stoler      RA:2302711
# Victor Rocha Azevedo  RA 2300741

import sqlalchemy as sqa 
import pandas as pd
import time as tempo
from selenium import webdriver
from selenium.webdriver.common.by import By

navegador = webdriver.Chrome()
navegador.maximize_window()

navegador.get('https://inside.fifa.com/fifa-world-ranking/men')

# aguarda 3 segundos para carregar a pagina
tempo.sleep(3)

navegador.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click()

elemento = navegador.find_element(By.XPATH, '//*[@id="content"]/main/div[2]/section/div/div/div[6]/button/div[2]')
    
# Executa JavaScript para rolar a página até que o elemento esteja visível
navegador.execute_script("arguments[0].scrollIntoView();", elemento)

# aguarda 3 segundos para o scroll da pagina
tempo.sleep(3)

navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[6]/button/div[2]').click()

time                = navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr[1]/td[2]/div/a[1]').text   
pontos              = navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr[1]/td[3]/span').text   
pontos_anteriores   =  navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr[1]/td[4]/span').text   
porcentagem         =  navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr[1]/td[5]/span').text   

lista_times = []
for i in range(1,101):  
    posicao = i
    time                = navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr['+str(i)+']/td[2]/div/a[1]').text   
    pontos              = navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr['+str(i)+']/td[3]/span').text   
    pontos_anteriores   = navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr['+str(i)+']/td[4]/span').text   
    porcentagem         = navegador.find_element(By.XPATH,'//*[@id="content"]/main/div[2]/section/div/div/div[5]/table/tbody/tr['+str(i)+']/td[5]/span').text   

    lista_times.append([posicao, time, pontos, pontos_anteriores, porcentagem])  

df_times = pd.DataFrame(lista_times,columns=['Ranking','Time','Pontos','Pontos_anteriores','Porcentagem'])

# SALVANDO DADOS EM CSV E JSON
df_times.to_csv('../0_bases_originais/dados_originais.csv',sep=';', index=False, encoding='utf-8-sig')
df_times.to_json('../0_bases_originais/dados_originais.json')

# SALVANDO DADOS NO BANCO 
engine = sqa.create_engine("sqlite:///df_novo.db", echo=True)
conn = engine.connect()

df_times.to_sql('times.db', con=conn)

navegador.quit()