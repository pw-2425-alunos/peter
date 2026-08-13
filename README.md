Portfólio Académico — Engenharia Informática

Aplicação web desenvolvida como portfólio académico no âmbito da Licenciatura em Engenharia Informática.

O projeto reúne informação sobre a formação académica, unidades curriculares, projetos, tecnologias, competências, formações e áreas de interesse, permitindo também apresentar conteúdos multimédia e artigos.

Além da componente de portfólio, o projeto inclui uma API RESTful desenvolvida com Django Ninja, autenticação de utilizadores e um sistema de deployment baseado em Docker e CI/CD.

🌐 Projeto online

Portfólio:
http://peter.pw.deisi.ulusofona.pt/

🛠️ Tecnologias
Backend
Python
Django
Django Ninja
Django ORM
PostgreSQL
REST API
Frontend
HTML
CSS
Templates Django
Autenticação e serviços
Django Authentication
Django Allauth
API Keys
Cloudinary
DevOps / Deployment
Docker
Docker Compose
Git
GitHub Actions
GitHub Container Registry
Gunicorn
CI/CD
🏗️ Arquitetura

O projeto está organizado em várias aplicações Django, separando diferentes responsabilidades:

projeto/
├── portfolio/      # Conteúdo principal do portfólio académico
├── artigos/        # Sistema de artigos, comentários, likes e avaliações
├── accounts/       # Autenticação e gestão de utilizadores
├── dnd/            # API RESTful relacionada com Dungeons & Dragons
└── project/        # Configuração principal do projeto Django
Portfólio

A aplicação portfolio utiliza modelos relacionais para representar diferentes componentes da formação académica, incluindo:

Licenciatura
Unidades Curriculares
Projetos
Tecnologias
Competências
Formações
Áreas de Interesse
Trabalhos Finais de Curso (TFC)
Docentes
Making Of
Conteúdos multimédia

As relações entre estes elementos são geridas através do Django ORM.

Artigos

A aplicação artigos permite criar e consultar artigos, incluindo:

autores;
fotografias;
links externos;
comentários;
likes;
avaliações.
🔐 Autenticação

O projeto inclui autenticação de utilizadores através do Django e Django Allauth.

Também foi implementado um sistema de autenticação através de Magic Link, permitindo iniciar sessão através de um link enviado por email.

A API utiliza um mecanismo próprio de autenticação através de API Key, enviada no header:

X-API-Key

As chaves possuem estado de ativação e data de expiração.

🔌 API RESTful

O projeto inclui uma API desenvolvida com Django Ninja, disponível através do prefixo:

/api/dnd/

A API disponibiliza operações CRUD para diferentes entidades relacionadas com campanhas de Dungeons & Dragons.

Entidades
Campanhas
Personagens
Missões
Músicas Ambiente
Operações

São disponibilizadas operações:

GET
POST
PUT
DELETE
Exemplo — obter uma campanha
GET /api/dnd/campanhas/{campanha_id}
Exemplo — criar uma campanha
POST /api/dnd/campanhas
Content-Type: application/json
X-API-Key: <API_KEY>

Exemplo de payload:

{
    "nome": "Aventura em Faerûn",
    "mestre": "Dungeon Master",
    "mundo": "Forgotten Realms",
    "nivel_recomendado": 5,
    "ativa": true
}
Listagem com filtros e paginação

A listagem de campanhas permite utilizar parâmetros como:

GET /api/dnd/campanhas?ativa=true&mundo=Forgotten&skip=0&limit=10

A API utiliza schemas do Django Ninja para validar e estruturar os dados de entrada e saída.

🐳 Docker

A aplicação pode ser executada através de Docker.

O projeto inclui:

Dockerfile
docker-compose.yml

A imagem utiliza Python 3.12 e executa a aplicação Django através do Gunicorn.

🚀 CI/CD e Deployment

O projeto possui um workflow de GitHub Actions responsável pelo processo de deployment.

O pipeline executa:

Push para main
      ↓
Build da imagem Docker
      ↓
Push para GitHub Container Registry
      ↓
Ligação ao servidor através de SSH
      ↓
Pull da nova imagem
      ↓
Substituição do container em execução

As credenciais e configurações sensíveis utilizadas no processo são fornecidas através de GitHub Secrets e variáveis de ambiente.

📚 Objetivo académico

Este projeto foi desenvolvido como parte da formação em Engenharia Informática, servindo simultaneamente como portfólio dos conhecimentos adquiridos ao longo do curso.

O desenvolvimento permitiu aplicar conhecimentos de:

desenvolvimento web;
programação em Python;
bases de dados relacionais;
modelação de dados;
desenvolvimento de APIs;
autenticação;
integração de serviços;
gestão de ficheiros e media;
Docker;
CI/CD;
deployment de aplicações web.
📌 Estado do projeto

Projeto em desenvolvimento e evolução contínua durante a Licenciatura em Engenharia Informática.

👨‍💻 Autor

Pedro Tiago Caeiro Santos

Portfólio:
http://peter.pw.deisi.ulusofona.pt
