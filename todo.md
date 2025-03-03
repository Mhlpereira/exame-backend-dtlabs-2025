adicionar monitoramento de saúde
rever os requisitos
começar os teste


Lógica do middleware, pausa para descanso!

utilizar a lógica de verificar ao menos um valor para para o zervidor


Prioridades para testes (do mais importante ao menos importante):

Repository (Alta Prioridade)

Razões:

Contém lógica de acesso a dados e interação com o Redis
A verificação de frequência é crítica para o funcionamento correto
Erros aqui afetam todo o sistema


Foco dos testes:

FrequencyRateMiddleware.check_rate() - lógica de controle de taxa
ServerRepository.save_sensor_data() - persistência dos dados




Services (Alta-Média Prioridade)

Razões:

Contém a lógica de negócio central
Coordena várias operações
Implementa regras de negócio


Foco dos testes:

Funções de processamento de dados
Lógica de validação e transformação




Worker Queue (Média Prioridade)

Razões:

Processamento assíncrono crítico
Garante que as mensagens sejam processadas na taxa correta


Foco dos testes:

Operações de enfileiramento/desenfileiramento
Controle de taxa de processamento




Endpoints (Média-Baixa Prioridade)

Razões:

Geralmente delegam a maioria do trabalho aos serviços e repositórios
Importantes para testar integração, mas com menos lógica própria


Foco dos testes:

Validação de entrada
Resposta correta para diferentes cenário


Teste de sucesso básico: Verifica se a função salva os dados corretamente quando todos os parâmetros são válidos.
Teste de falha de conexão: Verifica o comportamento quando não há conexão com o banco de dados.
Teste de formato de data inválido: Verifica como a função lida com formatos de data/hora inválidos.
Teste de erro de banco de dados: Simula um erro durante a execução da query.
Teste de validação de parâmetros: Verifica se a função rejeita corretamente parâmetros inválidos.
Teste parametrizado: Usa @pytest.mark.parametrize para testar diferentes tipos de sensores e valores, demonstrando a flexibilidade do código.