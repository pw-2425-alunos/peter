from ninja import Router
from .models import Campanha
from .schemas import CampanhaSchema, CampanhaCreateSchema

router = Router()


# GET ONE
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