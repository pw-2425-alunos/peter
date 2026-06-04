from ninja import Router
from ninja.security import APIKeyHeader

from .models import (
    Campanha,
    Personagem,
    Missao,
    MusicaAmbiente,
    APIKey,
)

from .schemas import (
    CampanhaSchema,
    CampanhaCreateSchema,
    PersonagemSchema,
    PersonagemCreateSchema,
    MissaoSchema,
    MissaoCreateSchema,
    MusicaSchema,
    MusicaCreateSchema,
)

router = Router()


# Criação da classe API para autenticação
class AuthAPIKey(APIKeyHeader):
    param_name = "X-API-Key"

    def authenticate(self, request, key):
        try:
            api_key = APIKey.objects.get(key=key)

            if api_key.is_valid():
                return api_key.name

        except APIKey.DoesNotExist:
            pass

        return None

# GET UM
@router.get("/campanhas/{campanha_id}", response=CampanhaSchema)
def obter_campanha(request, campanha_id: int):
    return Campanha.objects.get(id=campanha_id)


# CREATE
@router.post("/campanhas", response=CampanhaSchema)
def criar_campanha(request, payload: CampanhaCreateSchema):
    campanha = Campanha.objects.create(**payload.dict())
    return campanha


# UPDATE
@router.put("/campanhas/{campanha_id}", response=CampanhaSchema)
def atualizar_campanha(request, campanha_id: int, payload: CampanhaCreateSchema):
    campanha = Campanha.objects.get(id=campanha_id)

    campanha.nome = payload.nome
    campanha.mestre = payload.mestre
    campanha.mundo = payload.mundo
    campanha.nivel_recomendado = payload.nivel_recomendado
    campanha.ativa = payload.ativa

    campanha.save()

    return campanha


# DELETE
@router.delete("/campanhas/{campanha_id}")
def apagar_campanha(request, campanha_id: int):
    campanha = Campanha.objects.get(id=campanha_id)
    campanha.delete()

    return {"success": True}

# GET ALL + FILTROS + PAGINACAO
@router.get("/campanhas", response=list[CampanhaSchema])
def listar_campanhas(
    request,
    ativa: bool | None = None,
    mundo: str | None = None,
    skip: int = 0,
    limit: int = 10,
):
    campanhas = Campanha.objects.all()

    # filtros
    if ativa is not None:
        campanhas = campanhas.filter(ativa=ativa)


    if mundo:
        campanhas = campanhas.filter(mundo__icontains=mundo)

    # paginação
    return campanhas[skip:skip + limit]    

# =========================
# PERSONAGENS
# =========================

@router.get("/personagens", response=list[PersonagemSchema])
def listar_personagens(request):
    return Personagem.objects.all()


@router.get("/personagens/{personagem_id}", response=PersonagemSchema)
def obter_personagem(request, personagem_id: int):
    return Personagem.objects.get(id=personagem_id)


@router.post("/personagens", response=PersonagemSchema)
def criar_personagem(request, payload: PersonagemCreateSchema):

    personagem = Personagem.objects.create(
        nome=payload.nome,
        raca=payload.raca,
        classe=payload.classe,
        nivel=payload.nivel,
        vida=payload.vida,
        campanha_id=payload.campanha_id,
    )

    return personagem


@router.put("/personagens/{personagem_id}", response=PersonagemSchema)
def atualizar_personagem(
    request,
    personagem_id: int,
    payload: PersonagemCreateSchema
):

    personagem = Personagem.objects.get(id=personagem_id)

    personagem.nome = payload.nome
    personagem.raca = payload.raca
    personagem.classe = payload.classe
    personagem.nivel = payload.nivel
    personagem.vida = payload.vida
    personagem.campanha_id = payload.campanha_id

    personagem.save()

    return personagem
    



@router.delete("/personagens/{personagem_id}")
def apagar_personagem(request, personagem_id: int):

    personagem = Personagem.objects.get(id=personagem_id)
    personagem.delete()

    return {"success": True}    

# =========================
# MISSOES
# =========================

@router.get("/missoes", response=list[MissaoSchema])
def listar_missoes(request):
    return Missao.objects.all()


@router.get("/missoes/{missao_id}", response=MissaoSchema)
def obter_missao(request, missao_id: int):
    return Missao.objects.get(id=missao_id)


@router.post("/missoes", response=MissaoSchema)
def criar_missao(request, payload: MissaoCreateSchema):

    missao = Missao.objects.create(
        titulo=payload.titulo,
        descricao=payload.descricao,
        recompensa_ouro=payload.recompensa_ouro,
        concluida=payload.concluida,
        campanha_id=payload.campanha_id,
    )

    return missao


@router.put("/missoes/{missao_id}", response=MissaoSchema)
def atualizar_missao(
    request,
    missao_id: int,
    payload: MissaoCreateSchema
):

    missao = Missao.objects.get(id=missao_id)

    missao.titulo = payload.titulo
    missao.descricao = payload.descricao
    missao.recompensa_ouro = payload.recompensa_ouro
    missao.concluida = payload.concluida
    missao.campanha_id = payload.campanha_id

    missao.save()

    return missao


@router.delete("/missoes/{missao_id}")
def apagar_missao(request, missao_id: int):

    missao = Missao.objects.get(id=missao_id)
    missao.delete()

    return {"success": True}    

# =========================
# MUSICAS
# =========================

@router.get("/musicas", response=list[MusicaSchema])
def listar_musicas(request):
    return MusicaAmbiente.objects.all()


@router.get("/musicas/{musica_id}", response=MusicaSchema)
def obter_musica(request, musica_id: int):
    return MusicaAmbiente.objects.get(id=musica_id)


@router.post("/musicas", response=MusicaSchema)
def criar_musica(request, payload: MusicaCreateSchema):

    musica = MusicaAmbiente.objects.create(
        titulo=payload.titulo,
        artista=payload.artista,
        genero=payload.genero,
        duracao=payload.duracao,
        url=payload.url,
        campanha_id=payload.campanha_id,
    )

    return musica


@router.put("/musicas/{musica_id}", response=MusicaSchema)
def atualizar_musica(
    request,
    musica_id: int,
    payload: MusicaCreateSchema
):

    musica = MusicaAmbiente.objects.get(id=musica_id)

    musica.titulo = payload.titulo
    musica.artista = payload.artista
    musica.genero = payload.genero
    musica.duracao = payload.duracao
    musica.url = payload.url
    musica.campanha_id = payload.campanha_id

    musica.save()

    return musica


@router.delete("/musicas/{musica_id}")
def apagar_musica(request, musica_id: int):

    musica = MusicaAmbiente.objects.get(id=musica_id)
    musica.delete()

    return {"success": True}

@router.get("/teste-privado", auth=AuthAPIKey())
def teste_privado(request):

    return {
        "message": (
            f"Autenticado com sucesso "
            f"como {request.auth}"
        )
    }