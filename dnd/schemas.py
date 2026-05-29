from ninja import Schema


class CampanhaSchema(Schema):
    id: int
    nome: str
    mestre: str
    mundo: str
    nivel_recomendado: int
    ativa: bool


class CampanhaCreateSchema(Schema):
    nome: str
    mestre: str
    mundo: str
    nivel_recomendado: int
    ativa: bool = True