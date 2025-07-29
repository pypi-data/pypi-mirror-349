# token_itemize/cli.py
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description="Token Itemize: Count tokens for files and prompts."
    )
    parser.add_argument(
        '--gui',
        action='store_true',
        help='Launch graphical interface.'
    )
    parser.add_argument(
        '--prompt',
        type=str,
        help='User prompt (wrap in quotes if containing spaces).'
    )
    parser.add_argument(
        '--file',
        action='append',
        help='Individual file to process.'
    )
    parser.add_argument(
        '--folder',
        action='append',
        help='Folder to process.'
    )
    parser.add_argument(
        '--exclude',
        type=str,
        help='Regex pattern to exclude files.'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging.'
    )
    parser.add_argument(
        '--api',
        action='store_true',
        help='Enable API mode for tokenization.'
    )
    parser.add_argument(
        '--endpoint',
        type=str,
        help='API endpoint URL (for Ollama or DeepSeek).'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='LLM model name (required in API mode).'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='API key for authentication.'
    )
    parser.add_argument(
        '--cost-rate',
        type=float,
        default=0.03,
        help='Cost rate per 1k tokens.'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Enable batch processing for large directories.'
    )
    parser.add_argument(
        '--output-format',
        choices=['json', 'csv'],
        default='json',
        help='Output format for results.'
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help='Display package version and exit.'
    )
    parser.add_argument(
        '--gitignore',
        action='store_true',
        help='If a .gitignore file is present, skip files and directories listed in it.'
    )
    parser.add_argument(
        '--provider',
        type=str,
        default='ollama',
        choices=['ollama', 'openai', 'deepseek', 'openrouter'],
        help='API provider to use.'
    )
    parser.add_argument(
        '--save-transcript',
        action='store_true',
        help='Save the conversation transcript as Markdown.'
    )
    return parser.parse_args()
