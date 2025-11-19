import csv
import io
import requests
from celery import shared_task
from .models import Product, Webhook

@shared_task(bind=True)
def process_csv_import(self, filecontent):
    
    file = io.StringIO(filecontent)
    values = csv.DictReader(file)
    
    rows = list(values)
    totalrows = len(rows)
    bath_size = 1000
    
   
    def chunked(iterable, n):
        for i in range(0, len(iterable), n):
            yield iterable[i:i + n]

    processcount = 0
    """[
        {"sku": "abc123", "name": "Shir,...}
        ]
    """
    for batch in chunked(rows, bath_size):
        products_to_create = []
        products_to_update = []
        
        skus=[]
        #extracting skus in lowrcase
        for row in batch:
            if row.get('sku'):
                row['sku'] = row['sku'].lower()
                skus.append(row['sku'])
        #loading already existing product tht match sku in bulk
        existing_products = Product.objects.filter(sku__in=skus).in_bulk(field_name='sku')

        for row in batch:
            sku = row.get('sku', '').lower()
            if not sku: 
                continue
            #cleaning data so as if field is missing for model ths can be used  
            data = {
                'name': row.get('name', ''),
                'description': row.get('description', ''),
                'is_active': str(row.get('active', 'true')).lower() in ['true', '1', 'yes']
            }

            if sku in existing_products:
                prod = existing_products[sku]
                prod.name = data['name']
                prod.description = data['description']
                prod.is_active = data['is_active']
                products_to_update.append(prod)
            else:
                products_to_create.append(Product(sku=sku, **data))

        if products_to_create:
            Product.objects.bulk_create(products_to_create)
        
        if products_to_update:
            Product.objects.bulk_update(products_to_update, ['name', 'description', 'is_active'])

        processcount += len(batch)
        
       
        self.update_state(
            state='PROGRESS',
            meta={'current': processcount, 'total': totalrows}
        )

    trigger_webhooks.delay(event='import_complete')
    return {'status': 'Complete', 'processed': processcount}

@shared_task
def trigger_webhooks(event):
    hooks = Webhook.objects.filter(is_active=True)
    for hook in hooks:
        try:
            requests.post(hook.url, json={'event': event}, timeout=5)
        except Exception:
            pass 

@shared_task
def bulk_delete_products():
    Product.objects.all().delete()
    return "All products deleted"