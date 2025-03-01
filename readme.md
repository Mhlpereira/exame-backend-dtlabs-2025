### Comece por aqui

**As variaveis de ambiente já estão adicionadas!!**
```

docker compose build 
```

## Utilize o docker compose up -d para subir o container sem travar o terminal.
```
docker compose up -d
```

## Execute para alimentar o banco de dados
```
python -m app.script.seed
```

## Utilize esse comando para iniciar o servidor 
```
uvicorn app.main:app
```

## Execute o get list-server

```
Por alguma ferramenta HTTP (postman, insonia e etc)
Método get
http://127.0.0.1:8000/server/

**imagem pelo postman**

ou para ir pelo swagger

http://127.0.0.1:8000/docs#/server/list_server_list_servers_get

**imagem para lista de server no swagger**

```

Copie e cole o ulid do servidor e passe no corpo da requisição no post.data

Post data vai salvar os valores do sensores

continua...

