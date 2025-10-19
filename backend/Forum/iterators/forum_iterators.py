from abc import ABC, abstractmethod
from typing import Any, Optional
from django.db.models import QuerySet
from ..models import Forum


class Iterator(ABC):
    
    @abstractmethod
    def has_next(self) -> bool:
        pass
    
    @abstractmethod
    def next(self) -> Any:
        pass
    
    @abstractmethod
    def reset(self) -> None:
        pass


class TopicoPorTipoIterator(Iterator):
    
    def __init__(self, topicos: QuerySet, tipo_topico: str = None):
        self._topicos = list(topicos)
        self._tipo_topico = tipo_topico
        self._position = 0
        
        if tipo_topico:
            self._filtrar_por_tipo()
    
    def _filtrar_por_tipo(self):
        marcadores = {
            'vaga': '[VAGA',
            'duvida': '[DÚVIDA',
            'experiencia': '[EXPERIÊNCIA',
            'dica': '[DICA',
            'discussao': '[DISCUSSÃO'
        }
        
        marcador = marcadores.get(self._tipo_topico.lower())
        if marcador:
            self._topicos = [
                topico for topico in self._topicos 
                if marcador in topico.titulo
            ]
    
    def has_next(self) -> bool:
        return self._position < len(self._topicos)
    
    def next(self) -> Forum:
        if not self.has_next():
            raise StopIteration("Não há mais tópicos")
        
        topico = self._topicos[self._position]
        self._position += 1
        return topico
    
    def reset(self) -> None:
        self._position = 0
    
    def get_total(self) -> int:
        return len(self._topicos)

    def current(self) -> Optional[Forum]:
        if 0 <= self._position - 1 < len(self._topicos):
            return self._topicos[self._position - 1]
        return None


class ForumCollection:
    
    def __init__(self, queryset: QuerySet = None):
        self._queryset = queryset if queryset is not None else Forum.objects.all()
    
    def create_iterator_por_tipo(self, tipo_topico: str) -> TopicoPorTipoIterator:
        return TopicoPorTipoIterator(self._queryset, tipo_topico)
    
    def get_total_count(self) -> int:
        return self._queryset.count()


def exemplo_basico():
    collection = ForumCollection()
    iterator_vagas = collection.create_iterator_por_tipo('vaga')
    
    print(f"Vagas encontradas: {iterator_vagas.get_total()}")
    
    while iterator_vagas.has_next():
        vaga = iterator_vagas.next()
        print(f"• {vaga.titulo}")


if __name__ == "__main__":
    exemplo_basico()
