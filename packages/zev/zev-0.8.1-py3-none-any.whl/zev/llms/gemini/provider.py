import json
import urllib.error
import urllib.request

from zev.config import config
from zev.constants import GEMINI_BASE_URL, GEMINI_DEFAULT_MODEL, PROMPT
from zev.llms.inference_provider_base import InferenceProvider
from zev.llms.types import OptionsResponse

GEMINI_RESPONSE_SCHEMA = {
    "response_mime_type": "application/json",
    "response_schema": {
        "type": "OBJECT",
        "properties": {
            "commands": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "command": {"type": "STRING"},
                        "short_explanation": {"type": "STRING"},
                        "is_dangerous": {"type": "BOOLEAN"},
                        "dangerous_explanation": {"type": "STRING"},
                    },
                    "required": [
                        "command",
                        "short_explanation",
                        "is_dangerous",
                    ],
                },
            },
            "is_valid": {"type": "BOOLEAN"},
            "explanation_if_not_valid": {"type": "STRING"},
        },
        "required": [
            "commands",
            "is_valid",
        ],
    },
}


class GeminiProvider(InferenceProvider):
    def __init__(self):
        if not config.gemini_api_key:
            raise ValueError("GEMINI_API_KEY must be set. Try running `zev --setup`.")

        self.model = config.gemini_model or GEMINI_DEFAULT_MODEL
        self.api_url = f"{GEMINI_BASE_URL}/v1beta/models/{self.model}:generateContent?key={config.gemini_api_key}"

    def get_options(self, prompt: str, context: str) -> None:
        assembled_prompt = PROMPT.format(prompt=prompt, context=context)
        headers = {"Content-Type": "application/json"}
        body = json.dumps(
            {
                "contents": [{"parts": [{"text": assembled_prompt}]}],
                "generationConfig": GEMINI_RESPONSE_SCHEMA,
            }
        ).encode("utf-8")
        request = urllib.request.Request(self.api_url, data=body, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(request) as response:
                data = json.loads(response.read().decode())
                text_output = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed_json = json.loads(text_output)
                return OptionsResponse(**parsed_json)
        except urllib.error.HTTPError as e:
            try:
                error_data = json.loads(e.read().decode())
                print("Error:", error_data["error"]["message"])
            except Exception:
                print("HTTP Error:", e.code)
            print("Note that to update settings, you can run `zev --setup`.")
        except Exception as e:
            print(f"Unexpected error: {e}")
        return None
