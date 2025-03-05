# Comece por aqui / Start Here

**As variáveis de ambiente já estão adicionadas!**  
**Environment variables are already set!**

## Subir o Docker / Start Docker
Este comando sobe o PostgreSQL e o Redis.
This command starts PostgreSQL and Redis.

```sh

make docker

```

## Iniciar o servidor e criar as tabelas com o Turtle ORM / Start the Server and Create Tables with Turtle ORM
Este comando inicia o servidor Uvicorn.
This command starts the Uvicorn server.

```sh

make start-server

```

## Popular o banco de dados com dados básicos / Seed the Database with Basic Data
Este comando alimenta o banco de dados com dados pré-definidos para auxiliar nos testes.
This command seeds the database with predefined data to assist in testing.
```sh

make seed-db

```

## Registrar um usuário / Register a User
```sh
make register-user
```

## Fazer login no sistema / Login to the System
```sh
make login
```

## Criar o servidor Dolly#3 / Create the Dolly#3 Server
```sh
make create-server
```

## Registrar o sensor 10 vezes / Register the Sensor 10 Times
```sh
make 10-register-data
```

## Executar os testes / Run Tests
```sh
make pytest
```

## Consultar dados / Query Data

**Utilize este link para acessar a documentação Swagger e realizar consultas.**  
**Use this link to access the Swagger documentation and perform queries.**  

[http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)

Você pode se autenticar utilizando este token:  
You can authenticate using this token:
```sh
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpOSjhIQ0hSV0RLNjIzN0RWTjRDSzFaMiIsImVtYWlsIjoiZXhhbXBsZTJAZXhhbXBsZS5jb20ifQ.Pnf4u7Ty0I0yoeNHrdVKU6v1btziSAdbwIKqfuxvTOk

```
![Image](https://github.com/user-attachments/assets/996f0213-89c5-4455-8d31-4edd0263f342)

Ou gere um novo token registrando-se e fazendo login.
Pegue o token e autentique-se no canto superior direito da página.  
 
Or generate a new token by registering and logging in.
Retrieve the token and authenticate at the top-right of the page.

![Image](https://github.com/user-attachments/assets/633e8961-cf88-476b-810d-9f36202d5526)

![Image](https://github.com/user-attachments/assets/0df45ca4-5253-4e4f-a38f-fbc0db5cff38)

## Registro de Sensores / Sensor Registration
```sh
# Coloque esta chave no campo de registro de dados para capturar as leituras dos sensores e enviá-las ao banco de dados.
# Place this key in the data registration field to capture sensor readings and send them to the database.
Server_ULID: 01JN4HCDW7ZF0TFMXWKRFV06GG
```
![Image](https://github.com/user-attachments/assets/b571855a-9f37-4bbc-80d2-89a78979f691)

Após isso, utilize a verificação de integridade para conferir se o servidor está online ou offline.  
Também é possível verificar todos os servidores registrados.

After that, use the health check to verify if the server is online or offline. 
You can also check all registered servers.

Check por id

![Image](https://github.com/user-attachments/assets/1ed1517c-c913-4dae-8d87-bf2eb039c037)

Check all 

![Image](https://github.com/user-attachments/assets/c56b4619-0830-4772-998f-91d9901bb68a)

## Filtragem de Dados dos Sensores / Filtering Sensor Data

Para realizar buscas personalizadas, utilize o endpoint de consulta de sensores.  
To perform custom searches, use the sensor query endpoint.

**Observação:** Os sensores precisam estar registrados antes da consulta.  
**Note:** Sensors must be registered before querying.

```sh
# Utilize este Server ULID ou gere um novo para testes.
# Use this Server ULID or generate a new one for testing.
Server_ULID: 01JN4HCDW7ZF0TFMXWKRFV06GG
```

![Image](https://github.com/user-attachments/assets/1104322f-ab8a-4374-bdf3-ef8f12189d9f)

Formato para `start` ou `end`:

Format for `start` or `end`:
```sh
"2025-03-05T01:55:07.596458"
```

### Tipos de Sensores / Sensor Types
- Temperature
- Humidity
- Current
- Voltage

### Granularidade da Agregação / Aggregation Granularity
- Minute
- Hour
- Day

