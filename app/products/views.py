from rest_framework import viewsets, status,filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render
from .models import Product, Webhook
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer, WebhookSerializer
from .tasks import process_csv_import, bulk_delete_products
from celery.result import AsyncResult



class ProductViewSet(viewsets.ModelViewSet):
    
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'sku']
    search_fields = ['sku', 'name', 'description']


    @action(detail=False, methods=['post'])
    def upload_csv(self, request):
        file = request.FILES.get('file')
        #with open('temp.csv', 'wb+') as :
        if not file:
            return Response(status=400)
        #filer=file.read()
        try:
            file_content = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return Response(status=400)
            
        task = process_csv_import.delay(file_content)
        return Response({'task_id': task.id}, status=202)

    @action(detail=False, methods=['get'])
    def import_status(self, request):
        task_id = request.query_params.get('task_id')
        if not task_id: 
            #return Response
            return Response({'error': 'you missed task id'}, status=400)
            
        result = AsyncResult(task_id)
        
        response_data = {
            'state': result.state,
            'details': result.info,
        }
        
       
        if result.state == 'FAILURE':
            response_data['details'] = str(result.info)
            
        return Response(response_data)
    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        bulk_delete_products.delay()
        return Response({'status': 'Deletion started'}, status=202)

class WebhookViewSet(viewsets.ModelViewSet):
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer

def index(request):
    return render(request, 'index.html')