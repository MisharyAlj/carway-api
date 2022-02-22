from django.db import models

# Create your models here.


class AdditionalServices(models.Model):
    service = models.CharField(max_length=100, null=False)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    def __str__(self):
        return "%s -- %s SR" % (self.service, self.price)


class WashType(models.Model):
    car_size = models.CharField(max_length=100)
    wash_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    def __str__(self):
        return "%s - %s - %s SR" % (self.car_size, self.wash_type, self.price)


class Invoice(models.Model):
    invoice_number = models.AutoField(primary_key=True)
    date = models.DateField(null=False)
    time = models.TimeField(null=False)
    wash_type = models.ForeignKey(
        WashType, related_name='type', on_delete=models.CASCADE)
    additional_services = models.ManyToManyField(
        AdditionalServices, related_name="Invoices", blank=True)
    total = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    employee = models.ForeignKey(
        'Users.CustomUser', related_name='invoices', on_delete=models.CASCADE)
