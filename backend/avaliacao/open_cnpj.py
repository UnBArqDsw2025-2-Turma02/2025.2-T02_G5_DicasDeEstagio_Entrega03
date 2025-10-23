import requests
import re
from typing import Dict, Any, Optional

class OpenCNPJClient:

    BASE_URL = "https://publica.cnpj.ws/cnpj/"

    def _limpar_cnpj(self, cnpj: str) -> str:
        return re.sub(r'[^0-9]', '', cnpj)

    def buscar_por_cnpj(self, cnpj: str) -> Optional[Dict[str, Any]]:

        cnpj_limpo = self._limpar_cnpj(cnpj)
        url = f"{self.BASE_URL}{cnpj_limpo}"
        
        print(f"ADAPTEE: Buscando dados brutos em: {url}")
        
        try:

            response = requests.get(url, timeout=5)
            
            response.raise_for_status() 
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print(f"ADAPTEE: CNPJ {cnpj} não encontrado (404).")
                return None
            print(f"ADAPTEE: Erro HTTP: {e}")
            raise 
            
        except requests.exceptions.RequestException as e:
            print(f"ADAPTEE: Erro de conexão: {e}")
            raise

class OpenCNPJAdapter:
    def __init__(self, client: OpenCNPJClient):
        self._client = client

    def get_empresa_data(self, cnpj: str) -> Optional[Dict[str, Any]]:
        try:
            dados_brutos = self._client.buscar_por_cnpj(cnpj)
            
            if dados_brutos is None:
                return None

            print("ADAPTER: Traduzindo dados brutos para o formato interno...")

            estabelecimento = dados_brutos.get("estabelecimento", {})
            cidade = estabelecimento.get("cidade", {})
            estado = estabelecimento.get("estado", {})

            traduzido = {
                'cnpj': dados_brutos.get("cnpj"),
                'nome': dados_brutos.get("razao_social"),
                'nome_fantasia': dados_brutos.get("nome_fantasia"),
                'cidade': cidade.get("nome"),
                'uf': estado.get("sigla"),
                'logradouro': estabelecimento.get("logradouro"),
                'numero': estabelecimento.get("numero"),
                'bairro': estabelecimento.get("bairro"),
            }

            print(f"ADAPTER: Dados traduzidos com sucesso.")
            return traduzido

        except Exception as e:
            print(f"ADAPTER: Erro durante o processo de busca ou tradução: {e}")
            return None