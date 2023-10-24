#%%
#imports
import requests
import json

#%%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
ret = requests.get(url)
#%% 
if ret:
  print(ret)
else:
  print('falhou')
# %%
dolar = json.loads(ret.text)['USDBRL']

# %%
print(f" 20 Dólares hoje custam {float(dolar['bid']) * 20} reais")
# %%
def cotacao(valor, moeda):
  url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
  #url = 'https://economia.awesomeapi.com.br/json/last/{}'.format(moeda)
  ret = requests.get(url)
  dolar = json.loads(ret.text)[moeda.replace('-', '')]
  print(f" {valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")

# %%
cotacao(20,'JPY-BRL')
# %%
try:
   cotacao(20,'dindim')
except Exception as e:
   print(e)
else:
   print('ok')
# %%
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print(
       f" {valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")
    
# %%
lst_money = [
   "USD-BRL",
   "EUR-BRL",
   "BTC-BRL",
   "RPL-BRL",
   "JPY-BRL"
]

    # %%
multi_moedas(20, "USD-BRL")
# %%

def error_check(func):
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    return inner_func

@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print(
       f" {valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor} {moeda[-3:]}")

multi_moedas(20, "USD-BRL")
multi_moedas(20, "EUR-BRL")
multi_moedas(20, "BTC-BRL")
multi_moedas(20, "RPL-BRL")
multi_moedas(20, "JPY-BRL")

# %%
import backoff
import random

@backoff.on_exception(backoff.expo,(ConnectionAbortedError,ConnectionRefusedError,TimeoutError), max_tries=10)
def test_func(*args, **kwargs):
   rnd = random.random()
   print(f"""
          RND: {rnd}
          args: {args if args else 'sem args'}
          kargs: {kwargs if kwargs else 'sem kwargs'}
          """)
   if rnd < .2:
      raise ConnectionAbortedError('Conexão foi finalizada')
   elif rnd < .4:
      raise ConnectionRefusedError('Conexão foi recusada')
   elif rnd < .6:
      raise TimeoutError('Tempo de espera execedido')
   else:
      return "ok!"
# %%
test_func()
# %%
test_func(42, 51, nome="carol")
# %%
