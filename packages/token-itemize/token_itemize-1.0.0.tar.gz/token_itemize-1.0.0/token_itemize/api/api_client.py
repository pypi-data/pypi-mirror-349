# token_itemize/api/api_client.py
import os
import requests
import base64

class BaseAPIClient:
    def count_tokens(self, files, prompt=None):
        raise NotImplementedError()

# --- Ollama API Integration ---
class OllamaAPIClient(BaseAPIClient):
    def __init__(self, endpoint, model, api_key=None, cost_rate=0.03, verbose=False):
        self.endpoint = endpoint.rstrip('/')
        self.model = model
        self.api_key = api_key
        self.cost_rate = cost_rate
        self.verbose = verbose

    def process_files_for_ollama(self, files):
        text_contents = []
        images = []
        text_extensions = [
            '.txt', '.md', '.py', '.json', '.csv', '.ini', '.yaml', '.yml',
            '.js', '.bat', '.sh', '.sql', '.html', '.css'
        ]
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in text_extensions:
                try:
                    with open(f, "r", encoding="utf-8", errors="replace") as file_obj:
                        content = file_obj.read()
                        text_contents.append(f"File: {os.path.basename(f)}\n{content}\n")
                except Exception as e:
                    if self.verbose:
                        print(f"Error reading text file {f}: {e}")
            elif ext in image_extensions:
                try:
                    with open(f, "rb") as file_obj:
                        data = file_obj.read()
                        encoded = base64.b64encode(data).decode("utf-8")
                        images.append(encoded)
                except Exception as e:
                    if self.verbose:
                        print(f"Error reading image file {f}: {e}")
            else:
                if self.verbose:
                    print(f"Skipping unsupported file type for API mode: {f}")
        combined_text = "\n".join(text_contents)
        return combined_text, images

    def count_tokens(self, files, prompt=None):
        combined_text, images = self.process_files_for_ollama(files)
        if combined_text and prompt:
            combined_prompt = combined_text + "\n" + prompt
        elif combined_text:
            combined_prompt = combined_text
        else:
            combined_prompt = prompt or ""
        payload = {
            "model": self.model,
            "prompt": combined_prompt,
            "stream": False
        }
        if images:
            payload["images"] = images
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if self.verbose:
            print(f"Sending request to Ollama API at {self.endpoint}/api/generate with payload:")
            print(payload)
        try:
            url = self.endpoint + "/api/generate"
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            if self.verbose:
                print("Ollama API response:")
                print(data)
            input_tokens = data.get("prompt_eval_count", 0)
            output_tokens = data.get("eval_count", 0)
            result = {
                "results": [{
                    "prompt": combined_prompt,
                    "tokens": input_tokens,
                    "details": f"Ollama API prompt evaluation count: {input_tokens}"
                }],
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "full_response": data.get("response", "")
            }
            return result
        except requests.exceptions.Timeout:
            raise TimeoutError("Ollama API request timed out.")
        except requests.exceptions.HTTPError as e:
            raise ConnectionError(f"Ollama API HTTP error: {str(e)}")
        except Exception as e:
            raise ConnectionError(f"Error connecting to Ollama API: {str(e)}")

# --- OpenAI API Integration ---
class OpenAIApiClient(BaseAPIClient):
    def __init__(self, api_key, model="gpt-3.5-turbo", cost_rate=0.002, verbose=False):
        self.api_key = api_key
        self.model = model
        self.cost_rate = cost_rate
        self.verbose = verbose
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def process_files_for_openai(self, files):
        text_contents = []
        # OpenAI Chat API currently accepts only text prompt.
        text_extensions = [
            '.txt', '.md', '.py', '.json', '.csv', '.ini', '.yaml', '.yml',
            '.js', '.bat', '.sh', '.sql', '.html', '.css'
        ]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in text_extensions:
                try:
                    with open(f, "r", encoding="utf-8", errors="replace") as file_obj:
                        content = file_obj.read()
                        text_contents.append(f"File: {os.path.basename(f)}\n{content}\n")
                except Exception as e:
                    if self.verbose:
                        print(f"Error reading file {f}: {e}")
        combined_text = "\n".join(text_contents)
        return combined_text, []  # No image support for standard OpenAI Chat API

    def count_tokens(self, files, prompt=None):
        combined_text, _ = self.process_files_for_openai(files)
        if combined_text and prompt:
            combined_prompt = combined_text + "\n" + prompt
        elif combined_text:
            combined_prompt = combined_text
        else:
            combined_prompt = prompt or ""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": combined_prompt}],
        }
        if self.verbose:
            print(f"Sending request to OpenAI API at {self.endpoint} with payload:")
            print(payload)
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            result = {
                "results": [{
                    "prompt": combined_prompt,
                    "tokens": input_tokens,
                    "details": f"OpenAI prompt token count: {input_tokens}"
                }],
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "full_response": data.get("choices", [{}])[0].get("message", {}).get("content", "")
            }
            return result
        except Exception as e:
            raise ConnectionError(f"Error connecting to OpenAI API: {str(e)}")

