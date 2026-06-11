from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .forms import MagicLinkForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.core.management import call_command
from django.http import HttpResponse

import io
from .forms import (
    TecnologiaForm,
    CompetenciaForm,
    FormacaoForm,
    ProjetoForm
)
from .models import (
    Licenciatura,
    UnidadeCurricular,
    Projeto,
    Tecnologia,
    TFC,
    Competencia,
    Formacao,
    MakingOf,
    Docente,
    AreaInteresse,
    Midia,
)

import requests


def contrato_detalhe(request, id):

    headers = {
        "accept": "application/json"
    }

    try:

        response = requests.get(
            f"https://francisco-pearson-22308485.pw.deisi.ulusofona.pt/contratos/api/contratos/{id}/",
            headers=headers,
            verify=False
        )

        if response.status_code == 200:

            contrato = response.json()

            return render(
                request,
                "portfolio/contrato_detalhe.html",
                {
                    "contrato": contrato
                }
            )

        return render(
            request,
            "portfolio/contrato_detalhe.html",
            {
                "erro": f"Erro {response.status_code}"
            }
        )

    except Exception as e:

        return render(
            request,
            "portfolio/contrato_detalhe.html",
            {
                "erro": str(e)
            }
        )

def criar_contrato_colega(request):

    erro = None

    if request.method == "POST":

        dados = {
            "titulo": request.POST.get("titulo"),
            "tipo": request.POST.get("tipo"),
            "texto_original": request.POST.get("texto_original"),
            "jurisdicao": request.POST.get("jurisdicao"),
            "etiqueta_ids": []
        }

        try:

            headers = {
                "X-API-Key": "FWo8NeiWN-pHA8aGkK53oDBAZ1N10D53AXwiOHexsf0"
                }

            response = requests.post(
                "https://francisco-pearson-22308485.pw.deisi.ulusofona.pt/contratos/api/contratos/",
                json=dados,
                headers=headers,
                verify=False
                )

            if response.status_code in [200, 201]:
                return redirect("tarefas_colega")

            erro = f"Erro {response.status_code} - {response.text}"

        except Exception as e:
            erro = str(e)

    return render(
        request,
        "portfolio/contrato_form.html",
        {
            "erro": erro
        }
    )

def tarefas_colega(request):

    headers = {
        "accept": "application/json"
    }

    params = {}

    if request.GET.get("jurisdicao"):
        params["jurisdicao"] = request.GET.get("jurisdicao")

    if request.GET.get("tipo"):
        params["tipo"] = request.GET.get("tipo")

    try:

        response = requests.get(
            "https://francisco-pearson-22308485.pw.deisi.ulusofona.pt/contratos/api/contratos/",
            headers=headers,
            params=params,
            verify=False
        )

        if response.status_code == 200:
            contratos = response.json()
            erro = None
        else:
            contratos = []
            erro = f"Erro {response.status_code}"

    except Exception as e:
        contratos = []
        erro = str(e)

    return render(
        request,
        "portfolio/colega_lista.html",
        {
            "contratos": contratos,
            "erro": erro
        }
    )

def export_database(request):
    buffer = io.StringIO()

    call_command(
        'dumpdata',
        exclude=['contenttypes', 'auth.permission', 'sessions'],
        stdout=buffer
    )

    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/json'
    )

    response['Content-Disposition'] = 'attachment; filename="db.json"'

    return response


# MAGIC LINK

