import os
import sys
from unittest.mock import Mock

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from gmail.gmail_tools import delete_gmail_draft


def _unwrap(tool):
    fn = tool.fn if hasattr(tool, "fn") else tool
    while hasattr(fn, "__wrapped__"):
        fn = fn.__wrapped__
    return fn


@pytest.mark.asyncio
async def test_delete_gmail_draft_calls_api_and_returns_confirmation():
    mock_service = Mock()
    mock_service.users().drafts().delete().execute.return_value = ""

    result = await _unwrap(delete_gmail_draft)(
        service=mock_service,
        user_google_email="user@example.com",
        draft_id="draft123",
    )

    assert "draft123" in result
    assert "deleted" in result.lower()

    delete_kwargs = (
        mock_service.users.return_value.drafts.return_value.delete.call_args.kwargs
    )
    assert delete_kwargs == {"userId": "me", "id": "draft123"}
