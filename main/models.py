from django.db import models

class Client(models.Model):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=20, blank=True, null=True)
    country = models.CharField( max_length=200, null=True, blank=True)
    region = models.CharField( max_length=200, null=True, blank=True)
    genders = (("MALE", "MALE"), ("FEMALE", "FEMALE"),)
    gender = models.CharField(max_length=10, choices=genders ,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    ids = (("National ID", "National ID"),("Passport", "Passport"),("VOTERS ID", "VOTERS ID"),("DRIVING LICENCE", "DRIVING LICENCE"),)
    identification = models.CharField(choices=ids, max_length=200, default="Null")
    identification_number = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, null=True)
    edited_at = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Loan(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    loan_amount = models.IntegerField(default="")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    payment_schedule = models.CharField(max_length=255)
    statuses  = (("Processing", "Processing"), ("Active", "Active"),("Complited", "Complited"))

    status = models.CharField(max_length=255, choices=statuses)
    created_at = models.DateTimeField(auto_now=True, null=True)
    edited_at = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __str__(self):
        return self.client.first_name + str(self.loan_amount)
    
    
class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateField()
    amount = models.IntegerField(default='')
    created_at = models.DateTimeField(auto_now=True, null=True)
    edited_at = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __str__(self):
        return self.loan.client.first_name + str(self.amount)
    