from abc import ABC, abstractmethod
from django.utils import timezone
from ..models import Forum


class TopicoCreator(ABC):
    """
    Classe abstrata para criação de diferentes tipos de tópicos do fórum
    """
    
    @abstractmethod
    def create_topico(self, user, titulo, conteudo, **kwargs):
        """
        Método abstrato para criar um tópico
        
        Args:
            user: Usuário que está criando o tópico
            titulo: Título do tópico
            conteudo: Conteúdo do tópico
            **kwargs: Parâmetros específicos para cada tipo de tópico
        """
        pass
    
    def validar_conteudo(self, titulo, conteudo):
        """Método comum para validar título e conteúdo"""
        if not titulo or len(titulo.strip()) < 5:
            raise ValueError("Título deve ter pelo menos 5 caracteres")
        
        if not conteudo or len(conteudo.strip()) < 10:
            raise ValueError("Conteúdo deve ter pelo menos 10 caracteres")
        
        return True
    
    def formatar_titulo(self, titulo, prefixo):
        """Método auxiliar para formatar título com prefixo"""
        titulo_limpo = titulo.strip()
        if not titulo_limpo.startswith(f"[{prefixo}]"):
            return f"[{prefixo}] {titulo_limpo}"
        return titulo_limpo


class TopicoVagaCreator(TopicoCreator):
    """
    Factory para criar tópicos de vagas de estágio/emprego
    """
    
    def create_topico(self, user, titulo, conteudo, salario=None, requisitos=None, 
                     empresa=None, tipo_vaga="Estágio", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        # Formatar título com prefixo de vaga
        titulo_formatado = self.formatar_titulo(titulo, f"VAGA - {tipo_vaga.upper()}")
        
        # Enriquecer o conteúdo com informações específicas da vaga
        conteudo_enriquecido = conteudo
        
        if empresa:
            conteudo_enriquecido += f"\n\n🏢 **Empresa:** {empresa}"
        
        if salario:
            conteudo_enriquecido += f"\n💰 **Salário:** {salario}"
        
        if requisitos:
            conteudo_enriquecido += f"\n📋 **Requisitos:** {requisitos}"
        
        conteudo_enriquecido += f"\n\n🏷️ **Tipo de Vaga:** {tipo_vaga}"
        conteudo_enriquecido += f"\n📅 **Publicado em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDuvidaCreator(TopicoCreator):
    """
    Factory para criar tópicos de dúvidas sobre estágios
    """
    
    def create_topico(self, user, titulo, conteudo, categoria="Geral", 
                     urgencia="Normal", tags=None, **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        # Formatar título com prefixo de dúvida
        titulo_formatado = self.formatar_titulo(titulo, f"DÚVIDA - {categoria.upper()}")
        
        # Adicionar informações específicas da dúvida
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n📂 **Categoria:** {categoria}"
        conteudo_enriquecido += f"\n⚡ **Urgência:** {urgencia}"
        
        if tags:
            tags_str = ", ".join(tags) if isinstance(tags, list) else tags
            conteudo_enriquecido += f"\n🏷️ **Tags:** {tags_str}"
        
        # Adicionar call-to-action para respostas
        if urgencia.lower() == "alta":
            conteudo_enriquecido += f"\n\n🚨 **URGENTE:** Preciso de ajuda rapidamente!"
        
        conteudo_enriquecido += f"\n\n📅 **Pergunta feita em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n👥 **Aguardando respostas da comunidade...**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoExperienciaCreator(TopicoCreator):
    """
    Factory para criar tópicos de compartilhamento de experiências
    """
    
    def create_topico(self, user, titulo, conteudo, empresa=None, periodo=None, 
                     area=None, nota_experiencia=None, **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        # Formatar título com prefixo de experiência
        titulo_formatado = self.formatar_titulo(titulo, "EXPERIÊNCIA")
        
        # Enriquecer conteúdo com detalhes da experiência
        conteudo_enriquecido = conteudo
        
        if empresa:
            conteudo_enriquecido += f"\n\n🏢 **Empresa:** {empresa}"
        
        if periodo:
            conteudo_enriquecido += f"\n📅 **Período:** {periodo}"
        
        if area:
            conteudo_enriquecido += f"\n💼 **Área:** {area}"
        
        if nota_experiencia:
            estrelas = "⭐" * int(nota_experiencia)
            conteudo_enriquecido += f"\n⭐ **Avaliação:** {estrelas} ({nota_experiencia}/5)"
        
        conteudo_enriquecido += f"\n\n📖 **Compartilhado em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n💬 **Compartilhe sua experiência também!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDicaCreator(TopicoCreator):
    """
    Factory para criar tópicos de dicas sobre estágios e carreira
    """
    
    def create_topico(self, user, titulo, conteudo, categoria_dica="Carreira", 
                     nivel="Iniciante", aplicabilidade="Geral", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        # Formatar título com prefixo de dica
        titulo_formatado = self.formatar_titulo(titulo, f"DICA - {categoria_dica.upper()}")
        
        # Enriquecer conteúdo com informações da dica
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n💡 **Categoria:** {categoria_dica}"
        conteudo_enriquecido += f"\n🎯 **Nível:** {nivel}"
        conteudo_enriquecido += f"\n🌐 **Aplicabilidade:** {aplicabilidade}"
        
        # Adicionar call-to-action baseado no nível
        if nivel.lower() == "iniciante":
            conteudo_enriquecido += f"\n\n🌱 **Perfeito para quem está começando!**"
        elif nivel.lower() == "avançado":
            conteudo_enriquecido += f"\n\n🚀 **Para quem já tem experiência!**"
        
        conteudo_enriquecido += f"\n\n📅 **Dica compartilhada em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n👍 **Ajudou? Deixe um comentário!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDiscussaoCreator(TopicoCreator):
    """
    Factory para criar tópicos de discussão geral
    """
    
    def create_topico(self, user, titulo, conteudo, tema="Geral", 
                     tipo_discussao="Aberta", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        # Formatar título com prefixo de discussão
        titulo_formatado = self.formatar_titulo(titulo, f"DISCUSSÃO - {tema.upper()}")
        
        # Enriquecer conteúdo
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n🗣️ **Tema:** {tema}"
        conteudo_enriquecido += f"\n💭 **Tipo:** {tipo_discussao}"
        
        # Adicionar call-to-action para participação
        conteudo_enriquecido += f"\n\n📅 **Discussão iniciada em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n💬 **Participe! Queremos ouvir sua opinião!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoFactory:
    """
    Factory principal que gerencia os diferentes tipos de criadores de tópicos
    """
    
    _creators = {
        'vaga': TopicoVagaCreator(),
        'duvida': TopicoDuvidaCreator(),
        'experiencia': TopicoExperienciaCreator(),
        'dica': TopicoDicaCreator(),
        'discussao': TopicoDiscussaoCreator(),
    }
    
    @classmethod
    def get_creator(cls, tipo_topico):
        """
        Retorna o creator apropriado baseado no tipo de tópico
        
        Args:
            tipo_topico: Tipo do tópico ('vaga', 'duvida', 'experiencia', 'dica', 'discussao')
        
        Returns:
            TopicoCreator: O creator apropriado
        """
        creator = cls._creators.get(tipo_topico.lower())
        if not creator:
            raise ValueError(f"Tipo de tópico '{tipo_topico}' não suportado. "
                           f"Tipos disponíveis: {list(cls._creators.keys())}")
        return creator
    
    @classmethod
    def create_topico(cls, tipo_topico, user, titulo, conteudo, **kwargs):
        """
        Método de conveniência para criar um tópico
        
        Args:
            tipo_topico: Tipo do tópico
            user: Usuário que está criando o tópico
            titulo: Título do tópico
            conteudo: Conteúdo do tópico
            **kwargs: Parâmetros específicos para cada tipo
        
        Returns:
            Forum: O tópico criado
        """
        creator = cls.get_creator(tipo_topico)
        return creator.create_topico(user, titulo, conteudo, **kwargs)
    
    @classmethod
    def get_tipos_disponiveis(cls):
        """
        Retorna informações sobre os tipos de tópicos disponíveis
        """
        return {
            'vaga': {
                'nome': 'Vaga de Estágio/Emprego',
                'descricao': 'Para publicar oportunidades de estágio ou emprego',
                'campos_extras': ['salario', 'requisitos', 'empresa', 'tipo_vaga'],
                'exemplo': 'Vaga para desenvolvedor Python júnior'
            },
            'duvida': {
                'nome': 'Dúvida sobre Estágios',
                'descricao': 'Para fazer perguntas sobre estágios e carreira',
                'campos_extras': ['categoria', 'urgencia', 'tags'],
                'exemplo': 'Como me preparar para entrevista técnica?'
            },
            'experiencia': {
                'nome': 'Compartilhar Experiência',
                'descricao': 'Para compartilhar experiências de estágio',
                'campos_extras': ['empresa', 'periodo', 'area', 'nota_experiencia'],
                'exemplo': 'Minha experiência como estagiário na empresa X'
            },
            'dica': {
                'nome': 'Dica de Carreira',
                'descricao': 'Para compartilhar dicas úteis sobre carreira',
                'campos_extras': ['categoria_dica', 'nivel', 'aplicabilidade'],
                'exemplo': 'Como criar um LinkedIn profissional'
            },
            'discussao': {
                'nome': 'Discussão Geral',
                'descricao': 'Para iniciar discussões sobre temas diversos',
                'campos_extras': ['tema', 'tipo_discussao'],
                'exemplo': 'O que vocês acham do home office para estagiários?'
            }
        }
