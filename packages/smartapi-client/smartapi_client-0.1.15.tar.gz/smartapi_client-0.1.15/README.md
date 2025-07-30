# SmartAPI Client 🚀

A Python HTTP client for REST APIs with dynamic endpoint registration, retry logic, mock responses, and OpenAPI/Postman integration.

---

## 🔧 Features

- **Dynamic Endpoint Registration** – Generate API methods from OpenAPI/Postman specs  
- **Mock Responses** – Test APIs without real network calls  
- **Retry Logic** – Configurable retries for failed requests  
- **CLI Tool** – Convert Postman/OpenAPI specs to client-ready code  
- **Type Hints** – Full IDE support  
- **Error Handling** – 40+ HTTP status-specific exceptions  
- **Parameter Validation** – Path/query params auto-detection  
- **Business Error Detection** – Catch errors in successful responses  
- **SSL Verification** – Built-in security checks  

---

## 📦 Installation

```bash
pip install smartapi-client
```
⚡ Quick Start
```python
from smartapi import ApiClient, EndpointConfig

# Initialize client
client = ApiClient(
    "ExampleAPI",
    base_url="https://api.example.com",
    api_key="your_key_here",
    retry_options={"retries": 3}
)

# Register endpoints
client.register_endpoints([
    EndpointConfig(
        method="GET",
        path="/users/{user_id}",
        params=["user_id"],
        description="Get user details"
    )
])

# Call dynamically generated method
user = client.get_users(user_id=1)
```
🛠️ CLI Usage
Convert Postman/OpenAPI specs to client-ready endpoints:
```bash
smartapi generate \
  -i postman_collection.json \
  -t postman \
  -o endpoints.json \
  --base-url https://api.example.com
```

📚 Detailed Usage
1. Dynamic Endpoints
```python
client.register_endpoints([
    EndpointConfig(
        method="POST",
        path="/orders",
        params=["items", "shipping_address"],
        description="Create new order"
    ),
    EndpointConfig(
        method="GET",
        path="/orders/{order_id}",
        params=["order_id"],
        description="Retrieve order details"
    )
])

new_order = client.create_orders(
    items=["item1", "item2"],
    shipping_address="123 Main St"
)

order_details = client.get_orders(order_id="ORD-123")
```
2. Mock Responses
 ```python
 client = ApiClient(
  "TestAPI",
  test_mode=True,
  mock_responses={
      "GET /users/1": (200, {"id": 1, "name": "Test User"}),
      "POST /orders": {"status": "created"}
  }
)

# Returns mock data
user = client.get_users(user_id=1)  # Returns {"id": 1, "name": "Test User"}
```

3. Error Handling
```python
try:
    client.get_users(user_id=999)
except ApiNotFoundError as e:
    print(f"Error {e.status_code}: {e}")
except ApiRateLimitError as e:
    print(f"Retry after {e.retry_after} seconds")
except ApiClientError as e:
    print(f"Generic error: {e}")
```

4. Retry Configuration
```python
from smartapi import RetryConfig

client = ApiClient(
    "RetryDemo",
    retry_options=RetryConfig(
        retries=5,
        status_forcelist=[500, 502, 503, 504],
        backoff_factor=1.5
    )
)
```

5. Request/Response Hooks
```python
def add_tracing(headers):
    headers["X-Trace-ID"] = "trace_123"
    return headers

client = ApiClient(
    "TracedAPI",
    before_request=lambda method, url, params, headers, data: {
        "headers": add_tracing(headers)
    },
    after_response=lambda response, duration: 
        print(f"Request took {duration:.2f}s")
)
```
🔄 Convert API Specs
Postman Collections
```python
from smartapi import ApiClient

client = ApiClient.from_postman_collection(
    collection_path="postman_collection.json",
    base_url="https://api.example.com",
    save_endpoints=True,
    output_format="yaml"
)
```
OpenAPI Specifications
```python
client = ApiClient.from_openapi_spec(
    spec_path="openapi.yaml",
    base_url="https://api.example.com",
    api_name="SwaggerAPI"
)
```
🤝 Contributing
1.Fork the repository

2.Create a feature branch:

```bash
git checkout -b feature/awesome-feature
```
3.Commit your changes:

```bash
git commit -m 'Add awesome feature'
```
4.Push to your branch:
```bash
git push origin feature/awesome-feature
```

📄 License
MIT License – See LICENSE for details.



