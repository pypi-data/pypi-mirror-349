# Token Itemize

Token Itemize is a versatile Python package engineered to accurately count tokens across a wide array of file formats, including text, images, audio, and video. It seamlessly integrates with various Large Language Model (LLM) APIs, enabling precise cost calculation for your AI workloads. Token Itemize offers both a user-friendly Command-Line Interface (CLI) and an intuitive Graphical User Interface (GUI), catering to users of all technical levels.

## ✨ Key Features

- **Comprehensive Multi-Format Tokenization:**
    - **Text Files:** Leverages `tiktoken` for advanced tokenization or offers a simple whitespace splitting method for basic text analysis.
    - **Images:** Decomposes images into 16x16 pixel patches for a granular token estimation.
    - **Audio Files:** Employs spectrogram window estimation for detailed audio analysis, supporting popular formats like .wav, .mp3, and .flac.
    - **Video Files:** Processes video by extracting frames and applying image tokenization techniques for frame-by-frame analysis.

- **Flexible API Integration:**
    - **LLM API Compatibility:** Designed to work with both local and cloud-based LLM endpoints.
    - **Configurable API Settings:** Allows easy customization of API parameters such as endpoint URLs, model names, and API keys.
    - **Broad Provider Support:** Supports a range of API providers including:
        - **Ollama:** For local LLMs.
        - **OpenAI:** Including models like GPT-3.5 Turbo and GPT-4 Vision.
        - **DeepSeek:** For efficient and cost-effective models.
        - **OpenRouter:** To access a wide range of models through a single API key.

- **Command-Line Interface (CLI) for Power Users:**
    - **Efficient File Processing:** Process individual files and entire folders directly from the command line.
    - **Prompt Specification:** Easily include prompts for API-based tokenization directly in your commands.
    - **File Exclusion:** Utilize regular expressions to exclude specific files or patterns for precise processing.
    - **Batch Processing:** Optimized for handling large directories with batch processing capabilities.
    - **Versatile Output Formats:** Export results in both JSON and CSV formats for easy data handling and reporting.
    - **Cost Management:** Configure the cost rate per 1k tokens to accurately estimate expenses.
    - **Verbose Logging:** Option for detailed logging to track processing and debug issues.

- **Graphical User Interface (GUI) for Ease of Use:**
    - **Drag and Drop Functionality:** Simply drag and drop files or folders into the GUI for immediate processing.
    - **Intuitive Prompt Input:** Clear fields to enter prompts and adjust API settings within the interface.
    - **Real-time Progress Tracking:** Built-in progress bar to monitor the tokenization process.
    - **Simple Result Export:** Easily export tokenization results in CSV or JSON format through the GUI.
    - **Gitignore Integration:** Option to automatically apply `.gitignore` rules to exclude files, streamlining project analysis.

- **Advanced Efficiency Tools:**
    - **Intelligent Caching:** Employs a caching system to avoid redundant processing of unchanged files, saving time and resources.
    - **Parallel Processing:** Leverages parallel processing for batch operations to significantly speed up token counting for large datasets.
    - **Cost Calculation and Estimation:** Automatically calculates costs based on token counts, using a default rate of $0.03 per 1k tokens, customizable to your specific pricing.

## ⚙️ CLI Commands

Token Itemize CLI offers a rich set of options to tailor token counting to your specific needs.

```text
Usage: token-itemize [options]

Available Options:
  --gui                       Launch the graphical user interface.
  --prompt PROMPT             User prompt for API processing (text prompt).
  --file FILE                 Individual file to process (can be specified multiple times).
  --folder FOLDER             Folder to process (can be specified multiple times for batch processing).
  --exclude REGEX             Regular expression pattern to exclude files from processing.
  --verbose                   Enable verbose logging for detailed output.
  --api                       Enable API mode for tokenization and cost estimation.
  --provider PROVIDER         Specify the API provider (ollama, openai, deepseek, openrouter).
  --endpoint URL              API endpoint URL for providers like Ollama and DeepSeek.
  --model MODEL               LLM model name (required in API mode, provider-specific).
  --api-key KEY               API key for authentication (required for OpenAI, DeepSeek, OpenRouter).
  --cost-rate RATE            Cost rate per 1k tokens (default: 0.03). Customize for different models or providers.
  --batch                     Enable batch processing for large directories to improve performance.
  --output-format FORMAT      Output format for results (json or csv, default: json).
  --gitignore                 Enable .gitignore filtering to exclude files.
  --version                   Display package version and exit.

```

**Examples:**

- **Launch GUI:**
  ```bash
  token-itemize --gui
  ```

- **Process a single file with API:**
  ```bash
  token-itemize --api --provider openai --model gpt-3.5-turbo --api-key YOUR_OPENAI_API_KEY --prompt "Summarize this document" --file document.txt
  ```

