from abc import ABC, abstractmethod
from django.utils import timezone
from ..models import Avaliacao


class AvaliacaoCreator(ABC):
    """
    Classe abstrata para criação de diferentes tipos de avaliação
    """
    
    @abstractmethod
    def create_avaliacao(self, user, nota, comentario, **kwargs):
        """
        Método abstrato para criar uma avaliação
        
        Args:
            user: Usuário que está fazendo a avaliação
            nota: Nota da avaliação (1-5)
            comentario: Comentário da avaliação
            **kwargs: Parâmetros específicos para cada tipo de avaliação
        """
        pass
    
    def validar_nota(self, nota):
        """Método comum para validar a nota"""
        if not isinstance(nota, int) or nota < 1 or nota > 5:
            raise ValueError("Nota deve ser um inteiro entre 1 e 5")
        return True


class AvaliacaoEstagioCreator(AvaliacaoCreator):
    """
    Factory para criar avaliações de estágio
    """
    
    def create_avaliacao(self, user, nota, comentario, data_inicio=None, data_fim=None, **kwargs):
        self.validar_nota(nota)
        
        # Se as datas não forem fornecidas, usa datas padrão baseadas no estágio
        if not data_inicio:
            data_inicio = timezone.now() - timezone.timedelta(days=180)  # 6 meses atrás
        if not data_fim:
            data_fim = timezone.now()
        
        avaliacao = Avaliacao.objects.create(
            user=user,
            nota=nota,
            comentario=f"[ESTÁGIO] {comentario}",
            datainicio=data_inicio,
            datafim=data_fim
        )
        
        return avaliacao


class AvaliacaoEmpresaCreator(AvaliacaoCreator):
    """
    Factory para criar avaliações de empresas/instituições
    """
    
    def create_avaliacao(self, user, nota, comentario, instituicao=None, **kwargs):
        self.validar_nota(nota)
        
        # Data padrão para avaliação de empresa (experiência geral)
        data_atual = timezone.now()
        
        # Adiciona contexto de empresa no comentário
        comentario_empresa = f"[EMPRESA] {comentario}"
        if instituicao:
            comentario_empresa += f" - Empresa: {instituicao.nome}"
        
        avaliacao = Avaliacao.objects.create(
            user=user,
            nota=nota,
            comentario=comentario_empresa,
            datainicio=data_atual,
            datafim=data_atual
        )
        
        return avaliacao


class AvaliacaoProcessoSeletivoCreator(AvaliacaoCreator):
    """
    Factory para criar avaliações de processos seletivos
    """
    
    def create_avaliacao(self, user, nota, comentario, tipo_processo="Entrevista", **kwargs):
        self.validar_nota(nota)
        
        data_atual = timezone.now()
        
        # Adiciona contexto do processo seletivo
        comentario_processo = f"[PROCESSO SELETIVO - {tipo_processo.upper()}] {comentario}"
        
        avaliacao = Avaliacao.objects.create(
            user=user,
            nota=nota,
            comentario=comentario_processo,
            datainicio=data_atual,
            datafim=data_atual
        )
        
        return avaliacao


class AvaliacaoFactory:
    """
    Factory principal que gerencia os diferentes tipos de criadores de avaliação
    """
    
    _creators = {
        'estagio': AvaliacaoEstagioCreator(),
        'empresa': AvaliacaoEmpresaCreator(),
        'processo_seletivo': AvaliacaoProcessoSeletivoCreator(),
    }
    
    @classmethod
    def get_creator(cls, tipo_avaliacao):
        """
        Retorna o creator apropriado baseado no tipo de avaliação
        
        Args:
            tipo_avaliacao: Tipo da avaliação ('estagio', 'empresa', 'processo_seletivo')
        
        Returns:
            AvaliacaoCreator: O creator apropriado
        """
        creator = cls._creators.get(tipo_avaliacao.lower())
        if not creator:
            raise ValueError(f"Tipo de avaliação '{tipo_avaliacao}' não suportado. "
                           f"Tipos disponíveis: {list(cls._creators.keys())}")
        return creator
    
    @classmethod
    def create_avaliacao(cls, tipo_avaliacao, user, nota, comentario, **kwargs):
        """
        Método de conveniência para criar uma avaliação
        
        Args:
            tipo_avaliacao: Tipo da avaliação
            user: Usuário que está fazendo a avaliação
            nota: Nota da avaliação (1-5)
            comentario: Comentário da avaliação
            **kwargs: Parâmetros específicos para cada tipo
        
        Returns:
            Avaliacao: A avaliação criada
        """
        creator = cls.get_creator(tipo_avaliacao)
        return creator.create_avaliacao(user, nota, comentario, **kwargs)
