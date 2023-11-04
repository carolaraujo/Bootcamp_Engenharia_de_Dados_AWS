import datetime
import math

class Pessoa:
    def __init__(self, nome: str, sobrenome: str, data_de_nascimento: datetime.date):
        self.data_de_nascimento = data_de_nascimento
        self.sobrenome = sobrenome
        self.nome = nome

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days /365.2425) #2425 para considerar os anos bisextos
    
    def  __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"

carol = Pessoa(nome='Carol', sobrenome='Araujo', data_de_nascimento=datetime.date(1993, 6, 8))

print(carol)
print(carol.nome)
print(carol.sobrenome)
print(carol.idade)