
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from users.views import UserViewSet
from Curriculo.views import CurriculoViewSet
from instituicao.views import InstituicaoViewSet
from avaliacao.views import AvaliacaoViewSet
from Forum.views import ForumViewSet, ComentarioForumViewSet

routers = routers.DefaultRouter()
routers.register(r'users', UserViewSet)
routers.register(r'curriculos', CurriculoViewSet)
routers.register(r'avaliacoes', AvaliacaoViewSet)
routers.register(r'instituicoes', InstituicaoViewSet)
routers.register(r'forum', ForumViewSet)
routers.register(r'comentarios', ComentarioForumViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(routers.urls)),
]
