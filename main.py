# main.py
# Central entry point for the project
from api_client import APIClient
from json_utils import save_json
import os

import argparse

import concurrent.futures

def main():
    parser = argparse.ArgumentParser(description="API Chaining Pipeline")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--run-all', action='store_true', help='Run all steps (default)')
    group.add_argument('--only-last', action='store_true', help='Only run the last step (API details)')
    parser.add_argument('--max-workers', type=int, default=10, help='Number of concurrent workers for API details step (default: 10)')
    parser.add_argument('--product', type=str, help='Only process the specified product name')
    args = parser.parse_args()

    client = APIClient()
    os.makedirs('tmp', exist_ok=True)
    from json_utils import load_json
    products_path = os.path.join('tmp', 'products.json')

    # Step 0 and 1: Only run if not --only-last
    if not args.only_last:
        # 0. Fetch all product names if not present
        if not os.path.exists(products_path):
            print(f"products.json not found at {products_path}. Fetching product names...")
            product_names = client.get_all_product_names()
            save_json(product_names, products_path)
            print(f"Fetched and saved {len(product_names)} product names to {products_path}")
        else:
            product_names = load_json(products_path)
        # If --product is specified, filter product_names
        if args.product:
            if args.product in product_names:
                product_names = [args.product]
            else:
                print(f"Product '{args.product}' not found in products.json.")
                return

        # 1. For each product, fetch API names and save to tmp/get_api_names_for_product/results/{productname}.json
        results_dir = os.path.join('tmp', 'get_api_names_for_product', 'results')
        os.makedirs(results_dir, exist_ok=True)
        for product in product_names:
            try:
                api_names = client.get_api_names_for_product(product)
                save_json(api_names, os.path.join(results_dir, f'{product}.json'))
                print(f"Saved {len(api_names)} APIs for {product} to {results_dir}/{product}.json")
            except Exception as e:
                print(f"Failed to fetch/save APIs for {product}: {e}")
    else:
        # On --only-last, just load product names
        if not os.path.exists(products_path):
            print(f"products.json not found at {products_path}. Cannot proceed.")
            return
        product_names = load_json(products_path)
        # If --product is specified, filter product_names
        if args.product:
            if args.product in product_names:
                product_names = [args.product]
            else:
                print(f"Product '{args.product}' not found in products.json.")
                return
        results_dir = os.path.join('tmp', 'get_api_names_for_product', 'results')

    # 2. For each product, for each API name, fetch API details and save to tmp/api_desc/{product}/{apiname}.json
    def fetch_and_save_api_detail(product, api_name):
        output_dir = os.path.join('tmp', 'get_api_request_details_by_api_and_product', product)
        os.makedirs(output_dir, exist_ok=True)
        try:
            api_detail = client.get_api_details_by_name(product, api_name)
            save_json(api_detail, os.path.join(output_dir, f'{api_name}.json'))
            print(f"Saved API details for {product}/{api_name} to {output_dir}/{api_name}.json")
        except Exception as e:
            print(f"Failed to fetch/save API details for {product}/{api_name}: {e}")

    tasks = []
    for product in product_names:
        product_api_path = os.path.join(results_dir, f'{product}.json')
        if not os.path.exists(product_api_path):
            print(f"API names file missing for {product}: {product_api_path}")
            continue
        api_names = load_json(product_api_path)
        for api_name in api_names:
            tasks.append((product, api_name))

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.max_workers) as executor:
        futures = [executor.submit(fetch_and_save_api_detail, product, api_name) for product, api_name in tasks]
        for future in concurrent.futures.as_completed(futures):
            pass  # All output is handled in fetch_and_save_api_detail

if __name__ == "__main__":
    main()
