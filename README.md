# ProductHub

A scalable Python-based product catalog integration platform designed to fetch product information from external APIs, process large datasets, and export structured data for analytics, reporting, and downstream applications.

## Overview

ProductHub is built to automate product data ingestion from external systems. It handles authentication, data collection, processing, and export while maintaining a clean and extensible architecture.

The project is designed to work across:

* Windows
* macOS
* Linux
* Docker
* Kubernetes

---

## Features

### Authentication Management

* OAuth / Token-based authentication
* Automatic token refresh
* Secure environment variable configuration

### Product Data Collection

* Fetch products from external APIs
* Paginated API support
* Large dataset processing

### Data Export

* Excel Export (.xlsx)
* CSV Export (Future)
* Database Storage (Future)

### Logging

* Application logging
* Error tracking
* Execution monitoring

### Cross Platform Support

* Windows
* macOS
* Ubuntu/Linux

---

## Project Structure

```text
ProductHub/
│
├── app/
│   ├── config/
│   │   └── settings.py
│   │
│   ├── clients/
│   │   └── api_client.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   └── product_service.py
│   │
│   ├── utils/
│   │   ├── logger.py
│   │   ├── excel_writer.py
│   │   └── folder_manager.py
│   │
│   └── models/
│
├── output/
├── logs/
├── tests/
│
├── .env
├── requirements.txt
├── README.md
└── main.py
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/ProductHub.git

cd ProductHub
```

### Create Virtual Environment

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file:

```env
BaseUrl=https://api.example.com
AuthUrl=/auth/token
href=/products?page=
```

Create `.env.token`

```env
username=your_username
password=your_password
grant_type=password
```

Create `.env.header`

```env
Content-Type=application/x-www-form-urlencoded
Accept=application/json
```

---

## Running the Application

```bash
python main.py
```

Output files will be generated in:

```text
output/
└── DD-MM-YYYY/
    └── Product_Data_DD-MM-YYYY.xlsx
```

---

## Logging

Application logs are stored in:

```text
logs/application.log
```

---

## Example Workflow

```text
Authentication
      │
      ▼
Retrieve Access Token
      │
      ▼
Fetch Product Pages
      │
      ▼
Process Product Data
      │
      ▼
Export Excel File
      │
      ▼
Store Logs
```

---

## Future Enhancements

### API Layer

* FastAPI Integration
* REST Endpoints
* Swagger Documentation

### Database Support

* MySQL
* PostgreSQL
* MongoDB

### Performance

* Parallel Processing
* Async Requests
* Retry Mechanism

### Deployment

* Docker
* Docker Compose
* Kubernetes
* AWS
* Azure

### DevOps

* GitHub Actions
* CI/CD Pipeline
* Automated Testing

---

## Requirements

* Python 3.11+
* requests
* pandas
* openpyxl
* python-dotenv

Install:

```bash
pip install -r requirements.txt
```

---

## License

MIT License

---

## Author

Manikandan R.

Python Developer | API Integration | FastAPI | Data Engineering | DevOps
