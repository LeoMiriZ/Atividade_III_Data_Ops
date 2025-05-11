# Atividade_III_Data_Ops

## Requisitos

- Desenvolver uma API Flask que exponha dois endpoints:

- POST /soma: recebe dois números e retorna a soma.

- POST /multiplicacao: recebe dois números e retorna o produto.

- Containerizar a aplicação com Docker.

- Subir o projeto para um repositório GitHub.

- Criar um pipeline GitHub Actions que:

  - Conecte via SSH à sua VM.

  - Faça o git pull do repositório.

  - Build do container.

  - Stop e remove o container anterior (se existir).

  - Run do novo container.

  - A aplicação deve rodar na porta 80.
