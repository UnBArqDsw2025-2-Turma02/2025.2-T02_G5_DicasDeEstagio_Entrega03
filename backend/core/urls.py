
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet
from Curriculo.views import CurriculoViewSet
from instituicao.views import InstituicaoViewSet
from avaliacao.views import AvaliacaoViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'curriculos', CurriculoViewSet)
router.register(r'avaliacoes', AvaliacaoViewSet)
router.register(r'instituicoes', InstituicaoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/forum/', include('Forum.urls')),
    path('api/auth/', include('users.urls')),
]
