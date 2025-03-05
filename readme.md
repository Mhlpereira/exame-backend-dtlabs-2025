# Comece por aqui


***As variaveis de ambiente já estão adicionadas!!***


### Suba o docker 
```
Este comando você sobe o postgreSQL e o redis.
make docker
```

### Utilize esse comando para iniciar o servidor e criar as tabelas com o turtle orm
```
Este comando você inicia o servidor uvicorne
make start-server
```

### Execute para alimentar o banco de dados com dados básicos para melhor funcionamento do makefile

```
Este comando você alimenta o banco de dados com dados pré definidos para auxiliar nos testes!
make seed-db
```

### Registre um usuario 
```
make register-user
```

### Logue no sistema

```
make Login
```

### Crie o servidor Dolly#3

```
make create-server
```

## Registre o sensor 10 vezes

```
make 10-register-data
```

## Execute os testes

```
make pyteste
```

### Consulta de dados

**Utilize esse link para ver a documentação por swagger e por ela pode ser feita as consultas.**

http://127.0.0.1:8000/docs/


```
Você pode se autenticar utlizando este token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIwMUpOSjhIQ0hSV0RLNjIzN0RWTjRDSzFaMiIsImVtYWlsIjoiZXhhbXBsZTJAZXhhbXBsZS5jb20ifQ.Pnf4u7Ty0I0yoeNHrdVKU6v1btziSAdbwIKqfuxvTOk

<img src="/public/swagger.png" width="600">

ou você pode gerar um token novo se registrando e logando para se autenticar!
Recomendo que não altere o corpo da requisição para não precisar alterar nada na hora de logar.

<img src="/public/register-data.png" width="600">

Pegue o token e se autentique no topo superior direito da página!

<img src="/public/token.png" width="600">

```

## Register
```
Coloque essa cahve no campo do register data para pegar os dados do sensores e enviar para o banco de dados.
Server_ULID:
01JN4HCDW7ZF0TFMXWKRFV06GG
<img src="/public/register-data.png" width="600">

Após isso no campo de health check, você podera verificar se o servidor está online ou offline.

<img src="/public/health-id.png" width="600">

Também pode verificar todos servidores!
<img src="/public/server-health-check.png" width="600">
```


```
No get sensor data personalizada você pode filtrar suas buscas! 
Obs: Tem que ter gerado o registro dos sensores [Register](#register)

<img src="/public/agregation.png" width="600">

Utilize esse server ULID mas você pode gerar outros para fazer seus testes:
01JN4HCDW7ZF0TFMXWKRFV06GG

Utile esse formato para start ou end:
"2025-03-05T01:55:07.596458" 

Temos 4 tipos de sensores:
- temperature
- humidity
- current
- voltage

Granularidade da agregação:
- minute
- hour
- day
```
