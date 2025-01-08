#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
import json

from src.llm_tools.core.core import LLMToolsCore
from src.llm_tools.core.config import LLMConfig
from src.llm_tools.document_tasks import DocumentTasks

def main():
    parser = argparse.ArgumentParser(description="LLM Tools CLI")
    
    # Required arguments
    parser.add_argument('input', help='Input file to process')
    parser.add_argument('--task', required=True, 
                       choices=['translate', 'summary', 'distill', 'correct'],
                       help='Processing task to perform')
    parser.add_argument('--output', required=True,
                       help='Output file path')
    
    # Optional arguments
    parser.add_argument('--api-url', default='http://localhost:5001',
                       help='KoboldCPP API URL')
    parser.add_argument('--api-password', default='',
                       help='API password if required')
    parser.add_argument('--templates', default='templates',
                       help='Templates directory path')
    parser.add_argument('--language', default='English',
                       help='Target language for translation')
    
    args = parser.parse_args()
    
    try:
        # Create config file from arguments
        config_dict = {
            "api_url": args.api_url,
            "api_password": args.api_password,
            "templates_directory": args.templates,
            "translation_language": args.language,
            "text_completion": False,
            "temp": 0.2,
            "top_k": 0,
            "top_p": 1.0,
            "rep_pen": 1.1,
            "min_p": 0.02
        }
        config_path = Path("config.json")
        with open(config_path, 'w') as f:
            json.dump(config_dict, f)
        core = LLMToolsCore(config_path)
        processor = DocumentTasks(core)
        results, metadata = processor.process_file(args.task, args.input)
        with open(args.output, 'w', encoding='utf-8') as f:
            for chunk in results:
                f.write(f"{chunk}\n\n")
        print(f"Processing complete. Output written to {args.output}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()