- **Process a folder and exclude specific files:**
  ```bash
  token-itemize --folder project_docs --exclude ".*\.log" --output-format csv --verbose
  ```

- **Process a video file and calculate tokens:**
  ```bash
  token-itemize --file video.mp4
  ```

## 💻 GUI Usage

For users who prefer a visual approach, Token Itemize provides a Graphical User Interface.

**Launching the GUI:**

```bash
token-itemize --gui
```

**Key GUI Features:**

1.  **File and Folder Selection:** Use the "Add Files" and "Add Folder" buttons to easily import files or directories for tokenization. Drag and drop functionality is also supported.
2.  **Prompt Input:** Enter your text prompts in the designated "Prompt" text area for API-based processing.
3.  **API Settings Configuration:** Enable API mode with the checkbox and configure:
    - **Provider Selection:** Choose your API provider from a dropdown (Ollama, OpenAI, DeepSeek, OpenRouter).
    - **Endpoint URL:**  Specify the API endpoint if needed (e.g., for local Ollama or DeepSeek instances).
    - **Model Name:** Enter the model identifier for your chosen provider.
    - **API Key:** Input your API key for authentication with services like OpenAI, DeepSeek, and OpenRouter.
4.  **Gitignore Filtering:** Check the ".gitignore Filtering" box to automatically apply `.gitignore` rules to your selected files and folders, excluding any files listed in your `.gitignore` file.
5.  **Start Token Counting:** Click the "Count Tokens" button to begin the tokenization process. A progress bar at the bottom of the window will indicate the current status.
6.  **Results Display:** The results table will populate, showing the file name (or "Prompt" for API-only prompts), token counts, and processing details for each item. A "Total" row summarizes the total tokens and estimated cost (if applicable).
7.  **Error Handling:** Error messages are displayed in pop-up dialogs for clear communication of issues during processing.
8.  **Export Results:** Use the "Export Results" button to save the results table as either a CSV (.csv) or JSON (.json) file.

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher is required.

### Installation via pip (Recommended)

The easiest way to install Token Itemize is using pip, Python's package installer. Open your terminal and run:

```bash
pip install token-itemize
```

This command will download and install Token Itemize and all necessary dependencies.

### Installation from Source (for developers)

If you are a developer or want to contribute to Token Itemize, you can install it from source:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/BenevolenceMessiah/token-itemize.git
   ```

2. **Navigate to the Project Directory:**
   ```bash
   cd token-itemize
   ```

3. **Install Dependencies and the Package:**
   ```bash
   pip install .
   ```
   or if you plan to develop:
   ```bash
   pip install -e .
   ```

## 🚀 API Client Usage in Python

Token Itemize is not just a CLI and GUI tool; it's also a Python library! You can directly integrate its API client into your Python scripts for programmatic token counting and API interactions.

```python
from token_itemize.api.api_client import get_api_client

# Example: Using OpenAI API Client
api_client_openai = get_api_client(
    provider="openai",
    api_key="YOUR_OPENAI_API_KEY",
    model="gpt-3.5-turbo",
    verbose=True
)
openai_result = api_client_openai.count_tokens(files=["document1.txt", "image.png"], prompt="Analyze these files.")
print(f"OpenAI Input Tokens: {openai_result['input_tokens']}")
print(f"OpenAI Response: {openai_result['full_response']}")


# Example: Using Ollama API Client (for local models)
api_client_ollama = get_api_client(
    provider="ollama",
    endpoint="http://localhost:11434", # Default Ollama endpoint
    model="llama2:latest",
    verbose=True
)
ollama_result = api_client_ollama.count_tokens(files=["document2.txt", "audio.wav"], prompt="Process these files with Ollama.")
print(f"Ollama Input Tokens: {ollama_result['input_tokens']}")
print(f"Ollama Response: {ollama_result['full_response']}")

