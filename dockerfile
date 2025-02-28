FROM timescale/timescaledb:latest-pg15

# Copia o script SQL que cria a extensão
COPY init-timescale.sql /docker-entrypoint-initdb.d/