# --- DeepSeek API Integration ---
class DeepSeekAPIClient(BaseAPIClient):
    def __init__(self, endpoint, api_key, model="default", cost_rate=0.002, verbose=False):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.cost_rate = cost_rate
        self.verbose = verbose

    def process_files_for_deepseek(self, files):
        text_contents = []
        images = []
        text_extensions = [
            '.txt', '.md', '.py', '.json', '.csv', '.ini', '.yaml', '.yml',
            '.js', '.bat', '.sh', '.sql', '.html', '.css'
        ]
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.tif']
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in text_extensions:
                try:
                    with open(f, "r", encoding="utf-8", errors="replace") as file_obj:
                        content = file_obj.read()
                        text_contents.append(f"File: {os.path.basename(f)}\n{content}\n")
                except Exception as e:
                    if self.verbose:
                        print(f"Error reading text file {f}: {e}")
            elif ext in image_extensions:
                try:
                    with open(f, "rb") as file_obj:
                        data = file_obj.read()
                        encoded = base64.b64encode(data).decode("utf-8")
                        images.append(encoded)
                except Exception as e:
                    if self.verbose:
                        print(f"Error reading image file {f}: {e}")
            else:
                if self.verbose:
                    print(f"Skipping unsupported file type for API mode: {f}")
        combined_text = "\n".join(text_contents)
        return combined_text, images

    def count_tokens(self, files, prompt=None):
        combined_text, images = self.process_files_for_deepseek(files)
        if combined_text and prompt:
            combined_prompt = combined_text + "\n" + prompt
        elif combined_text:
            combined_prompt = combined_text
        else:
            combined_prompt = prompt or ""
        headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model,
            "prompt": combined_prompt,
            "stream": False
        }
        if images:
            payload["images"] = images
        try:
            url = self.endpoint + "/generate"
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            input_tokens = data.get("prompt_eval_count", 0)
            output_tokens = data.get("eval_count", 0)
            result = {
                "results": [{
                    "prompt": combined_prompt,
                    "tokens": input_tokens,
                    "details": f"DeepSeek prompt evaluation count: {input_tokens}"
                }],
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "full_response": data.get("response", "")
            }
            return result
        except Exception as e:
            raise ConnectionError(f"Error connecting to DeepSeek API: {str(e)}")

# --- OpenRouter API Integration ---
class OpenRouterAPIClient(BaseAPIClient):
    def __init__(self, api_key, model="gpt-3.5-turbo", cost_rate=0.002, verbose=False):
        self.api_key = api_key
        self.model = model
        self.cost_rate = cost_rate
        self.verbose = verbose
        self.endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def process_files_for_openrouter(self, files):
        text_contents = []
        text_extensions = [
            '.txt', '.md', '.py', '.json', '.csv', '.ini', '.yaml', '.yml',
            '.js', '.bat', '.sh', '.sql', '.html', '.css'
        ]
        for f in files:
            ext = os.path.splitext(f)[1].lower()
            if ext in text_extensions:
                try:
                    with open(f, "r", encoding="utf-8", errors="replace") as file_obj:
                        content = file_obj.read()
                        text_contents.append(f"File: {os.path.basename(f)}\n{content}\n")
                except Exception as e:
                    if self.verbose:
                        print(f"Error reading file {f}: {e}")
        combined_text = "\n".join(text_contents)
        return combined_text, []  # OpenRouter Chat API supports text only

    def count_tokens(self, files, prompt=None):
        combined_text, _ = self.process_files_for_openrouter(files)
        if combined_text and prompt:
            combined_prompt = combined_text + "\n" + prompt
        elif combined_text:
            combined_prompt = combined_text
        else:
            combined_prompt = prompt or ""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": combined_prompt}],
        }
        try:
            response = requests.post(self.endpoint, json=payload, headers=headers, timeout=60)
            response.raise_for_status()
            data = response.json()
            usage = data.get("usage", {})
            input_tokens = usage.get("prompt_tokens", 0)
            output_tokens = usage.get("completion_tokens", 0)
            result = {
                "results": [{
                    "prompt": combined_prompt,
                    "tokens": input_tokens,
                    "details": f"OpenRouter prompt token count: {input_tokens}"
                }],
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "full_response": data.get("choices", [{}])[0].get("message", {}).get("content", "")
            }
            return result
        except Exception as e:
            raise ConnectionError(f"Error connecting to OpenRouter API: {str(e)}")

def get_api_client(provider, **kwargs):
    provider = provider.lower()
    if provider == "ollama":
        return OllamaAPIClient(
            endpoint=kwargs.get("endpoint"),
            model=kwargs.get("model"),
            api_key=kwargs.get("api_key"),
            cost_rate=kwargs.get("cost_rate", 0.03),
            verbose=kwargs.get("verbose", False)
        )
    elif provider == "openai":
        return OpenAIApiClient(
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "gpt-3.5-turbo"),
            cost_rate=kwargs.get("cost_rate", 0.002),
            verbose=kwargs.get("verbose", False)
        )
    elif provider == "deepseek":
        return DeepSeekAPIClient(
            endpoint=kwargs.get("endpoint"),
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "default"),
            cost_rate=kwargs.get("cost_rate", 0.002),
            verbose=kwargs.get("verbose", False)
        )
    elif provider == "openrouter":
        return OpenRouterAPIClient(
            api_key=kwargs.get("api_key"),
            model=kwargs.get("model", "gpt-3.5-turbo"),
            cost_rate=kwargs.get("cost_rate", 0.002),
            verbose=kwargs.get("verbose", False)
        )
    else:
        raise ValueError(f"Unsupported API provider: {provider}")
