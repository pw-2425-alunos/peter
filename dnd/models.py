from django.db import models


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