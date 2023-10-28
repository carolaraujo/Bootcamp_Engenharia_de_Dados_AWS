#%%
import requests
from bs4 import BeautifulSoup as bs

# %%
url = 'https://portalcafebrasil.com.br/todos/podcasts/'
# %%
ret = requests.get(url)
# %%
ret.text
# %%
soup = bs(ret.text, features="lxml")

# %%
soup.find('h5')
# %%
soup.find('h5').text
# %%
soup.find('h5').a['href']

# %%

lst_podcasts = soup.find_all('h5')
# %%
for item in lst_podcasts:
    print(f"EP: {item.text} - Link: {item.a['href']}")
# %%
