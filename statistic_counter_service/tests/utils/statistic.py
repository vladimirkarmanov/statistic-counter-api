from httpx import AsyncClient, Response


async def create_statistic(client: AsyncClient, json: dict) -> Response:
    return await client.post(f"api/v1/statistic/", json=json)


async def get_statistic(
        client: AsyncClient,
        from_date: str,
        to_date: str,
        order: str = "ASC",
        sort: str | None = None
) -> Response:
    return await client.get(f"api/v1/statistic/", params={"from": from_date,
                                                          "to": to_date,
                                                          "sort": sort,
                                                          "order": order})


async def delete_statistic(client: AsyncClient) -> Response:
    return await client.delete(f"api/v1/statistic/")
