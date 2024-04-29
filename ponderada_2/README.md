# Ponderada 2

## Informações do Aluno  
Aluno | Curso | Módulo | Turma
:---: | :---: | :---: | :---:
Caio Martins de Abreu | Engenharia da Computação | 10 | 2

## Informações da Ponderada
Com a finalidade de avaliar o conhecimento adquirido durante o módulo 10, a ponderada 2 tem como objetivo a implementação de testes de carga e stress em uma aplicação web. Para isso, foi utilizado o framework K6. 

## Instruções de Instalação
Para instalar o K6, basta seguir as instruções presentes no site oficial do framework: https://k6.io/docs/getting-started/installation/ caso esteja utilizando o windows 
Utilizando um container docker, basta executar o comando abaixo estando na pasta load_test:

## Instruções para execução
1. Instale o Docker e o Docker Compose
2. Clone o repositório
3. Entre na pasta fastapi 
4. Execute o comando `docker-compose up --build` na raiz do projeto
5. Acesse a documentação da API em `http://localhost:5000/docs`

```bash
git clone https://github.com/cmtabr/M10-ATIVIDADES-CAIO.git m10-atividades
cd m10-atividades/ponderada_2/fastapi
docker-compose -f docker-compose.yml up
```

```bash
cd ../load_test
docker run --name k6 --network=goliath_network --rm -i grafana/k6 run - <fastapi-load-test.js
```

E então é só ver a magia acontecer!

## Video Demonstrativo

