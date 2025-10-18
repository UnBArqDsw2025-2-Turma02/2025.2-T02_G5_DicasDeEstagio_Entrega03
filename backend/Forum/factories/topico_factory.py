from abc import ABC, abstractmethod
from django.utils import timezone
from ..models import Forum


class TopicoCreator(ABC):
    
    @abstractmethod
    def create_topico(self, user, titulo, conteudo, **kwargs):
        pass
    
    def validar_conteudo(self, titulo, conteudo):
        if not titulo or len(titulo.strip()) < 5:
            raise ValueError("Título deve ter pelo menos 5 caracteres")
        
        if not conteudo or len(conteudo.strip()) < 10:
            raise ValueError("Conteúdo deve ter pelo menos 10 caracteres")
        
        return True
    
    def formatar_titulo(self, titulo, prefixo):
        titulo_limpo = titulo.strip()
        if not titulo_limpo.startswith(f"[{prefixo}]"):
            return f"[{prefixo}] {titulo_limpo}"
        return titulo_limpo


class TopicoVagaCreator(TopicoCreator):
    # cria topicos de vagas de emprego/estagio
    def create_topico(self, user, titulo, conteudo, salario=None, requisitos=None, 
                     empresa=None, tipo_vaga="Estágio", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"VAGA - {tipo_vaga.upper()}")
        
        conteudo_enriquecido = conteudo
        
        if empresa:
            conteudo_enriquecido += f"\n\n**Empresa:** {empresa}"
        
        if salario:
            conteudo_enriquecido += f"\n**Salário:** {salario}"
        
        if requisitos:
            conteudo_enriquecido += f"\n**Requisitos:** {requisitos}"
        
        conteudo_enriquecido += f"\n\n**Tipo de Vaga:** {tipo_vaga}"
        conteudo_enriquecido += f"\n**Publicado em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDuvidaCreator(TopicoCreator):
    # cria topicos de duvidas sobre carreiraa
    def create_topico(self, user, titulo, conteudo, categoria="Geral", 
                     urgencia="Normal", tags=None, **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"DÚVIDA - {categoria.upper()}")
        
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n**Categoria:** {categoria}"
        conteudo_enriquecido += f"\n**Urgência:** {urgencia}"
        
        if tags:
            tags_str = ", ".join(tags) if isinstance(tags, list) else tags
            conteudo_enriquecido += f"\n**Tags:** {tags_str}"
        
        if urgencia.lower() == "alta":
            conteudo_enriquecido += f"\n\n**URGENTE:** Preciso de ajuda rapidamente!"
        
        conteudo_enriquecido += f"\n\n**Pergunta feita em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Aguardando respostas da comunidade...**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoExperienciaCreator(TopicoCreator):
    # cria topicos de relatos de experiências
    def create_topico(self, user, titulo, conteudo, empresa=None, periodo=None, 
                     area=None, nota_experiencia=None, **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, "EXPERIÊNCIA")
        
        conteudo_enriquecido = conteudo
        
        if empresa:
            conteudo_enriquecido += f"\n\n**Empresa:** {empresa}"
        
        if periodo:
            conteudo_enriquecido += f"\n**Período:** {periodo}"
        
        if area:
            conteudo_enriquecido += f"\n**Área:** {area}"
        
        if nota_experiencia:
            estrelas = "*" * int(nota_experiencia)
            conteudo_enriquecido += f"\n**Avaliação:** {estrelas} ({nota_experiencia}/5)"
        
        conteudo_enriquecido += f"\n\n**Compartilhado em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Compartilhe sua experiência também!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDicaCreator(TopicoCreator):
    # cria topicos de dicas de carreira
    def create_topico(self, user, titulo, conteudo, categoria_dica="Carreira", 
                     nivel="Iniciante", aplicabilidade="Geral", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"DICA - {categoria_dica.upper()}")
        
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n**Categoria:** {categoria_dica}"
        conteudo_enriquecido += f"\n**Nível:** {nivel}"
        conteudo_enriquecido += f"\n**Aplicabilidade:** {aplicabilidade}"
        
        if nivel.lower() == "iniciante":
            conteudo_enriquecido += f"\n\n**Perfeito para quem está começando!**"
        elif nivel.lower() == "avançado":
            conteudo_enriquecido += f"\n\n**Para quem já tem experiência!**"
        
        conteudo_enriquecido += f"\n\n**Dica compartilhada em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Ajudou? Deixe um comentário!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoDiscussaoCreator(TopicoCreator):
    # cria topicos de discussões gerais
    def create_topico(self, user, titulo, conteudo, tema="Geral", 
                     tipo_discussao="Aberta", **kwargs):
        self.validar_conteudo(titulo, conteudo)
        
        titulo_formatado = self.formatar_titulo(titulo, f"DISCUSSÃO - {tema.upper()}")
        
        conteudo_enriquecido = conteudo
        conteudo_enriquecido += f"\n\n**Tema:** {tema}"
        conteudo_enriquecido += f"\n**Tipo:** {tipo_discussao}"
        
        conteudo_enriquecido += f"\n\n**Discussão iniciada em:** {timezone.now().strftime('%d/%m/%Y às %H:%M')}"
        conteudo_enriquecido += f"\n**Participe! Queremos ouvir sua opinião!**"
        
        topico = Forum.objects.create(
            user=user,
            titulo=titulo_formatado,
            conteudo=conteudo_enriquecido,
            visualizacoes=0,
            is_active=True
        )
        
        return topico


class TopicoFactory:
    # topico = TopicoFactory.create_topico('vaga', user, titulo, conteudo, empresa='TechCorp')
    _creators = {
        'vaga': TopicoVagaCreator(),
        'duvida': TopicoDuvidaCreator(),
        'experiencia': TopicoExperienciaCreator(),
        'dica': TopicoDicaCreator(),
        'discussao': TopicoDiscussaoCreator(),
    }
    
    @classmethod
    def get_creator(cls, tipo_topico):
        creator = cls._creators.get(tipo_topico.lower())
        if not creator:
            raise ValueError(f"Tipo de tópico '{tipo_topico}' não suportado. "
                           f"Tipos disponíveis: {list(cls._creators.keys())}")
        return creator
    
    @classmethod
    def create_topico(cls, tipo_topico, user, titulo, conteudo, **kwargs):
        creator = cls.get_creator(tipo_topico)
        return creator.create_topico(user, titulo, conteudo, **kwargs)
    
    @classmethod
    def get_tipos_disponiveis(cls):
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
