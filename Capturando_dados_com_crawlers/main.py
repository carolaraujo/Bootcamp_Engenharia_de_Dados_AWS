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
# selecionando o tipo de cep
elem_cod = driver.find_element('name', 'tipoCEP')
elem_cod.click()
elem_cod = driver.find_element('xpath', '//*[@id="tipoCEP"]/optgroup/option[6]')
# %%
# clicando em pesquisar
elem_cod = driver.find_element('id', 'btn_pesquisar')
elem_cod.click()
# %%
# capturando os dados da pesquisa
logradouro = driver.find_element('xpath', '/html/body/main/form/div[1]/div[2]/div/div[4]/table/tbody/tr/td[1]')
logradouro.text
bairro = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[2]')
bairro.text
localidade = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[3]')
localidade.text
cep = driver.find_element('xpath', '//*[@id="resultado-DNEC"]/tbody/tr/td[4]')
cep.text

driver.close()
# %%
print(f"""
      Para o CEP: {cep.text}
      Endereço: {logradouro.text}
      Bairro: {bairro.text}
      Localidade: {localidade.text}
""")

# %%
