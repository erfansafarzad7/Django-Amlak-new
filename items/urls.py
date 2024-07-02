from django.urls import path
from . import views


app_name = 'items'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('all-items/', views.AllItemsView.as_view(), name='all'),
    # path('category/<str:key>/', views.ItemCategoryView.as_view(), name='category'),
    # path('filter/', views.ItemFilterView.as_view(), name='filter'),
    path('item-detail/<str:code>/', views.ItemDetailView.as_view(), name='detail'),

]
