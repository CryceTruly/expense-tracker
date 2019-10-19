from rest_framework import generics,status
from rest_framework.response import Response
from .models import Expense
from .serializer import ExpenseSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from .permissions import IsOwner

class ExpensesAPIView(generics.ListCreateAPIView):
    queryset=Expense.objects.all()
    serializer_class=ExpenseSerializer
    permission_classes=(permissions.IsAuthenticated,)

    def perform_create(self,serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)



class ExpenseDetailsAPIView(generics.GenericAPIView):
    serializer_class=ExpenseSerializer
    permission_classes=(permissions.IsAuthenticated,IsOwner)

    def get(self,request,id):
        expense = self.get_object(id)
        if not expense:
            return Response({'errors': 'that expense was not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,expense)
        serialized_data = self.serializer_class(expense)
        return Response(serialized_data.data, status=status.HTTP_200_OK)
    def patch(self, request, id):
        expense = self.get_object(id)
        if expense:
            self.check_object_permissions(request,expense)
            serializer_data = self.serializer_class(expense, request.data, partial=True)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response({'data':serializer_data.data,'message':'Expense updated successfully'},
                            status=status.HTTP_200_OK)
        return Response({
            'errors': 'that expense was not found'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        expense = self.get_object(id)
        if expense:
            self.check_object_permissions(request,expense)
            expense.delete()
            return Response({'expense': 'expense has been deleted'}, status=status.HTTP_200_OK)
        return Response({'errors': 'that expense was not found'}, status=status.HTTP_404_NOT_FOUND)
    def get_object(self, id):
        return Expense.objects.filter(id=id).first()
