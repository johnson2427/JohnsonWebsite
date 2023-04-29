from typing import Any, Dict

import pytest
from httpx import AsyncClient

from app.core.config import settings


@pytest.mark.asyncio
async def create_post(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any], data: Dict[Any, Any]
) -> Any:
    response = await client.post(
        url=f"{settings.API_V1_STR}/mongo_item/",
        headers=superuser_token_headers,
        json=data,
    )
    return response


@pytest.mark.asyncio
async def delete_post(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any], data: Dict[Any, Any]
) -> Any:
    response = await client.delete(
        url=f"{settings.API_V1_STR}/mongo_item/{data['name']}",
        headers=superuser_token_headers,
    )
    return response


@pytest.mark.asyncio
async def test_create_mongo_item(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any]
) -> None:
    data = {"name": "Async-FastAPI", "date": "2022-11-19"}
    response = await create_post(client, superuser_token_headers, data)
    assert response.status_code == 200
    content = response.json()
    assert content["name"] == data["name"]
    assert content["date"] == data["date"]
    response = await delete_post(client, superuser_token_headers, data)
    assert response.status_code == 200
    return_val = response.json()
    del return_val["id"]
    assert return_val == data


@pytest.mark.asyncio
async def test_get_mongo_item(
    client: AsyncClient,
    superuser_token_headers: Dict[Any, Any],
) -> None:
    data = {"name": "Async-FastAPI", "date": "2022-11-19"}
    await create_post(client, superuser_token_headers, data)
    response = await client.get(
        url=f"{settings.API_V1_STR}/mongo_item/",
        headers=superuser_token_headers,
        params={"name": data["name"]},
    )
    assert response.status_code == 200
    content = response.json()[0]
    assert content["name"] == data["name"]
    assert content["date"] == data["date"]
    response = await delete_post(client, superuser_token_headers, data)
    assert response.status_code == 200
    return_val = response.json()
    del return_val["id"]
    assert return_val == data


@pytest.mark.asyncio
async def test_get_mongo_list(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any]
) -> None:
    data = {"name": "Async-FastAPI", "date": "2022-11-19"}
    await create_post(client, superuser_token_headers, data)
    response = await client.get(
        url=f"{settings.API_V1_STR}/mongo_item/", headers=superuser_token_headers
    )
    assert response.status_code == 200
    content = response.json()
    assert content[0]["name"] == data["name"]
    response = await delete_post(client, superuser_token_headers, data)
    assert response.status_code == 200
    return_val = response.json()
    del return_val["id"]
    assert return_val == data


@pytest.mark.asyncio
async def test_update_mongo_item(
    client: AsyncClient, superuser_token_headers: Dict[Any, Any]
) -> None:
    data = {"name": "Async-FastAPI", "date": "2022-11-19"}
    await create_post(client, superuser_token_headers, data)
    response = await client.put(
        url=f"{settings.API_V1_STR}/mongo_item/{data['name']}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    response = await delete_post(client, superuser_token_headers, data)
    assert response.status_code == 200
    return_val = response.json()
    del return_val["id"]
    assert return_val == data


@pytest.mark.asyncio
async def test_delete_mongo_item(
    client: AsyncClient,
    superuser_token_headers: Dict[Any, Any],
) -> None:
    data = {"name": "Async-FastAPI-3", "date": "2022-11-19"}
    await create_post(client, superuser_token_headers, data)
    response = await delete_post(client, superuser_token_headers, data)
    assert response.status_code == 200
    return_val = response.json()
    del return_val["id"]
    assert return_val == data
