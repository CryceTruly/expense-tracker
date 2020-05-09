from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Expenses API",
        default_version='v1',
        description="API for all things expenditure",
        terms_of_service="",
        contact=openapi.Contact(email="info.truly@makethatapp.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('exp/adm/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('api/expenses/', include(('expense_tracker.apps.expenses.urls',
                                   'expenses'), namespace='expenses')),
    path('api/income/', include(('expense_tracker.apps.income.urls',
                                 'income'), namespace='income')),
    path('api/auth/', include(('expense_tracker.apps.authentication.urls',
                               'authentication'), namespace='authentication'))
]
