import time
from typing import Optional

import httpx
import llm
from pydantic import Field


class OpenHandsModel(llm.KeyModel):
    needs_key = "openhands"
    key_env_var = "LLM_OPENHANDS_KEY"
    can_stream = False

    class Options(llm.Options):
        repository: Optional[str] = Field(
            description="GitHub repository URL to analyze", default=None
        )

    def __init__(self):
        self.model_id = "openhands"

    def execute(self, prompt, stream, response, conversation, key):
        request_json = {"initial_user_msg": prompt.prompt}
        if prompt.options.repository:
            request_json["repository"] = prompt.options.repository

        create_conversation_response = httpx.post(
            "https://app.all-hands.dev/api/conversations",
            headers={"Authorization": f"Bearer {key}"},
            json=request_json,
            timeout=httpx.Timeout(5.0, read=10.0),
        )
        create_conversation_response.raise_for_status()

        conversation_id = create_conversation_response.json()["conversation_id"]
        print(
            f"OpenHands URL: https://app.all-hands.dev/conversations/{conversation_id}"
        )
        print()

        while True:
            trajectory_response = httpx.get(
                f"https://app.all-hands.dev/api/conversations/{conversation_id}/trajectory",
                headers={"Authorization": f"Bearer {key}"},
                timeout=httpx.Timeout(5.0, read=30.0),
            )
            try:
                trajectory_response.raise_for_status()
            except httpx.HTTPStatusError:
                continue
            else:
                trajectories = trajectory_response.json()["trajectory"]
                last_trajectory = trajectories[-1]
                if (
                    "extras" in last_trajectory
                    and last_trajectory["extras"].get("agent_state")
                    == "awaiting_user_input"
                ):
                    break
                time.sleep(5)

        for trajectory in trajectories:
            if (
                trajectory["source"] == "agent"
                and trajectory.get("action") == "message"
            ):
                yield trajectory["message"]


@llm.hookimpl
def register_models(register):
    register(OpenHandsModel())
