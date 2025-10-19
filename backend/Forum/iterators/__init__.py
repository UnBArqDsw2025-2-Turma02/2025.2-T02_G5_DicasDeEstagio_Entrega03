# Iterators package for Forum module - VERSÃO MÍNIMA

"""
Módulo de Iterators para o Forum - Versão Mínima
Implementa demonstração essencial do padrão Iterator integrado com Factory Method

Implementação mínima:
- TopicoPorTipoIterator: Filtra tópicos por tipo usando marcadores do Factory Method
- ForumCollection: Factory para criar iterators apropriados
"""

from .forum_iterators import (
    Iterator,
    TopicoPorTipoIterator,
    ForumCollection
)

__all__ = [
    'Iterator',
    'TopicoPorTipoIterator',
    'ForumCollection'
]

__version__ = '1.0.0-minimal'
__author__ = 'Equipe DicasDeEstagio'
__description__ = 'Implementação mínima do padrão Iterator integrada com Factory Method'

from .forum_iterators import (
    # Interface abstrata
    Iterator,
    
    # Implementação essencial
    TopicoPorTipoIterator,
    ForumCollection,
)

# Versão do pacote
__version__ = '1.0.0-minimo'

# Metadados do padrão
__pattern_info__ = {
    'pattern_type': 'Behavioral',
    'pattern_name': 'Iterator',
    'version': 'Minimal Implementation',
    'description': 'Permite navegar por tópicos de tipo específico',
    'integration': 'Factory Method Pattern (TopicoFactory)',
    'core_iterator': 'TopicoPorTipoIterator'
}

__all__ = [
    # Interface
    'Iterator',
    
    # Implementação essencial
    'TopicoPorTipoIterator',
    'ForumCollection',
    
    # Metadados
    '__version__',
    '__pattern_info__',
]
