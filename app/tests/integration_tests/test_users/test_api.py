from httpx import AsyncClient
import pytest


@pytest.mark.parametrize('email, password, status_code',
                         [('kot@samara.ru', 'kotopes', 200),
                          ('kot@samara.ru', 'kotpes', 409),
                          ('fsdfsf23f2f', 'kotpes', 422),
                          ])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(url='/auth/register',
                             json={'email': email, 'password': password}, )

    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code',
                         [('test@test.com', 'test', 200),
                          ('artem@example.com', 'artem', 200),
                          ('borodach@example.com', 'ff22f', 401),
                          ('test@test.com', 'testfdf', 401),
                          ])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post(url='/auth/login',
                             json={'email': email, 'password': password}, )

    assert response.status_code == status_code