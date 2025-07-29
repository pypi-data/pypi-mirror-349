# token_itemize/main.py
import sys
import json
import csv
from token_itemize.cli import parse_args
from token_itemize.config import load_config
from token_itemize.utils import collect_files, process_file
from token_itemize import __version__

def main():
    args = parse_args()
    
    if args.version:
        print(f"token-itemize version {__version__}")
        sys.exit(0)
    
    # Load defaults from config.yaml (if available)
    config = load_config()

    if args.gui:
        from token_itemize.gui.gui_app import launch_gui
        launch_gui()
        return

    # Collect files based on --file and --folder arguments.
    files = collect_files(
        file_list=args.file,
        folder_list=args.folder,
        exclude_pattern=args.exclude,
        verbose=args.verbose,
        use_gitignore=args.gitignore
    )
    
    results = []
    
    if args.api:
        # API mode: select provider and use the unified API client.
        from token_itemize.api.api_client import get_api_client
        client = get_api_client(
            provider=args.provider,
            endpoint=args.endpoint,
            model=args.model,
            api_key=args.api_key,
            cost_rate=args.cost_rate,
            verbose=args.verbose
        )
        response = client.count_tokens(files=files, prompt=args.prompt)
        results = response
        
        # Save conversation transcript as Markdown if requested.
        if args.save_transcript:
            conversation = {
                "provider": args.provider,
                "prompt": args.prompt or "",
                "files": files,
                "response": response.get("full_response", ""),
                "input_tokens": response.get("input_tokens", 0),
                "output_tokens": response.get("output_tokens", 0)
            }
            from token_itemize.api.conversation_saver import save_conversation_markdown
            transcript_file = save_conversation_markdown(conversation)
            if args.verbose:
                print(f"Conversation transcript saved to {transcript_file}")
    else:
        # Process files locally.
        total_input_tokens = 0
        for file in files:
            try:
                token_count, details = process_file(file, verbose=args.verbose)
                results.append({
                    "file": file,
                    "tokens": token_count,
                    "details": details
                })
                total_input_tokens += token_count
            except Exception as e:
                if args.verbose:
                    print(f"Error processing {file}: {str(e)}")
        if args.prompt:
            from token_itemize.tokenizers.text_tokenizer import count_text_tokens
            prompt_tokens, prompt_details = count_text_tokens(args.prompt, verbose=args.verbose)
            results.append({
                "prompt": args.prompt,
                "tokens": prompt_tokens,
                "details": prompt_details
            })
            total_input_tokens += prompt_tokens

    # Calculate cost
    total_tokens = sum(item["tokens"] for item in results if "tokens" in item and isinstance(item["tokens"], (int, float)))
    cost = (total_tokens / 1000) * args.cost_rate

    output_data = {
        "results": results,
        "total_tokens": total_tokens,
        "total_cost": cost
    }

    # Output results in the requested format.
    if args.output_format == 'json':
        print(json.dumps(output_data, indent=2))
    elif args.output_format == 'csv':
        csv_file = "token_itemize_results.csv"
        with open(csv_file, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["File/Prompt", "Token Count", "Details"])
            for item in results:
                key = item.get("file", item.get("prompt", ""))
                writer.writerow([key, item["tokens"], item["details"]])
            writer.writerow([])
            writer.writerow(["Total Tokens", total_tokens])
            writer.writerow(["Total Cost", cost])
        print(f"Results written to {csv_file}")

if __name__ == '__main__':
    main()
