## Docker Setup

### Build Docker Image

```bash
docker build -t producthub:1.0 .
```

Verify the image:

```bash
docker images
```

---

### Run Container

```bash
docker run --rm \
--env-file .env \
--env-file .env.header \
--env-file .env.token \
-v $(pwd)/output:/app/output \
-v $(pwd)/logs:/app/logs \
producthub:1.0
```

---

### Expected Output

```text
Records Count: 4900
Output File: /app/output/06-06-2026/Product_Data_06-06-2026.xlsx
Completed Successfully
```

---

### Verify Generated File

Linux / macOS

```bash
find output -name "*.xlsx"
```

Example:

```text
output/06-06-2026/Product_Data_06-06-2026.xlsx
```

Windows PowerShell

```powershell
Get-ChildItem -Path .\output -Recurse *.xlsx
```

---

### View Logs

```bash
cat logs/application.log
```

---

### Docker Compose

Build and Run

```bash
docker compose up --build
```

Run in Background

```bash
docker compose up -d
```

View Logs

```bash
docker compose logs -f
```

Stop Containers

```bash
docker compose down
```

---

### Docker Volumes

The following volume mappings are used:

| Host Machine | Container   |
| ------------ | ----------- |
| ./output     | /app/output |
| ./logs       | /app/logs   |

Generated Excel files will be available in:

```text
output/
└── DD-MM-YYYY/
    └── Product_Data_DD-MM-YYYY.xlsx
```

---

### Troubleshooting

#### Output Folder Empty

Ensure the output volume is mounted correctly:

```bash
-v $(pwd)/output:/app/output
```

Incorrect:

```bash
-v $(pwd)/output:/app/output01
```

If the container writes to a path that is not mounted, the generated file will be removed when the container exits.

---

#### Environment Variables Not Loaded

Verify environment files exist:

```text
.env
.env.header
.env.token
```

Run:

```bash
docker run --rm \
--env-file .env \
--env-file .env.header \
--env-file .env.token \
producthub:1.0 env
```

---

#### Rebuild After Code Changes

```bash
docker build --no-cache -t producthub:1.0 .
```

---

### Remove Docker Resources

Remove Container

```bash
docker ps -a
docker rm <container_id>
```

Remove Image

```bash
docker rmi producthub:1.0
```

Remove Unused Resources

```bash
docker system prune -a
```
