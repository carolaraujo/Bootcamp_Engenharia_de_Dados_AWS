#%%
import requests

# %%
url = 'https://portalcafebrasil.com.br/todos/podcasts/'
# %%
ret = requests.get(url)
# %%
ret.text
# %%
