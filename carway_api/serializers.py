from rest_framework import serializers
from .models import Invoice, AdditionalServices, WashType
from django.contrib.auth.models import User
from Users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    # invoices = serializers.PrimaryKeyRelatedField(
    #    many=True, queryset=User.objects.all())

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name",
                  "email", "is_active", "is_staff"]


class AdditionalServicesSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdditionalServices
        fields = "__all__"


class WashTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WashType
        fields = "__all__"


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name"]


class InvoiceSerializer(serializers.ModelSerializer):
    additional_services = AdditionalServicesSerializer(many=True)
    wash_type = WashTypeSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "date",
            "time",
            "wash_type",
            "additional_services",
            "total",
            "employee"
        ]
        extra_kwargs = {
            "additional_services": {"required": False},
        }


class InvoiceCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = [
            "invoice_number",
            "date",
            "time",
            "wash_type",
            "additional_services",
            "total",
            "employee",
        ]
        read_only_fields = ("employee",)
        extra_kwargs = {
            "additional_services": {"required": False},
        }


class EmptySerializer(serializers.Serializer):
    pass
