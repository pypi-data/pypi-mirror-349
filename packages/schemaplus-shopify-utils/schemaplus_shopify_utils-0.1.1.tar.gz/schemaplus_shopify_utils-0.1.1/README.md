# Shopify Utils

A collection of utility functions for working with the Shopify API, with a focus on GraphQL endpoints.

## Features

- Fetch published products with pagination support
- Customizable product fields
- Sorting options
- Proper error handling

## Installation

```bash
pip install schemaplus-shopify-utils
```

## Usage

```python
from schemaplus_shopify_utils.product_utils import get_published_products

# Replace with your shop details
shop = {
    "name": "your-store.myshopify.com",
    "token": "your_access_token"
}

# Get published products
total_count, products = get_published_products(
    shop,
    count=10,
    with_additional_fields=True
)

# Process products
for product in products:
    print(f"- {product['title']} ({product['handle']})")
```

## License

MIT
