from unittest.mock import MagicMock

import httpx
import respx
from llm.plugins import load_plugins, pm

from llm_openhands import OpenHandsModel


def test_plugin_is_installed():
    load_plugins()

    names = [mod.__name__ for mod in pm.get_plugins()]
    assert "llm_openhands" in names


@respx.mock
def test_execute_without_repository(respx_mock):
    respx_mock.post(
        "https://app.all-hands.dev/api/conversations",
        headers__contains={"Authorization": "Bearer test-api-key"},
        json__eq={"initial_user_msg": "Hello, how are you?"},
    ).mock(
        return_value=httpx.Response(
            status_code=200,
            json={"status": "ok", "conversation_id": "test-conversation-id"},
        )
    )
    respx_mock.get(
        "https://app.all-hands.dev/api/conversations/test-conversation-id/trajectory",
        headers__contains={"Authorization": "Bearer test-api-key"},
    ).mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "trajectory": [
                    {
                        "id": 2,
                        "source": "user",
                        "message": "Hello, how are you?",
                        "action": "message",
                    },
                    {
                        "id": 3,
                        "source": "environment",
                        "action": "change_agent_state",
                    },
                    {
                        "id": 4,
                        "source": "user",
                        "action": "recall",
                    },
                    {
                        "id": 5,
                        "source": "environment",
                        "observation": "agent_state_changed",
                    },
                    {
                        "id": 6,
                        "source": "environment",
                        "observation": "recall",
                    },
                    {
                        "id": 7,
                        "source": "agent",
                        "message": "Hello! I'm doing well, thank you for asking. How can I assist you today?",
                        "action": "message",
                    },
                    {
                        "id": 8,
                        "source": "environment",
                        "observation": "agent_state_changed",
                        "extras": {"agent_state": "awaiting_user_input", "reason": ""},
                    },
                ]
            },
        )
    )

    sut = OpenHandsModel()
    prompt = MagicMock()
    prompt.prompt = "Hello, how are you?"
    prompt.options = MagicMock()
    prompt.options.repository = None

    actual = list(
        sut.execute(
            prompt,
            stream=False,
            response=MagicMock(),
            conversation=MagicMock(),
            key="test-api-key",
        )
    )

    assert actual == [
        "Hello! I'm doing well, thank you for asking. How can I assist you today?"
    ]


@respx.mock
def test_execute(respx_mock):
    respx_mock.post(
        "https://app.all-hands.dev/api/conversations",
        headers__contains={"Authorization": "Bearer test-api-key"},
        json__eq={
            "initial_user_msg": "Check the code",
            "repository": "https://github.com/yourusername/your-repo",
        },
    ).mock(
        return_value=httpx.Response(
            status_code=200,
            json={"status": "ok", "conversation_id": "test-conversation-id"},
        )
    )
    respx_mock.get(
        "https://app.all-hands.dev/api/conversations/test-conversation-id/trajectory",
        headers__contains={"Authorization": "Bearer test-api-key"},
    ).mock(
        return_value=httpx.Response(
            status_code=200,
            json={
                "trajectory": [
                    {
                        "id": 2,
                        "source": "user",
                        "message": "Check the code",
                        "action": "message",
                    },
                    {
                        "id": 7,
                        "source": "agent",
                        "message": "I've checked the repository code.",
                        "action": "message",
                    },
                    {
                        "id": 8,
                        "source": "environment",
                        "observation": "agent_state_changed",
                        "extras": {"agent_state": "awaiting_user_input", "reason": ""},
                    },
                ]
            },
        )
    )

    sut = OpenHandsModel()
    prompt = MagicMock()
    prompt.prompt = "Check the code"
    prompt.options = MagicMock()
    prompt.options.repository = "https://github.com/yourusername/your-repo"

    actual = list(
        sut.execute(
            prompt,
            stream=False,
            response=MagicMock(),
            conversation=MagicMock(),
            key="test-api-key",
        )
    )

    assert actual == ["I've checked the repository code."]