def magic_link_request_view(request):
    mensagem = None

    if request.method == "POST":
        form = MagicLinkForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            try:
                user = User.objects.get(email=email)

                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)

                magic_url = request.build_absolute_uri(
                    reverse("accounts:magic_login", kwargs={
                        "uidb64": uid,
                        "token": token
                    })
                )

                send_mail(
                    "Link mágico de login",
                    f"Clica neste link para entrar no portfólio:\n\n{magic_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )

            except User.DoesNotExist:
                pass

            mensagem = "Se o email existir, foi enviado um link mágico."

    else:
        form = MagicLinkForm()

    return render(request, "accounts/magic_link.html", {
        "form": form,
        "mensagem": mensagem
    })


def magic_login_view(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except Exception:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        login(request, user)
        return redirect("home")

    return render(request, "accounts/magic_link_invalid.html")

# SOBRE APLICACAO

def is_gestor_portfolio(user):
    return user.is_authenticated and user.groups.filter(name="gestor-portfolio").exists()

def sobre_aplicacao(request):
    return render(request, 'portfolio/sobre_aplicacao.html')

def api_restful(request):
    return render(request, "portfolio/api_restful.html")


# PROJETOS

def lista_projetos(request):
    dados = Projeto.objects.all()
    return render(request, "portfolio/projetos.html", {
        "dados": dados,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def criar_projeto(request):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    form = ProjetoForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("lista_projetos")

    return render(request, "portfolio/projeto_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def editar_projeto(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    projeto = get_object_or_404(Projeto, id=id)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)

    if form.is_valid():
        form.save()
        return redirect("lista_projetos")

    return render(request, "portfolio/projeto_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def apagar_projeto(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    projeto = get_object_or_404(Projeto, id=id)

    if request.method == "POST":
        projeto.delete()
        return redirect("lista_projetos")

    return render(request, "portfolio/projeto_confirm_delete.html", {
        "projeto": projeto,
        "is_gestor": is_gestor_portfolio(request.user)
    })


# TECNOLOGIAS


def lista_tecnologias(request):
    dados = Tecnologia.objects.all()
    return render(request, "portfolio/tecnologias.html", {
        "dados": dados,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def criar_tecnologia(request):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    form = TecnologiaForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("lista_tecnologias")

    return render(request, "portfolio/tecnologia_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def editar_tecnologia(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    tecnologia = get_object_or_404(Tecnologia, id=id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)

    if form.is_valid():
        form.save()
        return redirect("lista_tecnologias")

    return render(request, "portfolio/tecnologia_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def apagar_tecnologia(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    tecnologia = get_object_or_404(Tecnologia, id=id)

    if request.method == "POST":
        tecnologia.delete()
        return redirect("lista_tecnologias")

    return render(request, "portfolio/tecnologia_confirm_delete.html", {
        "tecnologia": tecnologia,
        "is_gestor": is_gestor_portfolio(request.user)
    })


# COMPETÊNCIAS


def lista_competencias(request):
    dados = Competencia.objects.all()
    return render(request, "portfolio/competencias.html", {
        "dados": dados,
        "is_gestor": is_gestor_portfolio(request.user)
    })


@login_required
def criar_competencia(request):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    form = CompetenciaForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("lista_competencias")

    return render(request, "portfolio/competencia_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def editar_competencia(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    competencia = get_object_or_404(Competencia, id=id)
    form = CompetenciaForm(request.POST or None, instance=competencia)

    if form.is_valid():
        form.save()
        return redirect("lista_competencias")

    return render(request, "portfolio/competencia_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def apagar_competencia(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    competencia = get_object_or_404(Competencia, id=id)

    if request.method == "POST":
        competencia.delete()
        return redirect("lista_competencias")

    return render(request, "portfolio/competencia_confirm_delete.html", {
        "competencia": competencia,
        "is_gestor": is_gestor_portfolio(request.user)
    })


# FORMAÇÕES

def lista_formacoes(request):
    dados = Formacao.objects.all()
    return render(request, "portfolio/formacoes.html", {
        "dados": dados,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def criar_formacao(request):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    form = FormacaoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect("lista_formacoes")

    return render(request, "portfolio/formacao_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def editar_formacao(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    formacao = get_object_or_404(Formacao, id=id)
    form = FormacaoForm(request.POST or None, instance=formacao)

    if form.is_valid():
        form.save()
        return redirect("lista_formacoes")

    return render(request, "portfolio/formacao_form.html", {
        "form": form,
        "is_gestor": is_gestor_portfolio(request.user)
    })

@login_required
def apagar_formacao(request, id):
    if not is_gestor_portfolio(request.user):
        return redirect("home")

    formacao = get_object_or_404(Formacao, id=id)

    if request.method == "POST":
        formacao.delete()
        return redirect("lista_formacoes")

    return render(request, "portfolio/formacao_confirm_delete.html", {
        "formacao": formacao,
        "is_gestor": is_gestor_portfolio(request.user)
    })

def build_detail_context(obj, title, fields, image_attr=None, related_sections=None):
    details = []

    for label, value in fields:
        if value is not None and value != "":
            details.append((label, value))

    image_url = None
    if image_attr:
        image_field = getattr(obj, image_attr, None)
        if image_field:
            try:
                image_url = image_field.url
            except Exception:
                image_url = None

    return {
        "page_title": title,
        "object_name": str(obj),
        "details": details,
        "image_url": image_url,
        "related_sections": related_sections or [],
    }


def licenciatura_detail(request, id):
    obj = get_object_or_404(Licenciatura, id=id)

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Licenciatura",
        image_attr="imagem",
        fields=[
            ("Nome", obj.nome),
            ("Número de semestres", obj.numero_semestres),
            ("ECTS total", obj.ects_total),
            ("Descrição", obj.descricao),
            ("Objetivo", obj.objetivo),
            ("Website", obj.url_website),
            ("Saídas profissionais", obj.saidas_profissionais),
        ],
        related_sections=[
            ("Unidades Curriculares", obj.unidades_curriculares.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def unidade_curricular_detail(request, id):
    obj = get_object_or_404(
        UnidadeCurricular.objects.select_related("licenciatura").prefetch_related("docentes", "projetos", "midias"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Unidade Curricular",
        image_attr="imagem",
        fields=[
            ("Nome", obj.nome),
            ("Licenciatura", obj.licenciatura),
            ("Ano curricular", obj.ano_curricular),
            ("Semestre", obj.semestre),
            ("ECTS", obj.ects),
            ("Apresentação", obj.apresentacao),
            ("Programa", obj.programa),
            ("Objetivos", obj.objectivos),
            ("Website", obj.url_website),
        ],
        related_sections=[
            ("Docentes", obj.docentes.all()),
            ("Projetos", obj.projetos.all()),
            ("Mídias", obj.midias.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def projeto_detail(request, id):
    obj = get_object_or_404(
        Projeto.objects.select_related("unidade_curricular", "area_interesse")
        .prefetch_related("tecnologias", "competencias", "makingofs", "midias"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe do Projeto",
        image_attr="imagem",
        fields=[
            ("Título", obj.titulo),
            ("Unidade Curricular", obj.unidade_curricular),
            ("Área de interesse", obj.area_interesse),
            ("Descrição", obj.descricao),
            ("Conceitos aplicados", obj.conceitos_aplicados),
            ("Ano de realização", obj.ano_realizacao),
            ("Estado", obj.estado),
            ("Destaque", "Sim" if obj.destaque else "Não"),
        ],
        related_sections=[
            ("Tecnologias", obj.tecnologias.all()),
            ("Competências", obj.competencias.all()),
            ("Making Of", obj.makingofs.all()),
            ("Mídias", obj.midias.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def tecnologia_detail(request, id):
    obj = get_object_or_404(
        Tecnologia.objects.prefetch_related("projetos", "formacoes", "tfcs", "makingofs", "midias"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Tecnologia",
        image_attr="logo",
        fields=[
            ("Nome", obj.nome),
            ("Tipo", obj.tipo),
            ("Descrição", obj.descricao),
            ("Website", obj.url_website),
            ("Observações", obj.observacoes),
        ],
        related_sections=[
            ("Projetos", obj.projetos.all()),
            ("Formações", obj.formacoes.all()),
            ("TFCs", obj.tfcs.all()),
            ("Making Of", obj.makingofs.all()),
            ("Mídias", obj.midias.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def tfc_detail(request, id):
    obj = get_object_or_404(
        TFC.objects.select_related("area_interesse")
        .prefetch_related("tecnologias", "makingofs"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe do TFC",
        image_attr="imagem",
        fields=[
            ("Título", obj.titulo),
            ("Autor", obj.autor),
            ("Orientador", obj.orientador),
            ("Curso", obj.curso),
            ("Ano", obj.ano),
            ("Resumo", obj.resumo),
            ("Palavras-chave", obj.palavras_chave),
            ("Email do autor", obj.email_autor),
            ("Documento", obj.documento_url),
            ("Classificação de interesse", obj.classificacao_interesse),
            ("Área de interesse", obj.area_interesse),
            ("Destaque", "Sim" if obj.destaque else "Não"),
        ],
        related_sections=[
            ("Tecnologias", obj.tecnologias.all()),
            ("Making Of", obj.makingofs.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def competencia_detail(request, id):
    obj = get_object_or_404(
        Competencia.objects.prefetch_related("projetos", "formacoes", "makingofs"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Competência",
        fields=[
            ("Nome", obj.nome),
            ("Tipo", obj.tipo),
            ("Descrição", obj.descricao),
            ("Nível", obj.nivel),
            ("Evidência", obj.evidencia),
            ("Destaque", "Sim" if obj.destaque else "Não"),
        ],
        related_sections=[
            ("Projetos", obj.projetos.all()),
            ("Formações", obj.formacoes.all()),
            ("Making Of", obj.makingofs.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def formacao_detail(request, id):
    obj = get_object_or_404(
        Formacao.objects.prefetch_related("competencias", "tecnologias", "makingofs"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Formação",
        fields=[
            ("Nome", obj.nome),
            ("Instituição", obj.instituicao),
            ("Tipo", obj.tipo),
            ("Data de início", obj.data_inicio),
            ("Data de fim", obj.data_fim),
            ("Descrição", obj.descricao),
            ("Certificado", obj.certificado_url),
            ("Estado", obj.estado),
            ("Ordem cronológica", obj.ordem_cronologica),
        ],
        related_sections=[
            ("Competências", obj.competencias.all()),
            ("Tecnologias", obj.tecnologias.all()),
            ("Making Of", obj.makingofs.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def makingof_detail(request, id):
    obj = get_object_or_404(
        MakingOf.objects.select_related(
            "projeto",
            "unidade_curricular",
            "tecnologia",
            "tfc",
            "formacao",
            "competencia",
        ).prefetch_related("midias"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe do Making Of",
        fields=[
            ("Título", obj.titulo),
            ("Descrição", obj.descricao),
            ("Data de registo", obj.data_registo),
            ("Versão do modelo", obj.versao_modelo),
            ("Decisões tomadas", obj.decisoes_tomadas),
            ("Erros encontrados", obj.erros_encontrados),
            ("Correções realizadas", obj.correcoes_realizadas),
            ("Justificação da modelação", obj.justificacao_modelacao),
            ("Uso de IA", obj.uso_ia),
            ("Observações", obj.observacoes),
            ("Projeto", obj.projeto),
            ("Unidade Curricular", obj.unidade_curricular),
            ("Tecnologia", obj.tecnologia),
            ("TFC", obj.tfc),
            ("Formação", obj.formacao),
            ("Competência", obj.competencia),
        ],
        related_sections=[
            ("Mídias", obj.midias.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def docente_detail(request, id):
    obj = get_object_or_404(
        Docente.objects.prefetch_related("unidades_curriculares"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe do Docente",
        image_attr="foto",
        fields=[
            ("Nome", obj.nome),
            ("Email", obj.email),
            ("Área de especialização", obj.area_especializacao),
            ("Página pessoal", obj.pagina_pessoal_url),
        ],
        related_sections=[
            ("Unidades Curriculares", obj.unidades_curriculares.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def area_interesse_detail(request, id):
    obj = get_object_or_404(
        AreaInteresse.objects.prefetch_related("projetos", "tfcs"),
        id=id,
    )

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Área de Interesse",
        fields=[
            ("Nome", obj.nome),
            ("Descrição", obj.descricao),
            ("Categoria", obj.categoria),
            ("Destaque", "Sim" if obj.destaque else "Não"),
        ],
        related_sections=[
            ("Projetos", obj.projetos.all()),
            ("TFCs", obj.tfcs.all()),
        ],
    )
    return render(request, "portfolio/detalhe.html", context)


def midia_detail(request, id):
    obj = get_object_or_404(
        Midia.objects.select_related("unidade_curricular", "projeto", "tecnologia", "making_of"),
        id=id,
    )

    file_url = None
    try:
        file_url = obj.ficheiro.url
    except Exception:
        file_url = None

    context = build_detail_context(
        obj=obj,
        title="Detalhe da Mídia",
        fields=[
            ("Título", obj.titulo),
            ("Tipo", obj.tipo),
            ("Legenda", obj.legenda),
            ("Descrição", obj.descricao),
            ("Data de upload", obj.data_upload),
            ("Unidade Curricular", obj.unidade_curricular),
            ("Projeto", obj.projeto),
            ("Tecnologia", obj.tecnologia),
            ("Making Of", obj.making_of),
            ("Ficheiro", file_url),
        ],
    )

    return render(request, "portfolio/detalhe.html", context)


def home_view(request):
    context = {
        "licenciaturas": Licenciatura.objects.all(),
        "ucs": UnidadeCurricular.objects.all(),
        "tecnologias": Tecnologia.objects.all(),
        "competencias": Competencia.objects.all(),
        "formacoes": Formacao.objects.all(),
        "areas_interesse": AreaInteresse.objects.all(),
        "tfcs": TFC.objects.all(),
        "projetos": Projeto.objects.all(),
        "makingofs": MakingOf.objects.all(),
        "midias": Midia.objects.all(),
        "docentes": Docente.objects.all(),
        "is_gestor": is_gestor_portfolio(request.user),
    }
    return render(request, "portfolio/home.html", context)