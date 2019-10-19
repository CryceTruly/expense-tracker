from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('exp/adm/', admin.site.urls),
    path('api-auth/',include('rest_framework.urls')),
    path('api/',include(('expense_tracker.apps.expenses.urls','expenses'),namespace='expenses'))
]
