import requests
import json
import os
import pprint


class Bot():
    def __init__(self) -> None:
        self.api_endpoint = "https://openrouter.ai/api/v1/chat/completions"
        token = os.getenv("OPENROUTER_TOKEN");
        self.api_key = token  # Replace with your actual OpenRouter API key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self._import_context()

    def _import_context(self):
        try:
            with open("./cached_context.json", "r") as file:
                cached_messages = json.load(file)
                self.messages =   self._init_messages() + cached_messages
        except FileNotFoundError:
            self.messages = self._init_messages()

    def _init_messages(self):
        with open("./systemprompt.txt", "r") as file:
            system_content = file.read()
        return [{"role": "system", "content": system_content}]

    def ask_image(self, base64_image, caption=None):
        image_msg = {
                "role": "user",
                "content": [{
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }]
            }
        if caption:
            caption_msg = {
                "role": "user",
                "content": caption
            }
            self.messages.append(caption_msg)
            image_msg["content"].append(caption_msg)
        payload = {
            "model": "google/gemini-flash-1.5",
            "messages": self.messages + [image_msg]
        }
        response = requests.post(self.api_endpoint, json=payload, headers=self.headers)
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            answer = response_data['choices'][0]['message']
            self.messages.append(answer)
            return answer["content"]
        else:
            raise Exception(response)

    def add_context(self, message):
        self.messages.append({
            "role": "user",
            "content": message
        });

    def cache_context(self):
        "function saves last 100 messages to a file"
        with open("./cached_context.json", "w", encoding="utf-8") as file:
            json.dump(self.messages[-1000:][1:], file)

    def ask(self, text) -> str:
        self.messages.append({
            "role": "user",
            "content": text
        })
        payload = {
            "model": "google/gemini-flash-1.5",
            "messages": self.messages,
        }
        response = requests.post(self.api_endpoint, json=payload, headers=self.headers)
        if response.status_code == 200:
            response_data = response.json()
            print(response_data)
            answer = response_data['choices'][0]['message']
            self.messages.append(answer)
            return answer["content"]
        else:
            raise Exception(response)

    def ask_stream(self, text):
        self.messages.append({
            "role": "user",
            "content": text
        })
        payload = {
            "model": "google/gemini-flash-1.5",
            "messages": self.messages,
            "stream": True
        }
        print("ASKING");
        response = requests.post(self.api_endpoint, json=payload, headers=self.headers, stream=True)
        if response.status_code == 200:
            return self._handle_stream(response.iter_lines())
        else:
            pprint.pprint(response.reason)
            raise Exception(response)

    def _handle_stream(self, stream):
        message = {"role": "assistant", "content": ""}
        for line in stream:
            if line:
                decoded_line = line.decode('utf-8')
                if decoded_line.startswith("data: "):
                    json_data = decoded_line[6:]
                    if json_data == "[DONE]":
                        break
                    response_data = json.loads(json_data)
                    if 'choices' not in response_data or len(response_data['choices']) == 0:
                        raise Exception(f"No choices in response data: {response_data}")
                    delta = response_data['choices'][0]['delta']
                    if "content" in delta:
                        message["content"] += delta["content"]
                        yield {"token": delta["content"]}
                        self.messages.append(message)

    def reset(self):
        self.messages = self._init_messages()
        if os.path.exists("./cached_context.json"):
            os.remove("./cached_context.json")
