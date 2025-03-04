# from dependency_injector import containers, providers
# from redis.asyncio import Redis


# class Container(containers.DeclarativeContainer):
#     # Configurações
#     config = providers.Configuration()

#     # Dependências
#     redis = providers.Singleton(Redis.from_url, url="redis://localhost:6379", db=0)

#     # Serviços
#     user_service = providers.Factory(
#         UserService,
#         redis=redis,
#     )
