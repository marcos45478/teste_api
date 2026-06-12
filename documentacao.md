# Documentação da API de Tarefas

## Visão Geral
API de tarefas construída com FastAPI. Ela oferece autenticação via token JWT e operações para criar, listar, buscar e excluir tarefas.

## Componentes principais
- `src/tarefas/app.py`
  - Endpoints:
    - `GET /` → redireciona para `/docs`
    - `POST /auth/login` → gera token JWT
    - `GET /tarefas` → lista tarefas
    - `POST /tarefas` → cria tarefa
    - `GET /tarefas/{tarefa_id}` → busca tarefa por ID
    - `DELETE /tarefas/{tarefa_id}` → exclui tarefa com autenticação
- `src/tarefas/auth.py`
  - Geração e verificação de token JWT
  - Usa `jose`, `bcrypt` e `OAuth2PasswordBearer`
- `src/tarefas/modelos.py`
  - Modelos Pydantic:
    - `TarefaCreate`
    - `TarefaResponse`
    - `StatusTarefa`
- `src/tarefas/repositorio.py`
  - Arquivo presente mas sem implementação atual

## Fluxo de autenticação
1. Fazer `POST /auth/login` com campos `username` e `password`
2. Receber `access_token` no retorno
3. Usar header `Authorization: Bearer <token>` para acessar `DELETE /tarefas/{id}`

## Casos de uso suportados
- Criar tarefas com ou sem descrição
- Listar todas as tarefas
- Buscar tarefa por ID
- Excluir tarefa com token válido
- Validação de entrada para título vazio, título ausente e tamanho máximo

## Resultados de teste
Todos os testes executados passaram com sucesso.

- Comando usado: `c:/Users/alunosuper/Desktop/teste_api/venv/Scripts/python.exe -m pytest -q`
- Resultado: `19 passed in 0.45s`

## Tabela de situação de teste

| Caso de teste | Objetivo | Endpoint / fluxo | Status |
|---|---|---|---|
| `test_loginCT1_valido` | Login válido | `POST /auth/login` | Pass |
| `test_loginCT2_sem_username` | Falta username | `POST /auth/login` | Pass |
| `test_loginCT3_sem_password` | Falta password | `POST /auth/login` | Pass |
| `test_criarCT4_tarefa_com_descricao` | Criar tarefa com descrição | `POST /tarefas` | Pass |
| `testCT5_criar_tarefa_sem_descricao` | Criar tarefa sem descrição | `POST /tarefas` | Pass |
| `testCT6_criar_tarefa_vazio` | Título vazio inválido | `POST /tarefas` | Pass |
| `testCT7_criar_tarefa_sem_titulo` | Campo obrigatório faltando | `POST /tarefas` | Pass |
| `testCT8_criar_tarefa_titulo_maior_limite` | Título > 200 chars | `POST /tarefas` | Pass |
| `testCT9_status_inicial_pendente` | Status inicial correto | `POST /tarefas` | Pass |
| `testCT10_lista_tarefas_vazia` | Lista vazia | `GET /tarefas` | Pass |
| `testCT11_listar_tarefas_com_dados` | Listar tarefas após criação | `GET /tarefas` | Pass |
| `testCT12_buscar_tarefa_existente` | Buscar tarefa existente | `GET /tarefas/{id}` | Pass |
| `testCT13_buscar_tarefa_inexistente` | Buscar ID inexistente | `GET /tarefas/{id}` | Pass |
| `testCT14_buscar_tarefa_id_invalido` | ID inválido no path | `GET /tarefas/abc` | Pass |
| `testCT15_deletar_sem_token` | Deletar sem token | `DELETE /tarefas/{id}` | Pass |
| `testCT16_deletar_token_invalido` | Token inválido | `DELETE /tarefas/{id}` | Pass |
| `test17_deletar_tarefas_com_token` | Deletar com token válido | `DELETE /tarefas/{id}` | Pass |
| `testCT18_deletar_tarefa_inexistente` | Excluir tarefa inexistente | `DELETE /tarefas/{id}` | Pass |

## Observações
- `src/tarefas/repositorio.py` está sem conteúdo.
- A autenticação funciona apenas para exclusão de tarefas. Outros endpoints não exigem token.
- A cobertura atual foca em fluxo de criação, listagem, consulta e exclusão.
