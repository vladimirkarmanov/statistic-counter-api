import pytest
from fastapi import status

from core.settings import Settings
from schemas.statistic import StatisticRetrieveSchema
from tests.utils.statistic import create_statistic, get_statistic, delete_statistic

settings = Settings()


class TestCreateStatistic:
    @pytest.mark.asyncio
    async def test_create_statistic_valid_data(self, client_with_teardown, full_correct_statistic):
        response = await create_statistic(client_with_teardown, full_correct_statistic)
        assert (
                response.status_code == status.HTTP_200_OK
        ), f"Error: create statistic failed, {response.json()}"
        data = response.json()
        try:
            StatisticRetrieveSchema(**data)
        except Exception as e:
            raise AssertionError(f"Error: POST /statistic/: {e}")

    @pytest.mark.asyncio
    async def test_create_statistic_invalid_data(self, client_with_teardown, full_correct_statistic):
        full_correct_statistic["cost"] = 123.123
        response = await create_statistic(client_with_teardown, full_correct_statistic)
        assert (
                response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), f"Error: create statistic must returns 422 validation error, {response.json()}"


class TestGetStatistic:
    @pytest.mark.asyncio
    async def test_get_statistic_returns_correct_data(self, client_with_teardown):
        from_date = '2020-01-01'
        to_date = '2025-01-01'
        response = await get_statistic(client_with_teardown, from_date=from_date, to_date=to_date)
        assert (
                response.status_code == status.HTTP_200_OK
        ), f"Error: get statistic failed, {response.json()}"
        data = response.json()
        try:
            assert len([StatisticRetrieveSchema(**s) for s in data]) > 0
        except Exception as e:
            raise AssertionError(f"Error: GET /statistic/: {e}")

    @pytest.mark.asyncio
    async def test_get_statistic_returns_empty_list(self, client_with_teardown):
        from_date = '2030-01-01'
        to_date = '2035-01-01'
        response = await get_statistic(client_with_teardown, from_date=from_date, to_date=to_date)
        assert (
                response.status_code == status.HTTP_200_OK
        ), f"Error: get statistic failed, {response.json()}"
        data = response.json()
        assert len(data) == 0, f"Error: get statistic failed (must returns empty list): {data}"


class TestDeleteStatistic:
    @pytest.mark.asyncio
    async def test_delete_statistic(self, client_with_teardown):
        response = await delete_statistic(client_with_teardown)
        assert (
                response.status_code == status.HTTP_204_NO_CONTENT
        ), f"Error: delete statistic failed, {response.json()}"

        response = await delete_statistic(client_with_teardown)
        assert (
                response.status_code == status.HTTP_404_NOT_FOUND
        ), f"Error: delete statistic failed (must returns 404 when no statistic in db), {response.json()}"
