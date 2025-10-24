from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AvaliacaoForm
from .builders import AvaliacaoBuilder 
from .memento_avaliacao import EditorAvaliacao, HistoricoAvaliacao 

class EnviarAvaliacaoView(LoginRequiredMixin, View):
    form_class = AvaliacaoForm
    template_name = 'core/enviar_avaliacao.html'

    def get(self, request, *args, **kwargs):
        editor = EditorAvaliacao()
        historico = HistoricoAvaliacao(request)
        
        rascunho_salvo = historico.carregar_rascunho()
        if rascunho_salvo:
            editor.restaurar_de_memento(rascunho_salvo)
            messages.info(request, "Um rascunho salvo foi carregado.")
        
        form = self.form_class(initial=editor.get_state())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        action = request.POST.get('action')
        
        editor = EditorAvaliacao()
        historico = HistoricoAvaliacao(request)
        
        editor.set_state_from_dict(request.POST)

        if action == 'save_draft':
            memento = editor.salvar_para_memento()
            historico.salvar_rascunho(memento)
            messages.success(request, "Rascunho salvo com sucesso!")

            form = self.form_class(initial=editor.get_state())
            return render(request, self.template_name, {'form': form})

        elif action == 'submit':
            if form.is_valid():
                data = form.cleaned_data
                builder = AvaliacaoBuilder()
                try:
                    avaliacao_pronta = (builder
                        .set_identificacao(usuario=request.user, empresa=data['empresa'])
                        .set_nota_geral(data['nota_geral'])
                        .add_detalhes_texto(data['titulo'], data['pros'], data['contras'])
                        .set_contexto_profissional(data['cargo'], data['anonima'])
                        .get_result()
                    )
                    avaliacao_pronta.save()
                    
                    historico.limpar_rascunho() 
                    messages.success(request, "Avaliação enviada com sucesso!")
                    return redirect('pagina_sucesso')
                
                except (ValueError, TypeError) as e:
                    messages.error(request, f"Erro ao enviar: {e}. Verifique os campos obrigatórios.")
            

            return render(request, self.template_name, {'form': form})
