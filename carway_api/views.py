from datetime import datetime
from django.http import JsonResponse
from rest_framework import generics, permissions, status
from .models import Invoice, AdditionalServices, WashType
from .serializers import EmptySerializer, InvoiceSerializer, InvoiceCreateSerializer, AdditionalServicesSerializer, WashTypeSerializer
from .permissions import IsSuperuserOrReadOnly
from Users.models import CustomUser
from rest_framework.response import Response
from django.db.models import Avg, Sum, Count
from django.db.models.functions import TruncMonth, TruncDay, ExtractYear


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


# A viewset that returns the analytics of the system.
class AnalyticsViewSet(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser, ]
    queryset = CustomUser.objects.all()
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        # Number of activ users
        active_users = CustomUser.objects.filter(
            is_active='True').count()

        # Number of employees
        employees = CustomUser.objects.filter(
            is_staff='True').count()

        # Getting the number of invoices and the total of the invoices for today.
        todays_sales = Invoice.objects.filter(
            date=datetime.now().date()).aggregate(num_of_invoices=Count('invoice_number'), total=Sum('total'))

        # List (number of invoices, total, total avg, max/min invoice total) of all invoices
        all_sales = Invoice.objects.aggregate(
            num_of_invoices=Count('invoice_number'),
            income=Sum("total"),
            income_avg=Avg('total'))

        # Getting the number of invoices and the total of the invoices for each day.
        sales_by_day = Invoice.objects.annotate(
            day=TruncDay('date')).values('day').annotate(
                num_of_invoices=Count('invoice_number'),
                income_total=Sum('total')).order_by('date')

        # Getting the number of invoices and the total of the invoices for each month.
        sales_by_month = Invoice.objects.annotate(
            month=TruncMonth('date')).values('month').annotate(
                num_of_invoices=Count('invoice_number'),
                income_total=Sum('total'))

        # Getting the number of invoices and the total of the invoices for each year.
        sales_by_year = Invoice.objects.annotate(
            year=ExtractYear('date')).values('year').annotate(
                num_of_invoices=Count('invoice_number'),
                income_total=Sum('total'))

        return Response({
            'active_users': active_users,
            'employees': employees,
            'todays_sales': todays_sales,
            'all_sales': all_sales,
            'sales_by_day': sales_by_day,
            'sales_by_month': sales_by_month,
            'sales_by_year': sales_by_year,
        }, status=status.HTTP_200_OK)


def index(request):
    return JsonResponse({'info': 'Car way API v2',
                         'developer': 'Mishary Aljarie',
                         'documentations': 'https://carway-api.herokuapp.com/docs/'})
