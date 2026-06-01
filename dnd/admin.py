from django.contrib import admin
from .models import Campanha, Personagem, Missao, MusicaAmbiente

@admin.register(Campanha)
class CampanhaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "mestre", "mundo", "ativa")

@admin.register(Personagem)
class PersonagemAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "raca", "classe", "nivel", "campanha")

@admin.register(Missao)
class MissaoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "recompensa_ouro", "concluida", "campanha")

@admin.register(MusicaAmbiente)
class MusicaAmbienteAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "artista", "genero","campanha")
