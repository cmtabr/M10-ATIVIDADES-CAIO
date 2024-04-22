# Ponderada 1

## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 10 | 2


## Informações da Ponderada
Com objetivo de atestar se o aluno está apto a realizar uma api rest, foi proposto a criação de um CRUD de uma lista de afazeres, com autenticação, autorização e validação de dados. O projeto foi desenvolvido em Python, utilizando o framework FastAPI, e o banco de dados MySQL.

## Instruções para execução
1. Instale o Docker e o Docker Compose
2. Clone o repositório
3. Execute o comando `docker-compose up --build` na raiz do projeto
4. Acesse a documentação da API em `http://localhost:5000/docs`

```bash
git clone https://github.com/cmtabr/M10-ATIVIDADES-CAIO.git m10-atividades
cd m10-atividades/ponderada_1
docker-compose -f docker-compose.yml up
```

## Endpoints
- `POST /api/login`: Autentica o usuário
- `GET /api/todos`: Lista todos os afazeres
- `GET /api/todo/{id}`: Lista um afazer específico
- `POST /api/create_todo`: Cria um novo afazer
- `DELETE /api/todos/{id}`: Deleta um afazer
- `PUT /api/todos/{id}`: Atualiza um afazer

## Documentação
A documentação da API pode ser acessada em `http://localhost:5000/docs`, após a execução do projeto. Além disto é possível utilizar o arquivo `api_test.yaml`` para importar a coleção de requisições no Insomnia.