#%%
# importando os pacotes
from selenium import webdriver
import time
import pandas as pd
# %%
# acessando o wikipedia
driver = webdriver.Chrome()
def tem_item(xpath, driver = driver):
    try:
        driver.find_element('xpath', '//*[@id="mw-content-text"]/div[1]/table[2]')
        return True
    except:
        return False
time.sleep(5)
driver.implicitly_wait(40)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')


#%%

tb_filmes = '//*[@id="mw-content-text"]/div[1]/table[2]'

i = 0
while not tem_item(tb_filmes):
    i +=1
    if i > 50:
        break
    pass

tabela = driver.find_element('xpath', '//*[@id="mw-content-text"]/div[1]/table[2]')

# criando o dataframe
df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0]
driver.quit()
# %%
# visualizando o dataframe
df
# %%
# aplicando filtros
df[df['Ano']==1984]
# %%
# exportando o dataframe em csv 
df.to_csv('filmes_Nicolas_Cage.csv', sep=';', index=False)
# %%
