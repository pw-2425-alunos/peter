from django.db import models
from django.utils import timezone
import secrets

class Campanha(models.Model):
    nome = models.CharField(max_length=100)
    mestre = models.CharField(max_length=100)
    mundo = models.CharField(max_length=100)
    nivel_recomendado = models.IntegerField()
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome


class Personagem(models.Model):
    nome = models.CharField(max_length=100)
    raca = models.CharField(max_length=50)
    classe = models.CharField(max_length=50)
    nivel = models.IntegerField()
    vida = models.IntegerField()

    campanha = models.ForeignKey(
        Campanha,
        on_delete=models.CASCADE,
        related_name="personagens"
    )

    def __str__(self):
        return self.nome


class Missao(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    recompensa_ouro = models.IntegerField()
    concluida = models.BooleanField(default=False)

    campanha = models.ForeignKey(
        Campanha,
        on_delete=models.CASCADE,
        related_name="missoes"
    )

    personagens = models.ManyToManyField(
        Personagem,
        related_name="missoes"
    )

    def __str__(self):
        return self.titulo


class MusicaAmbiente(models.Model):
    titulo = models.CharField(max_length=100)
    artista = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    duracao = models.IntegerField()

    url = models.URLField(blank=True, default="")

    campanha = models.ForeignKey(
        Campanha,
        on_delete=models.CASCADE,
        related_name="musicas"
    )
def __str__(self):
    return self.titulo


def generate_api_key():
    return secrets.token_urlsafe(32)


class APIKey(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Nome de quem vai usar a chave"
    )

    key = models.CharField(
        max_length=255,
        unique=True,
        default=generate_api_key
    )

    is_active = models.BooleanField(default=True)

    expiration_date = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.name} - "
            f"{'Ativa' if self.is_active else 'Inativa'}"
        )

    def is_valid(self):
        return (
            self.is_active
            and self.expiration_date > timezone.now()
        )    