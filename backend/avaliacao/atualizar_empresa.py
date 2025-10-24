from django.core.management.base import BaseCommand
from .models import Empresa
from .open_cnpj import OpenCNPJClient, OpenCNPJAdapter

class Command(BaseCommand):
    help = 'Busca dados de uma empresa na API OpenCNPJ e os salva/atualiza no banco.'

    def add_arguments(self, parser):
        parser.add_argument('cnpj', type=str, help='O CNPJ da empresa a ser buscado.')

    def handle(self, *args, **options):
        cnpj_arg = options['cnpj']
        self.stdout.write(f"CLIENTE: Iniciando busca de dados para o CNPJ: {cnpj_arg}...")

        api_client = OpenCNPJClient()

        adapter = OpenCNPJAdapter(client=api_client)

        empresa_data = adapter.get_empresa_data(cnpj_arg)

        if empresa_data is None:
            self.stderr.write(self.style.ERROR("CLIENTE: Empresa não encontrada ou erro na API."))
            return

        try:
            empresa, created = Empresa.objects.update_or_create(
                cnpj=empresa_data['cnpj'],
                defaults=empresa_data 
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"CLIENTE: Empresa '{empresa.nome}' CRIADA com sucesso!"))
            else:
                self.stdout.write(self.style.SUCCESS(f"CLIENTE: Empresa '{empresa.nome}' ATUALIZADA com sucesso!"))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"CLIENTE: Erro ao salvar no banco: {e}"))