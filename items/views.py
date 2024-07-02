from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, FormView, DetailView, TemplateView
from .models import Category, Option, Item

# from .forms import SearchForm


# self.kwargs.get('urls.py')
# self.request.GET.get('query parameter')


class HomeView(TemplateView):
    template_name = 'index.html'


# class AllItemsView(ListView):
#     template_name = 'items/all_items.html'
#     model = Item
#     context_object_name = 'items'
#
#     def get_queryset(self):
#         return Item.objects.all().order_by('-created_at')


# class ItemCategoryView(ListView):
#     template_name = 'items/all_items.html'
#     model = Item
#     context_object_name = 'items'
#
#     def get_queryset(self):
#         key = self.kwargs.get('key')
#         return Item.objects.filter(Q(category__key=key) | Q(type__key=key))


class AllItemsView(ListView):
    template_name = 'items/all_items.html'
    model = Item
    context_object_name = 'items'

    def get_queryset(self):
        items = Item.objects.all()

        if code := self.request.GET.get('code'):
            items = items.filter(code__exact=code)

        elif address := self.request.GET.get('address'):
            items = items.filter(address__contains=address)

        elif min_price := self.request.GET.get('min_price'):
            items = items.filter(total_price__gte=min_price)

        elif max_price := self.request.GET.get('max_price'):
            items = items.filter(total_price__lte=max_price)

        elif category := self.request.GET.getlist('category'):
            items = items.filter(category__key__in=category)

        elif i_type := self.request.GET.getlist('type'):
            items = items.filter(type__key__in=i_type)

        elif min_area := self.request.GET.get('min_area'):
            items = items.filter(min_area__gte=min_area)

        elif max_area := self.request.GET.get('max_area'):
            items = items.filter(max_area__lte=max_area)

        elif order := self.request.GET.get('order_by'):
            items = items.order_by(order)

        return items.order_by('-created')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['min_price'] = self.request.GET.get('min_price')
        context['max_price'] = self.request.GET.get('max_price')
        context['min_area'] = self.request.GET.get('min_area')
        context['max_area'] = self.request.GET.get('max_area')
        context['filtered_categories'] = self.request.GET.getlist('category')
        context['filtered_types'] = self.request.GET.getlist('type')

        return context


class ItemDetailView(DetailView):
    template_name = 'items/item_detail.html'
    model = Item
    context_object_name = 'item'

    def get_object(self, queryset=None):
        return get_object_or_404(Item, code__exact=self.kwargs.get('code'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['related_items'] = Item.objects.filter(category__key=self.get_object().category.key)[:6]

        return context
