from django.urls import path
from . import views

urlpatterns=[
    path("expenses/",views.ExpensesAPIView.as_view(),name="expenses"),
    path("expense/<id>/",views.ExpenseDetailsAPIView.as_view(),name="expense")

]