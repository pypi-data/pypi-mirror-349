import pathlib
import re
import time
from typing import Any, Union

from openai import OpenAI
from PIL import Image
from pydantic import Field, HttpUrl, SecretStr
from pydantic_settings import BaseSettings

from askui.exceptions import QueryNoResponseError
from askui.reporting import Reporter
from askui.tools.agent_os import AgentOs
from askui.utils.image_utils import ImageSource, image_to_base64

from .parser import UITarsEPMessage
from .prompts import PROMPT, PROMPT_QA


class UiTarsApiHandlerSettings(BaseSettings):
    """Settings for TARS API."""

    tars_url: HttpUrl = Field(
        validation_alias="TARS_URL",
    )
    tars_api_key: SecretStr = Field(
        min_length=1,
        validation_alias="TARS_API_KEY",
    )


class UiTarsApiHandler:
    def __init__(
        self,
        agent_os: AgentOs,
        reporter: Reporter,
        settings: UiTarsApiHandlerSettings,
    ) -> None:
        self._agent_os = agent_os
        self._reporter = reporter
        self._settings = settings
        self._client = OpenAI(
            api_key=self._settings.tars_api_key.get_secret_value(),
            base_url=str(self._settings.tars_url),
        )

    def _predict(self, image_url: str, instruction: str, prompt: str) -> str | None:
        chat_completion = self._client.chat.completions.create(
            model="tgi",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url,
                            },
                        },
                        {"type": "text", "text": prompt + instruction},
                    ],
                }
            ],
            top_p=None,
            temperature=None,
            max_tokens=150,
            stream=False,
            seed=None,
            stop=None,
            frequency_penalty=None,
            presence_penalty=None,
        )
        return chat_completion.choices[0].message.content

    def locate_prediction(
        self, image: Union[pathlib.Path, Image.Image], locator: str
    ) -> tuple[int | None, int | None]:
        askui_locator = f'Click on "{locator}"'
        prediction = self._predict(
            image_url=f"data:image/png;base64,{image_to_base64(image)}",
            instruction=askui_locator,
            prompt=PROMPT,
        )
        assert prediction is not None
        pattern = r"click\(start_box='(\(\d+,\d+\))'\)"
        match = re.search(pattern, prediction)
        if match:
            x, y = match.group(1).strip("()").split(",")
            x, y = int(x), int(y)
            if isinstance(image, pathlib.Path):
                image = Image.open(image)
            width, height = image.size
            x = (x * width) // 1000
            y = (y * height) // 1000
            return x, y
        return None, None

    def get_inference(self, image: ImageSource, query: str) -> str:
        response = self._predict(
            image_url=image.to_data_url(),
            instruction=query,
            prompt=PROMPT_QA,
        )
        if response is None:
            error_msg = f"No response from UI-TARS to query: {query}"
            raise QueryNoResponseError(error_msg, query)
        return response

    def act(self, goal: str) -> None:
        screenshot = self._agent_os.screenshot()
        self.act_history = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:image/png;base64,{image_to_base64(screenshot)}"
                            )
                        },
                    },
                    {"type": "text", "text": PROMPT + goal},
                ],
            }
        ]
        self.execute_act(self.act_history)

    def add_screenshot_to_history(self, message_history: list[dict[str, Any]]) -> None:
        screenshot = self._agent_os.screenshot()
        message_history.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": (
                                f"data:image/png;base64,{image_to_base64(screenshot)}"
                            )
                        },
                    }
                ],
            }
        )

    def filter_message_thread(
        self, message_history: list[dict[str, Any]], max_screenshots: int = 3
    ) -> list[dict[str, Any]]:
        """
        Filter message history to keep only the last n screenshots while preserving all text content.

        Args:
            message_history: List of message dictionaries
            max_screenshots: Maximum number of screenshots to keep (default: 5)
        """
        # Count screenshots from the end to keep track of the most recent ones
        screenshot_count = 0
        filtered_messages: list[dict[str, Any]] = []

        # Iterate through messages in reverse to keep the most recent screenshots
        for message in reversed(message_history):
            content = message["content"]

            if isinstance(content, list):
                # Check if message contains an image
                has_image = any(item.get("type") == "image_url" for item in content)

                if has_image:
                    screenshot_count += 1
                    if screenshot_count <= max_screenshots:
                        filtered_messages.insert(0, message)
                    else:
                        # Keep only text content if screenshot limit exceeded
                        text_content = [
                            item for item in content if item.get("type") == "text"
                        ]
                        if text_content:
                            filtered_messages.insert(
                                0, {"role": message["role"], "content": text_content}
                            )
                else:
                    filtered_messages.insert(0, message)
            else:
                filtered_messages.insert(0, message)

        return filtered_messages

    def execute_act(self, message_history: list[dict[str, Any]]) -> None:
        message_history = self.filter_message_thread(message_history)

        chat_completion = self._client.chat.completions.create(
            model="tgi",
            messages=message_history,
            top_p=None,
            temperature=None,
            max_tokens=150,
            stream=False,
            seed=None,
            stop=None,
            frequency_penalty=None,
            presence_penalty=None,
        )
        raw_message = chat_completion.choices[-1].message.content
        print(raw_message)

        if self._reporter is not None:
            self._reporter.add_message("UI-TARS", raw_message)

        try:
            message = UITarsEPMessage.parse_message(raw_message)
            print(message)
        except Exception as e:  # noqa: BLE001 - We want to catch all other exceptions here
            message_history.append(
                {"role": "user", "content": [{"type": "text", "text": str(e)}]}
            )
            self.execute_act(message_history)
            return

        action = message.parsed_action
        if action.action_type == "click":
            self._agent_os.mouse(action.start_box.x, action.start_box.y)
            self._agent_os.click("left")
            time.sleep(1)
        if action.action_type == "type":
            self._agent_os.click("left")
            self._agent_os.type(action.content)
            time.sleep(0.5)
        if action.action_type == "hotkey":
            self._agent_os.keyboard_pressed(action.key)
            self._agent_os.keyboard_release(action.key)
            time.sleep(0.5)
        if action.action_type == "call_user":
            time.sleep(1)
        if action.action_type == "wait":
            time.sleep(2)
        if action.action_type == "finished":
            return

        self.add_screenshot_to_history(message_history)
        self.execute_act(message_history)

    def _filter_messages(
        self, messages: list[UITarsEPMessage], max_messages: int
    ) -> list[UITarsEPMessage]:
        return messages[-max_messages:]
