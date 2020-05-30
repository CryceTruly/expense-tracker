from django.urls import path
from . import views

urlpatterns = [
    path("", views.IncomesAPIView.as_view(), name="incomes"),
    path("<int:id>", views.IncomeDetailsAPIView.as_view(),
         name="income")

]
