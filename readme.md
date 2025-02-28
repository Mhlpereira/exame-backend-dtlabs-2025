utilize esse comando para iniciar o servidor 


docker compose build 

Utilize o docker compose up -d para subir o container sem travar o terminal.
docker compose up -d

python -m app.script.seed

utilize esse comando para iniciar o servidor 
uvicorn app.main:app

execute o getpaylod para pegar o id do servidor

execute o register data passando no body um json { "id" : "PayloadGerado"} sendo o x o valor do payload gerado