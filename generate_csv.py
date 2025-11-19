import csv
import random
import string

filename = "large_product.csv"
records = 500 

print(f"Generating {records} records. This may take a few seconds...")

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
   
    writer.writerow(['sku', 'name', 'description', 'active'])
    
    for i in range(records):
       
        sku = f"SKU-{i:06d}"
        name = f"Product {random_string(5)}"
        description = f"Description for product {sku} - {random_string(20)}"
        
        active = random.choice(['true', 'false', '1', '0'])
        
        writer.writerow([sku, name, description, active])
        
        if i % 50000 == 0:
            print(f"Generated {i} rows...")

print(f"Done! File saved as {filename}")