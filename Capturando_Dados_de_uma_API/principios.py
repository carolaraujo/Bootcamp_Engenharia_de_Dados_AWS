import datetime
import math
from typing import List

class Pessoa:
    def __init__(
            self, 
            nome: str, 
            sobrenome: str, 
            data_de_nascimento: datetime.date
            ) -> None:
        self.nome = nome
        self.sobrenome = sobrenome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)  # 2425 para considerar os anos bissextos
    
    def  __str__(self) -> str:
        return f"{self.nome} {self.sobrenome} tem {self.idade} anos"
    

class Curriculo:
    def __init__(self, pessoa: Pessoa, experiencias: List[str]):
        self.experiencias = experiencias
        self.pessoa = pessoa  # Remova a vírgula

    @property
    def quantidade_de_experiencias(self) -> int:
        return len(self.experiencias)
    
    @property
    def empresa_atual(self) -> str:
        return self.experiencias[-1]
    
    def adiciona_experiencia(self, experiencia: str) -> None:
        self.experiencias.append(experiencia)

    def __str__(self):
        return f"{self.pessoa.nome} {self.pessoa.sobrenome} tem {self.pessoa.idade} anos e já " \
        f"trabalhou em {self.quantidade_de_experiencias} empresas e atualmente trabalha" \
        f" na empresa {self.empresa_atual}"

carol = Pessoa(nome='Carol', sobrenome='Araujo', data_de_nascimento=datetime.date(1993, 6, 8))

curriculo_carol = Curriculo(pessoa=carol, experiencias=['RRJ', 'Protege', 'Cargox', 'Itau', 'Serasa Experian'])

#print(curriculo_carol.pessoa.idade)

#print(curriculo_carol)
#curriculo_carol.adiciona_experiencia("Carol S/A")
#print(curriculo_carol)



class Vivente:
    def __init__(self, nome: str, data_de_nascimento: datetime.date) -> None:
        self.nome = nome
        self.data_de_nascimento = data_de_nascimento

    @property
    def idade(self) -> int:
        return math.floor((datetime.date.today() - self.data_de_nascimento).days / 365.2425)
    
    def emite_ruido(self, ruido: str):
        print(f"{self.nome} fez ruido: {ruido}") 
    
class PessoaHeranca(Vivente):
    def  __str__(self) -> str:
        return f"{self.nome} tem {self.idade} anos"
    
    def fala(self, frase):
        return self.emite_ruido(frase)
    
class Cachorro(Vivente):
    def __init__(self, nome: str, data_de_nascimento: datetime.date, raca: str) -> None:
        super().__init__(nome, data_de_nascimento)
        self.raca = raca

    def late(self):
        return self.emite_ruido("Au! Au!")

    def  __str__(self) -> str:
        return f"{self.nome} é da raça {self.raca} e tem {self.idade} anos"
    
carol2 = PessoaHeranca(nome='Carol', data_de_nascimento=datetime.date(1993,6,9))

print(carol2)

belisco = Cachorro(nome='Belisco', data_de_nascimento=datetime.date(2019, 4, 15), raca='Lhasa Apso')

print(belisco)

belisco.late()
belisco.late()
belisco.late()
belisco.late()
belisco.late()
belisco.late()
belisco.late()
belisco.late()
belisco.late()
carol2.fala("Cala a boca belisco!")
belisco.late()
belisco.late()
belisco.late()
belisco.late()
belisco.late()
