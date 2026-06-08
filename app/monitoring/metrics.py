from prometheus_client import Counter,Gauge,Histogram

products_processed = Counter(
    "products_processed_total",
    "Total products Processed"
)

api_requests = Counter(
    "api_requests_total",
    'Total API Requests'
)

current_products = Gauge(
    "current_products",
    "Current number of products"
)

request_duration = Histogram(
    "api_request_duration_seconds",
    "API request duration"
)

api_errors = Counter(
    "api_errors_total",
    "Total API Errors"
)