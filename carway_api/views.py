from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import Invoice, AdditionalServices, WashType
from .serializers import InvoiceSerializer, InvoiceCreateSerializer, AdditionalServicesSerializer, WashTypeSerializer
from .permissions import IsSuperuserOrReadOnly


class AdditionalServicesListAPIView(generics.ListCreateAPIView):
    queryset = AdditionalServices.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]
    serializer_class = AdditionalServicesSerializer


class AdditionalServicesDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the invoices
        for the currently authenticated user or a list of all invoices for the admin.
        """
        employee = self.request.user
        if employee and employee.is_superuser:
            return Invoice.objects.all()
        return Invoice.objects.filter(employee=employee)


class InvoiceCreateAPIView(generics.CreateAPIView):
    queryset = AdditionalServices.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceCreateSerializer

    def perform_create(self, serializer):
        serializer.save(employee=self.request.user)


class InvoiceListAPIView(generics.ListAPIView):
    queryset = Invoice.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        """
        This view should return an invoice for the currently authenticated user.
        or the admin.
        """
        employee = self.request.user
        if employee is not None:
            if employee.is_superuser:
                return Invoice.objects.all().order_by('-date', '-time')
            return Invoice.objects.filter(employee=employee).order_by('-date', '-time')
        return None


class InvoiceDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, IsSuperuserOrReadOnly]
    serializer_class = InvoiceSerializer

    def get_queryset(self):
        """
        This view should return an invoice for the currently authenticated user.
        or the admin.
        """
        employee = self.request.user
        if employee is not None:
            if employee.is_superuser:
                return Invoice.objects.all()
            return Invoice.objects.filter(employee=employee)
        return None


class WashTypeListAPIView(generics.ListCreateAPIView):
    queryset = WashType.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]
    serializer_class = WashTypeSerializer


class WashTypeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WashType.objects.all()
    permission_classes = [IsSuperuserOrReadOnly]
    serializer_class = WashTypeSerializer


def index(request):
    return JsonResponse({'info': 'Car way API v1',
                         'developer': 'Mishary Aljarie',
                         'documentations': 'http://****/docs'})
