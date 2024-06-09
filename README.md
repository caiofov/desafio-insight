# Desafio Insight - Dev Full-Stack Python

> [Edital](https://www.insightlab.ufc.br/wp-content/uploads/2024/05/Projeto-Cultura-Dev-Full-Stack-Python.pdf)

A solução foi desenvolvida em Python utilizando FastAPI com Uvicorn. Foram utilizadas as seguintes APIs externas:
- [IBGE Localidades](https://servicodados.ibge.gov.br/api/docs/localidades)
- [IBGE Nomes](https://servicodados.ibge.gov.br/api/docs/nomes?versao=2)

## Como executar

- Inicializar o Poetry

```shell
poetry install
```

-  Rodar o arquivo Python `src/app/main.py` dentro do ambiente virtual
- Abrir `http://localhost:9000/docs` no navegador para acessar o Swagger, no qual todos os endpoints estão documentados e podem ser testados.
