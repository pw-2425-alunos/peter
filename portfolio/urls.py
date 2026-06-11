from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('licenciatura/<int:id>/', views.licenciatura_detail, name='licenciatura_detail'),
    path('unidade-curricular/<int:id>/', views.unidade_curricular_detail, name='unidade_curricular_detail'),
    path('projeto/<int:id>/', views.projeto_detail, name='projeto_detail'),
    path('tecnologia/<int:id>/', views.tecnologia_detail, name='tecnologia_detail'),
    path('tfc/<int:id>/', views.tfc_detail, name='tfc_detail'),
    path('competencia/<int:id>/', views.competencia_detail, name='competencia_detail'),
    path('formacao/<int:id>/', views.formacao_detail, name='formacao_detail'),
    path('makingof/<int:id>/', views.makingof_detail, name='makingof_detail'),
    path('docente/<int:id>/', views.docente_detail, name='docente_detail'),
    path('area-interesse/<int:id>/', views.area_interesse_detail, name='area_interesse_detail'),
    path('midia/<int:id>/', views.midia_detail, name='midia_detail'),
    path("projetos/", views.lista_projetos, name="lista_projetos"),
    path("projetos/criar/", views.criar_projeto, name="criar_projeto"),
    path("projetos/<int:id>/editar/", views.editar_projeto, name="editar_projeto"),
    path("projetos/<int:id>/apagar/", views.apagar_projeto, name="apagar_projeto"),
    path("tecnologias/", views.lista_tecnologias, name="lista_tecnologias"),
    path("tecnologias/criar/", views.criar_tecnologia, name="criar_tecnologia"),
    path("tecnologias/<int:id>/editar/", views.editar_tecnologia, name="editar_tecnologia"),
    path("tecnologias/<int:id>/apagar/", views.apagar_tecnologia, name="apagar_tecnologia"),
    path("competencias/", views.lista_competencias, name="lista_competencias"),
    path("competencias/criar/", views.criar_competencia, name="criar_competencia"),
    path("competencias/<int:id>/editar/", views.editar_competencia, name="editar_competencia"),
    path("competencias/<int:id>/apagar/", views.apagar_competencia, name="apagar_competencia"),
    path("formacoes/", views.lista_formacoes, name="lista_formacoes"),
    path("formacoes/criar/", views.criar_formacao, name="criar_formacao"),
    path("formacoes/<int:id>/editar/", views.editar_formacao, name="editar_formacao"),
    path("formacoes/<int:id>/apagar/", views.apagar_formacao, name="apagar_formacao"),
    path("sobre-esta-aplicacao/", views.sobre_aplicacao, name="sobre_aplicacao"),
    path("api/info/", views.api_restful, name="api_restful"),
    path(
    "tarefas-colega/",
    views.tarefas_colega,
    name="tarefas_colega"
    ),
    path(
    "tarefas-colega/criar/",
    views.criar_contrato_colega,
    name="criar_contrato_colega"
    ),
    path(
    "tarefas-colega/<int:id>/",
    views.contrato_detalhe,
    name="contrato_detalhe"
    ),
    path(
    "tarefas-colega/<int:id>/editar/",
    views.editar_contrato_colega,
    name="editar_contrato_colega"
    ),
    path(
    'tarefas-colega/apagar/<int:id>/',
    views.apagar_contrato_colega,
    name='apagar_contrato_colega'
    ),
] 