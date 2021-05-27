from django.urls import path
from .views import home_view, SalesListView, SalesDetailView

app_name = 'sales'

urlpatterns=[
	path('sales/<pk>/', SalesDetailView.as_view(), name='detail'),
	path('sales-list/', SalesListView.as_view(), name='list'),
	path('', home_view, name='home')

]