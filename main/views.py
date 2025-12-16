from django.shortcuts import render

from django.views.generic import ListView
from django.db.models import Count
from .models import Category, Product, Service, Country


class HomeView(ListView):
    template_name= 'main/index.html'
    model=Category
    context_object_name='categories'
    
    def get_context_data(self, **kwargs):
        data= super().get_context_data(**kwargs)
        data['recomended'] = Product.objects.filter(recommended=True)
        data['discount'] = Product.objects.filter(discount__gt=0)[:5]
        data['top_categories' ]=Product.objects.order_by('-view')[:3]
        data['services'] =Service.objects.filter(is_active=True)[:4]
        data['countries'] = Country.objects.all()
        data['best_categories'] = Category.objects.annotate(product_count=Count("product_categories_products")).order_by("-product_count")[:2]
        
        return data