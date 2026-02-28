import os
import json
import argparse
import sys
from pathlib import Path

try:
    import tiktoken
except ImportError:
    print("❌ Error: 'tiktoken' library is missing.")
    print("💡 Please run: pip install tiktoken")
    sys.exit(1)

# Common binary or irrelevant file extensions to skip
IGNORE_EXTENSIONS = {
    '.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.tar', '.gz', '.exe', 
    '.dll', '.so', '.pyc', '.node', '.mp4', '.mp3', '.woff', '.woff2', '.ttf'
}

# Directories to skip entirely
IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'dist', 'build', '.venv', '.openclaw'}

# Cost per 1M tokens (Default: $2.50 - average of Pro/Sonnet models)
DEFAULT_COST_PER_1M = 2.50
# Token limit per file before flagging as 'Context Risk' (Approx 100k tokens for GPT-4 compatibility)
TOKEN_RISK_THRESHOLD = 100000

def get_tokens(text, model="gpt-4o"):
    """Returns number of tokens for a given string using tiktoken."""
    try:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))
    except Exception as e:
        print(f"Error encoding text: {e}")
        return 0

def scan_directory(root_path, model="gpt-4o"):
    results = []
    total_tokens = 0
    total_files = 0

    for root, dirs, files in os.walk(root_path):
        # Prune ignore directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in IGNORE_EXTENSIONS:
                continue

            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    tokens = get_tokens(content, model)
                    
                    if tokens > 0:
                        rel_path = os.path.relpath(file_path, root_path)
                        risk = "HIGH" if tokens > TOKEN_RISK_THRESHOLD else "LOW"
                        results.append({
                            "path": rel_path,
                            "tokens": tokens,
                            "size_kb": round(os.path.getsize(file_path) / 1024, 2),
                            "risk": risk
                        })
                        total_tokens += tokens
                        total_files += 1
            except Exception as e:
                # print(f"Skipping {file}: {e}")
                continue

    # Sort by token count
    results.sort(key=lambda x: x['tokens'], reverse=True)
    
    total_cost = (total_tokens / 1_000_000) * DEFAULT_COST_PER_1M
    
    return {
        "summary": {
            "total_files": total_files,
            "total_tokens": total_tokens,
            "estimated_cost_usd": round(total_cost, 4),
            "token_threshold": TOKEN_RISK_THRESHOLD
        },
        "top_files": results[:10],
        "all_files": results
    }

def print_summary(report):
    s = report['summary']
    print("\n" + "="*50)
    print(" 🛡️  CONTEXT GUARD - HEALTH REPORT")
    print("="*50)
    print(f"Total Files Analyzed: {s['total_files']}")
    print(f"Total Tokens:         {s['total_tokens']:,}")
    print(f"Estimated Cost (1M):  ${s['estimated_cost_usd']}")
    print("-" * 50)
    print(f"{'PATH':<40} | {'TOKENS':<10} | {'RISK'}")
    print("-" * 50)
    for f in report['top_files']:
        path = (f['path'][:37] + '..') if len(f['path']) > 37 else f['path']
        print(f"{path:<40} | {f['tokens']:<10,} | {f['risk']}")
    print("="*50 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="🛡️ Context Guard: Audit your code context for AI agents.")
    parser.add_argument("path", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    full_path = os.path.abspath(args.path)
    report = scan_directory(full_path)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_summary(report)
