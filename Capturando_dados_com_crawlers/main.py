#%%
from selenium import webdriver
#%%
# Acesso ao site da How
driver = webdriver.Chrome()
driver.get('https://howedu.com.br')
# %%
# clicando no botão
element = driver.find_element('xpath', '//*[@id="post-11648"]/div/div/section[2]/div/div[1]/div/div[5]/div/div/a/span/span[2]')
element.click()
# %%
# Acessando o site de busca de cep dos correios
driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php')
elem_cep = driver.find_element('name', 'endereco')
elem_cep.click()

# %%
# preenchendo o formulário
elem_cep.clear()
elem_cep.send_keys('80420130')
# %%
#p preenchendo o cep
elem_cod = driver.find_element('name', 'tipoCEP')
elem_cod.click()
elem_cod = driver.find_element('xpath', '//*[@id="tipoCEP"]/optgroup/option[6]')
# %%
# clicando em pesquisar
elem_cod = driver.find_element('id', 'btn_pesquisar')
elem_cod.click()
# %%
