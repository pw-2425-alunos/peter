from django.db import models


class Licenciatura(models.Model):
    nome = models.CharField(max_length=200)
    numero_semestres = models.PositiveIntegerField()
    ects_total = models.PositiveIntegerField()
    descricao = models.TextField()
    objetivo = models.TextField()
    url_website = models.URLField()
    saidas_profissionais = models.TextField()
    imagem = models.ImageField(upload_to='licenciaturas/', blank=True, null=True)

    def __str__(self):
        return self.nome


class UnidadeCurricular(models.Model):
    licenciatura = models.ForeignKey(
        Licenciatura,
        on_delete=models.CASCADE,
        related_name='unidades_curriculares'
    )
    nome = models.CharField(max_length=200)
    ano_curricular = models.PositiveIntegerField()
    semestre = models.PositiveIntegerField()
    ects = models.PositiveIntegerField()
    apresentacao = models.TextField()
    programa = models.TextField()
    objectivo = models.TextField()
    imagem = models.ImageField(upload_to='unidades_curriculares/', blank=True, null=True)
    url_website = models.URLField()

    class Meta:
        verbose_name = "Unidade curricular"
        verbose_name_plural = "Unidades curriculares"

    def __str__(self):
        return self.nome


class Tecnologia(models.Model):
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    logo = models.ImageField(upload_to='tecnologias/', blank=True, null=True)
    url_website = models.URLField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome


class Competencia(models.Model):
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    descricao = models.TextField()
    nivel = models.CharField(max_length=100)
    evidencia = models.TextField()
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class Formacao(models.Model):
    nome = models.CharField(max_length=200)
    instituicao = models.CharField(max_length=200)
    tipo = models.CharField(max_length=100)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    descricao = models.TextField()
    certificado_url = models.URLField(blank=True, null=True)
    estado = models.CharField(max_length=100)
    ordem_cronologica = models.IntegerField()
    competencias = models.ManyToManyField(
        Competencia,
        related_name='formacoes',
        blank=True
    )
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='formacoes',
        blank=True
    )

    def __str__(self):
        return self.nome


class AreaInteresse(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.CharField(max_length=100)
    destaque = models.BooleanField(default=False)

    def __str__(self):
        return self.nome


class TFC(models.Model):
    area_interesse = models.ForeignKey(
        AreaInteresse,
        on_delete=models.CASCADE,
        related_name='tfcs'
    )
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    orientador = models.CharField(max_length=200)
    curso = models.CharField(max_length=200)
    ano = models.PositiveIntegerField()
    resumo = models.TextField()
    palavras_chave = models.TextField()
    imagem = models.ImageField(upload_to='tfcs/', blank=True, null=True)
    email_autor = models.EmailField()
    documento_url = models.URLField()
    classificacao_interesse = models.CharField(max_length=100)
    destaque = models.BooleanField(default=False)
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='tfcs',
        blank=True
    )

    def __str__(self):
        return self.titulo


class Projeto(models.Model):
    unidade_curricular = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='projetos'
    )
    area_interesse = models.ForeignKey(
        AreaInteresse,
        on_delete=models.CASCADE,
        related_name='projetos',
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    conceitos_aplicados = models.TextField()
    imagem = models.ImageField(upload_to='projetos/', blank=True, null=True)
    ano_realizacao = models.PositiveIntegerField()
    estado = models.CharField(max_length=100)
    destaque = models.BooleanField(default=False)
    tecnologias = models.ManyToManyField(
        Tecnologia,
        related_name='projetos',
        blank=True
    )
    competencias = models.ManyToManyField(
        Competencia,
        related_name='projetos',
        blank=True
    )

    def __str__(self):
        return self.titulo


class MakingOf(models.Model):
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='makingofs',
        null=True,
        blank=True
    )
    unidade_curricular = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='makingofs',
        null=True,
        blank=True
    )
    tecnologia = models.ForeignKey(
        Tecnologia,
        on_delete=models.CASCADE,
        related_name='makingofs',
        null=True,
        blank=True
    )
    tfc = models.ForeignKey(
        TFC,
        on_delete=models.CASCADE,
        related_name='makingofs',
        null=True,
        blank=True
    )
    formacao = models.ForeignKey(
        Formacao,
        on_delete=models.CASCADE,
        related_name='makingofs',
        null=True,
        blank=True
    )
    competencia = models.ForeignKey(
        Competencia,
        on_delete=models.CASCADE,
        related_name='makingofs',
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    data_registo = models.DateField()
    versao_modelo = models.CharField(max_length=100)
    decisoes_tomadas = models.TextField()
    erros_encontrados = models.TextField()
    correcoes_realizadas = models.TextField()
    justificacao_modelacao = models.TextField()
    uso_ia = models.TextField()
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.titulo


class Midia(models.Model):
    unidade_curricular = models.ForeignKey(
        UnidadeCurricular,
        on_delete=models.CASCADE,
        related_name='midias',
        null=True,
        blank=True
    )
    projeto = models.ForeignKey(
        Projeto,
        on_delete=models.CASCADE,
        related_name='midias',
        null=True,
        blank=True
    )
    tecnologia = models.ForeignKey(
        Tecnologia,
        on_delete=models.CASCADE,
        related_name='midias',
        null=True,
        blank=True
    )
    making_of = models.ForeignKey(
        MakingOf,
        on_delete=models.CASCADE,
        related_name='midias',
        null=True,
        blank=True
    )
    titulo = models.CharField(max_length=200)
    ficheiro = models.FileField(upload_to='midia/')
    tipo = models.CharField(max_length=100)
    legenda = models.CharField(max_length=255)
    descricao = models.TextField()
    data_upload = models.DateField()

    def __str__(self):
        return self.titulo
    
class Docente(models.Model):
    nome = models.CharField(max_length=200)
    pagina_pessoal_url = models.URLField()
    email = models.EmailField()
    area_especializacao = models.CharField(max_length=200)
    foto = models.ImageField(upload_to='docentes/', blank=True, null=True)
    unidades_curriculares = models.ManyToManyField(
        UnidadeCurricular,
        related_name='docentes',
        blank=True
    )

    def __str__(self):
        return self.nome    