from django.db import models

from django.contrib.auth.models import AbstractUser


class StatusChoices(models.TextChoices):
    SELLER='seller','Seller'
    CUSTOMER='customer','Customer'
    ADMIN='admin','Admin'
    
    
class User(AbstractUser):
    phone=models.CharField(max_length=50)
    address=models.TextField()
    image= models.FileField(upload_to='users/image')
    status=models.CharField(max_length=50, choices=StatusChoices.choices, default=StatusChoices.CUSTOMER)
    

    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        
        if self.status == StatusChoices.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save( *args, **kwargs)
 
 
 
    
