from django.views.generic import ListView
from .models import Product

class HomeView(ListView):
    model = Product
    template_name = "main/index.html"
    context_object_name = "products"
