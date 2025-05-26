# 📚 API de Reserva de Salas

Este repositório contém a **API de Reserva de Salas**, desenvolvida com **Flask** e **SQLAlchemy**, como parte de uma arquitetura baseada em **microsserviços**.

## 🧩 Arquitetura

A API de Reserva de Salas é um **microsserviço** que faz parte de um sistema maior chamado [School System](https://github.com/gortin1/ProjetoApi.git), sendo responsável exclusivamente pelo gerenciamento das reservas de salas por turma.

⚠️ **Importante:** Esta API **depende da API de Gerenciamento Escolar (School System)** rodando localmente, pois consome o endpoint `GET /turmas/<id>` para validar se uma **Turma** existe.

---

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- SQLite (como banco de dados local)
- Requests (para consumo da API externa)
- Unittest (para testes unitários da API)

---

## ▶️ Como Executar a API

-- Explicar 

---

## 📡 Endpoints Principais

- `GET /reservas` – Lista todas as reservas
- `POST /reservas` – Cria uma nova reserva
- `GET /reservas/<id>` – Detalha uma reserva
- `PUT /reservas/<id>` – Atualiza uma reserva (é necessário preencher todos os campos para atualizar a reserva)
- `DELETE /reservas/<id>` – Remove uma reserva

### Exemplo de corpo JSON para criação:

```json
{
    "turma_id": 5,
    "sala": "101",
    "data": "2025-05-25",
    "hora_inicio": "08:00",
    "hora_fim": "10:00"
}
```

---

## 🔗 Dependência Externa

📌 **Certifique-se de que a API de Gerenciamento Escolar esteja em execução** antes de criar uma reserva. Caso o endpoint de turma não retorne uma resposta válida (`200 OK`), a criação da reserva será negada.

Endpoint de turmas:

```
http://localhost:5000/api/turmas/{id}

```

---

## 📦 Estrutura do Projeto

```
reserva-salas/
│
├── api/                       
│   ├── reserva/               
│   │   ├── reserva_model.py   
│   │   └── reserva_route.py   
│   │
│   └── test/                  
│       └── test.py                     
├── app.py                     
├── database.py   
├── DockerFile           
├── README.md                  
└── requirements.txt           
```

---

## 🛠️ Futuras Melhorias

- Validação de conflito de horário na sala
- Integração via fila (RabbitMQ) com outros microsserviços
- Autenticação de usuários
- Swagger

---

## 🧑‍💻 Autores

- [Camila Ribeiro](https://github.com/camilasribeiro)
- [Fernando Storel](https://github.com/Fernandostorel)
- [Gabriel Nathan](https://github.com/gortin1)
- [Nicolas Lima](https://github.com/nicolas-liima)


Projeto de arquitetura com Flask e microsserviços.