```

You can use `get_api_client` to instantiate clients for "openai", "ollama", "deepseek", and "openrouter", passing in necessary credentials and settings.  Refer to the `token_itemize/api/api_client.py` for detailed class structures and available methods for each API provider.

## ⚙️ Configuration

### Config File (config.yaml)

Token Itemize supports configuration via a `config.yaml` file placed in the project root directory. This file allows you to set default API settings, which can be especially useful if you frequently use API mode.

```yaml
endpoint: "http://localhost:8000/api/tokenize" # Default API endpoint, can be overridden in CLI/GUI
model: "gpt-4-vision" # Default model, also overridable
api_key: "" # Default API key, ensure to set this or pass via CLI/GUI
cost_rate: 0.03 # Default cost rate per 1k tokens
```

Token Itemize will automatically load these settings when it starts, applying them as defaults for API operations, unless overridden by command-line arguments or GUI inputs.

## 💰 Cost Calculation

Token Itemize meticulously calculates the estimated cost by multiplying the total token count by a configurable cost rate. By default, the cost rate is set to $0.03 per 1,000 tokens. You can customize this rate to match the pricing of your specific LLM or API provider.

- **Configuration via CLI:** Use the `--cost-rate RATE` option when using the command-line interface.
- **Configuration via GUI:** The cost rate is set as a default within the GUI application but can be adjusted in the backend code if needed.
- **Configuration via API Client:** When using the Python API client, you can specify the `cost_rate` during client initialization.
- **Configuration via `config.yaml`:** Set a global default cost rate in the `config.yaml` file.

## 🗂️ Project Structure

```text
token-itemize/
├── token_itemize/                # Main package directory
│   ├── __init__.py             # Initializes the package
│   ├── api/                    # API related modules
│   │   ├── __init__.py         # Initializes the api submodule
│   │   ├── api_client.py       # API Client classes for different providers (OpenAI, Ollama, DeepSeek, OpenRouter)
│   │   └── conversation_saver.py # Functionality to save conversation transcripts
│   ├── tokenizers/             # Tokenization logic for different file types
│   │   ├── __init__.py         # Initializes the tokenizers submodule
│   │   ├── audio_tokenizer.py  # Tokenizer for audio files
│   │   ├── image_tokenizer.py  # Tokenizer for image files
│   │   ├── text_tokenizer.py   # Tokenizer for text files
│   │   └── video_tokenizer.py  # Tokenizer for video files
│   ├── utils/                    # Utility functions
│   │   ├── cache.py            # Caching mechanisms for token counts
│   ├── cli.py                    # Command-line interface logic
│   ├── config.py                 # Configuration loading and handling
│   ├── gui/                    # Graphical user interface components
│   │   ├── __init__.py         # Initializes the gui submodule
│   │   └── gui_app.py          # PyQt5 GUI application
│   ├── main.py                   # Main entry point for the CLI and GUI
├── tests/                      # Test suite
│   ├── __init__.py             # Initializes the tests package
│   ├── test_api_client.py      # Tests for API client functionality
│   ├── test_edge_cases.py      # Tests for edge case scenarios
│   ├── test_text_tokenizer.py  # Tests for text tokenization
│   ├── test_video_tokenizer.py # Tests for video tokenization
├── docs/                       # Documentation files (markdown format)
│   ├── api.md                  # API documentation
│   ├── contributing.md         # Contribution guidelines
│   └── index.md                # Main documentation index
├── .github/                    # GitHub workflow configurations
│   └── workflows/              # Workflow definitions
│       └── python-app.yml      # CI/CD workflow for testing
├── .gitignore                  # Specifies intentionally untracked files that Git should ignore
├── LICENSE                     # MIT License file
├── README.md                   # Project README file (this file)
├── MANIFEST.in                 # Lists files to include in package distribution
├── config.yaml                 # Default configuration file
├── pyproject.toml              # Build system configuration
├── requirements.txt            # Project dependencies
├── setup.py                    # Setup script for packaging
└── token-itemize.egg-info/      # Setuptools egg-info (created during installation)
    ├── ...                     # Various metadata files

```

## 🧑‍💻 Development & Testing

### Running Tests

To ensure the reliability and correctness of Token Itemize, a comprehensive suite of unit tests is included. To run the tests, navigate to the project's root directory and execute:

```bash
python -m unittest discover -s tests
```

This command will discover and run all tests located in the `tests/` directory, verifying the functionality of different components of Token Itemize.

### Contributing

We warmly welcome contributions to Token Itemize! Whether you're fixing bugs, adding new features, or improving documentation, your help is valuable. Please see `docs/contributing.md` for detailed guidelines on how to contribute to the project. Here's a quick start:

1.  **Fork the Repository:** Start by forking the Token Itemize repository on GitHub to your own account.
2.  **Create a Feature Branch:**
    ```bash
    git checkout -b feature/your-feature-name
    ```
3.  **Commit Your Changes:**
    ```bash
    git commit -am 'Add your feature or fix'
    ```
4.  **Push to the Branch:**
    ```bash
    git push origin feature/your-feature-name
    ```
5.  **Create a Pull Request:** Submit a pull request to the main repository with a clear description of your changes.

## 🤝 Support & Community

For any issues, questions, or feature requests, please open an issue on the GitHub repository. We are committed to providing support and continuously improving Token Itemize.

## 📜 License

Token Itemize is released under the MIT License, making it free for commercial and personal use. See the `LICENSE` file for the full license text.

## 📚 Documentation

For more in-depth information and advanced usage, refer to the full documentation available in the `docs` directory.

Thank you for choosing Token Itemize! We hope this tool enhances your workflow and simplifies token management and cost estimation for your projects. Happy tokenizing!