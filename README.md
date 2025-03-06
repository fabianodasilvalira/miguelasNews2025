# MiguelasNews API

## Descrição

A MiguelasNews é uma API para gerenciar notícias, categorias, comentários e curtidas. A API permite que jornalistas ou administradores publiquem notícias, enquanto leitores podem interagir com o conteúdo, postando comentários e curtindo as notícias. A API segue o padrão RESTful e é construída com o Django Rest Framework.

## Funcionalidades

- **Categorias**: Gerencie as categorias de notícias (ex: Policial, Esporte, Entretenimento, etc.).
- **Notícias**: Criação, leitura, atualização e exclusão de notícias.
- **Comentários**: Leitores podem adicionar comentários às notícias.
- **Curtidas**: Leitores autenticados podem curtir ou descurtir as notícias.
- **Autenticação**: Sistema de autenticação com JWT para garantir que apenas usuários autenticados possam interagir com notícias.

## Requisitos

- Python 3.8 ou superior
- Django 3.x ou superior
- Django Rest Framework 3.x ou superior
- PostgreSQL ou outro banco de dados relacional

## Instalação

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu-usuario/miguelasnews-api.git
   cd miguelasnews-api
