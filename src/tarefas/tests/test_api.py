from fastapi.testclient import TestClient
import pytest
import tarefas.app as app_module

@pytest.fixture
def client():
    app_module._tarrefas.clear()
    app_module._proximo_id = 1
    return TestClient(app_module.app)


def obter_token(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "aluno",
            "password": "senha123"
        }
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_loginCT1_valido(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "aluno",
            "password": "senha123"
        }
    )

    assert response.status_code == 200

    dados = response.json()

    assert "access_token" in dados
    assert dados["token_type"] == "bearer"


def test_loginCT2_sem_username(client):
    response = client.post(
        "/auth/login",
        data={
            "password": "senha123"
        }
    )

    assert response.status_code == 422


def test_loginCT3_sem_password(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "aluno"
        }
    )

    assert response.status_code == 422


def test_criarCT4_tarefa_com_descricao(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": "Estudar pytest",
            "descricao": "Ler a documentação"
        }
    )

    assert response.status_code == 201

    tarefa = response.json()

    assert isinstance(tarefa["id"], int)
    assert tarefa["titulo"] == "Estudar pytest"
    assert tarefa["descricao"] == "Ler a documentação"
    assert tarefa["status"] == "pendente"


def testCT5_criar_tarefa_sem_descricao(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": "Tarefa sem descricao"
        }
    )

    assert response.status_code == 201

    tarefa = response.json()

    assert tarefa["descricao"] is None


def testCT6_criar_tarefa_vazio(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": ""
        }
    )

    assert response.status_code == 422


def testCT7_criar_tarefa_sem_titulo(client):
    response = client.post(
        "/tarefas",
        json={
            "dascricao": "sem titulo"
        }
    )

    assert response.status_code == 422


def testCT8_criar_tarefa_titulo_maior_limite(client):
    titulo = "A" * 201

    response = client.post(
        "/tarefas",
        json={
            "titulo": titulo
        }
    )

    assert response.status_code == 422


def testCT9_status_inicial_pendente(client):
    response = client.post(
        "/tarefas",
        json={
            "titulo": "nova tarefa"
        }
    )

    assert response.status_code == 201

    tarefa = response.json()

    assert tarefa["status"] == "pendente"


def testCT10_lista_tarefas_vazia(client):
    response = client.get("/tarefas")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json() == []


def testCT11_listar_tarefas_com_dados(client):
    client.post(
        "/tarefas",
        json={
            "titulo": "primeira tarefa"
        }
    )

    response = client.get("/tarefas")

    assert response.status_code == 200

    tarefas = response.json()

    assert len(tarefas) > 0


def testCT12_buscar_tarefa_existente(client):
    criar = client.post(
        "/tarefas",
        json={
            "titulo": "Buscar tarefa"
        }
    )

    tarefa_id = criar.json()["id"]

    response = client.get(f"/tarefas/{tarefa_id}")

    assert response.status_code == 200
    assert response.json()["id"] == tarefa_id


def testCT13_buscar_tarefa_inexistente(client):
    response = client.get("/tarefas/99999")

    assert response.status_code == 404


def testCT14_buscar_tarefa_id_invalido(client):
    response = client.get("/tarefas/abc")

    assert response.status_code == 422


def testCT15_deletar_sem_token(client):
    response = client.delete("/tarefas/1")

    assert response.status_code == 401


def testCT16_deletar_token_invalido(client):
    response = client.delete(
        "/tarefas/1",
        headers={
            "Authorization": "Bearer token-invalido"
        }
    )

    assert response.status_code == 401


def test17_deletar_tarefas_com_token(client):
    token = obter_token(client)

    criar = client.post(
        "/tarefas",
        json={
            "titulo": "Tarefa para deletar"
        }
    )

    tarefa_id = criar.json()["id"]

    response = client.delete(
        f"/tarefas/{tarefa_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 204


def testCT18_deletar_tarefa_inexistente(client):
    token = obter_token(client)

    response = client.delete(
        "/tarefas/99999",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404


def testCT19_tarefa_deletada_nao_existe(client):
    token = obter_token(client)

    criar = client.post(
        "/tarefas",
        json={
            "titulo": "excluir depois buscar"
        }
    )

    tarefa_id = criar.json()["id"]

    client.delete(
        f"/tarefas/{tarefa_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    response = client.get(f"/tarefas/{tarefa_id}")

    assert response.status_code == 404
                                
                                
                            
            
            
    