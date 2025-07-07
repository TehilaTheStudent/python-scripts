# config.py
# Central configuration for API requests and project settings

API_BASE_URL = "https://apiexplorer.ap-southeast-3.myhuaweicloud.com/v4/apis/detail"

DEFAULT_HEADERS = {
    "X-Language": "en-us",
    # Add other common headers here if needed
}

# Optionally, store cookies or secrets here (for demo purposes only)
DEFAULT_COOKIES = {
    "HWWAFSESID": "b80f9730e7dced55c8",
    "HWWAFSESTIME": "1751864219440"
}

# Example of product/request to query
def get_api_params(product_short="CodeArtsPipeline", name="ListTemplates", region_id="ap-southeast-3"):
    return {
        "product_short": product_short,
        "name": name,
        "region_id": region_id,
    }
