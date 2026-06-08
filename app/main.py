from pathlib import Path
from datetime import datetime

from app.services.product_service import ProductService
from app.utils.excel_writer import ExcelWriter
from prometheus_client import start_http_server

today = datetime.now().strftime("%d-%m-%Y")

output_folder = Path("output") / today

output_folder.mkdir(
    parents=True,
    exist_ok=True
)

start_http_server(8000)

service = ProductService()
records = service.run()

file_path = (
    output_folder /
    f"Product_Data_{today}.xlsx"
)

service = ProductService()

records = service.run()
print(f"Records Count: {len(records)}")
print(f"Output File: {file_path}")

ExcelWriter.save(
    records,
    file_path
)

print("Completed Successfully")