from rest_framework import generics, status
from rest_framework.response import Response
from .models import Income
from .serializer import IncomeSerializer
from rest_framework import permissions
from .permissions import IsOwner
from .pagination import IncomePaginator


class IncomesAPIView(generics.ListCreateAPIView):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    pagination_class = IncomePaginator
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class IncomeDetailsAPIView(generics.GenericAPIView):
    serializer_class = IncomeSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def get(self, request, id):
        Income = self.get_object(id)
        if not Income:
            return Response({'errors': 'that Income was not found'},
                            status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request, Income)
        serialized_data = self.serializer_class(Income)
        return Response(serialized_data.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        income = self.get_object(id)
        if income:
            self.check_object_permissions(request, income)
            serializer_data = self.serializer_class(
                income, request.data, partial=True)
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            return Response(
                {'data': serializer_data.data,
                    'message': 'record updated successfully'},
                status=status.HTTP_200_OK)
        return Response({
            'errors': 'that income record was not found'
        }, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        income = self.get_object(id)
        if income:
            self.check_object_permissions(request, Income)
            income.delete()
            return Response({'income': 'income record has been deleted'},
                            status=status.HTTP_200_OK)
        return Response({'errors': 'that record was not found'},
                        status=status.HTTP_404_NOT_FOUND)

    def get_object(self, id):
        return Income.objects.filter(id=id).first()
