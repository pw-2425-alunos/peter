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

class PersonagemSchema(Schema):
    id: int
    nome: str
    raca: str
    classe: str
    nivel: int
    vida: int
    campanha_id: int


class PersonagemCreateSchema(Schema):
    nome: str
    raca: str
    classe: str
    nivel: int
    vida: int
    campanha_id: int


class MissaoSchema(Schema):
    id: int
    titulo: str
    descricao: str
    recompensa_ouro: int
    concluida: bool
    campanha_id: int


class MissaoCreateSchema(Schema):
    titulo: str
    descricao: str
    recompensa_ouro: int
    concluida: bool = False
    campanha_id: int


class MusicaSchema(Schema):
    id: int
    titulo: str
    artista: str
    genero: str
    duracao: int
    url: str
    campanha_id: int


class MusicaCreateSchema(Schema):
    titulo: str
    artista: str
    genero: str
    duracao: int
    url: str
    campanha_id: int    