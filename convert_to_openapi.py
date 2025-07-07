# convert_to_openapi.py
"""
Convert Huawei API Explorer details JSON to OpenAPI 3.0 YAML.
Usage:
    python convert_to_openapi.py --input <input_json_path> --output <output_yaml_path>
"""
import json
import yaml
import argparse
import os

def convert_api_details_to_openapi3(api_details):
    openapi_info = {
          "title": api_details.get("name", "API"),
            "description": api_details.get("summary", ""),
            "version": "1.0.0"
    }
    openapi_servers = api_details.get("host")

    return openapi

def main():
    parser = argparse.ArgumentParser(description="Convert API details JSON to OpenAPI 3.0 YAML.")
    parser.add_argument('--input', required=True, help='Input JSON file path')
    parser.add_argument('--output', required=True, help='Output YAML file path')
    args = parser.parse_args()

    with open(args.input, 'r', encoding='utf-8') as f:
        api_details = json.load(f)
    openapi3 = convert_api_details_to_openapi3(api_details)
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        yaml.dump(openapi3, f, sort_keys=False, allow_unicode=True)
    print(f"Converted {args.input} to OpenAPI 3.0 YAML at {args.output}")

if __name__ == "__main__":
    main()
