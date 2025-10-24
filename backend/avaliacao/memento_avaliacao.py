from __future__ import annotations
from typing import Dict, Any, Optional

class AvaliacaoMemento:
    def __init__(self, state: Dict[str, Any]):
        self._state = state.copy()

    def get_state(self) -> Dict[str, Any]:
        return self._state

class EditorAvaliacao:
    _state: Dict[str, Any]

    def __init__(self, state: Dict[str, Any] = None):
        self._state = state or self.get_empty_state()

    def get_empty_state(self) -> Dict[str, Any]:
        return {
            'titulo': '', 'pros': '', 'contras': '',
            'nota_geral': None, 'cargo': '', 'anonima': False,
            'empresa': None 
        }
    
    def set_state_from_dict(self, data: Dict[str, Any]):
        self._state = {
            'titulo': data.get('titulo', ''),
            'pros': data.get('pros', ''),
            'contras': data.get('contras', ''),
            'nota_geral': data.get('nota_geral'),
            'cargo': data.get('cargo', ''),
            'anonima': bool(data.get('anonima')),
            'empresa': data.get('empresa')
        }

    def get_state(self) -> Dict[str, Any]:
        return self._state

    def salvar_para_memento(self) -> AvaliacaoMemento:
        return AvaliacaoMemento(self._state)

    def restaurar_de_memento(self, memento: AvaliacaoMemento):
        self._state = memento.get_state()

class HistoricoAvaliacao:
    SESSION_KEY = 'avaliacao_draft'

    def __init__(self, request):
        self.request = request

    def salvar_rascunho(self, memento: AvaliacaoMemento):
        self.request.session[self.SESSION_KEY] = memento.get_state()
        self.request.session.modified = True
        print(f"RASCUNHO SALVO: {memento.get_state()}")

    def carregar_rascunho(self) -> Optional[AvaliacaoMemento]:
        state = self.request.session.get(self.SESSION_KEY)
        if state:
            print(f"RASCUNHO CARREGADO: {state}")
            return AvaliacaoMemento(state)
        return None

    def limpar_rascunho(self):
        if self.SESSION_KEY in self.request.session:
            del self.request.session[self.SESSION_KEY]
            print("RASCUNHO LIMPO.")