from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import AvaliacaoForm
from .builders import AvaliacaoBuilder

class EnviarAvaliacaoView(LoginRequiredMixin, View):

    form_class = AvaliacaoForm
    template_name = 'core/enviar_avaliacao.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data

            builder = AvaliacaoBuilder()

            try:
                avaliacao_pronta = (builder
                    .set_identificacao(usuario=request.user, empresa=data['empresa'])
                    .set_nota_geral(data['nota_geral'])
                    .add_detalhes_texto(
                        titulo=data['titulo'],
                        pros=data['pros'],
                        contras=data['contras']
                    )
                    .set_contexto_profissional(
                        cargo=data['cargo'],
                        anonimo=data['anonima']
                    )
                    .get_result()
                )
                
                avaliacao_pronta.save()
                
                return redirect('pagina_sucesso')

            except ValueError as e:
                form.add_error(None, str(e))

        return render(request, self.template_name, {'form': form})