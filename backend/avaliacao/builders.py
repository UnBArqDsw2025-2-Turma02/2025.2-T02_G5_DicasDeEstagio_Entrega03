from abc import ABC, abstractmethod
from .models import Avaliacao, Empresa, User
from django.utils.text import slugify

class IAvaliacaoBuilder(ABC):
    @abstract_method
    def reset(self):
        pass

    @abstract_method
    def set_identificacao(self, usuario: User, empresa: Empresa):
        pass

    @abstract_method
    def set_nota_geral(self, nota: int):
        pass
    
    @abstract_method
    def add_detalhes_texto(self, titulo: str, pros: str, contras: str):
        pass
        
    @abstract_method
    def set_contexto_profissional(self, cargo: str, anonimo: bool):
        pass

    @abstract_method
    def get_result(self) -> Avaliacao:
        pass

class AvaliacaoBuilder(IAvaliacaoBuilder):

    _avaliacao: Avaliacao = None

    def __init__(self):
        self.reset()

    def reset(self):
        self._avaliacao = Avaliacao()

    def set_identificacao(self, usuario: User, empresa: Empresa) -> 'AvaliacaoBuilder':
        self._avaliacao.usuario = usuario
        self._avaliacao.empresa = empresa
        return self 
    
    def set_nota_geral(self, nota: int) -> 'AvaliacaoBuilder':
        if not 1 <= nota <= 5:
            raise ValueError("Nota deve estar entre 1 e 5")
        self._avaliacao.nota_geral = nota
        return self

    def add_detalhes_texto(self, titulo: str, pros: str, contras: str) -> 'AvaliacaoBuilder':
        self._avaliacao.titulo = titulo
        self._avaliacao.pros = pros
        self._avaliacao.contras = contras
        return self
    
    def set_contexto_profissional(self, cargo: str, anonimo: bool) -> 'AvaliacaoBuilder':
        self._avaliacao.anonima = anonimo
        if not anonimo:
            self._avaliacao.cargo = cargo
        else:
            self._avaliacao.cargo = f"Ex-funcionário(a) ({slugify(cargo)})"
            
        return self

    def get_result(self) -> Avaliacao:
        if not all([self._avaliacao.usuario, self._avaliacao.empresa, self._avaliacao.nota_geral]):
            raise ValueError("Uma avaliação deve ter no mínimo usuário, empresa e nota.")
            
        produto_final = self._avaliacao
        self.reset() 
        return produto_final