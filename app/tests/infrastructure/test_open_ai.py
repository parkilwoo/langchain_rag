import pytest
import asyncio

from app.infrastructure.connector.open_ai import OpenAiConnector

@pytest.mark.asyncio
async def test_opeai_connector_test_fail_case():
    connector = OpenAiConnector("abc", "gpt-4o")
    result = await connector.test_connection()
    print(result)