# JSON API Project

## Overview
A Python project to make API requests (example: Huawei CodeArtsPipeline API) and write responses to JSON files. Easily extendable and configurable.

## Structure
- `config.py`: Central config (API URLs, headers, etc.)
- `api_client.py`: API request logic (add more endpoints easily)
- `json_utils.py`: JSON read/write helpers
- `main.py`: Entry point
- `requirements.txt`: Dependencies

## Usage
1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Run the main script:
   ```sh
   python main.py
   ```
3. Output will be saved in `output/api_details.json`

## Extending
- Add new API methods in `api_client.py`
- Change API params in `main.py` or config
