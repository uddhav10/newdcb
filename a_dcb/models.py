from django.db import models
from uuid import uuid4
import os
from datetime import datetime
# Create your models here.

def path_and_rename(instance, filename):
    upload_to = 'complaint_files'
    original_name = filename.split('.')[0]
    ext = filename.split('.')[-1]
    dateTime = datetime.now()
    dateTimeNow = dateTime.strftime("%d-%m-%Y_%H.%M.%S")
    filename = '{}_{}.{}'.format(original_name, dateTimeNow, ext)
    return os.path.join(upload_to, filename)

COMPLAINT_STATUS = [
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('rejected', 'Rejected'),
]

class Departments(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=100)
    file = models.FileField(upload_to=path_and_rename)
    complaint = models.CharField(max_length=5000)
    complaint_status = models.CharField(
        max_length=50, choices=COMPLAINT_STATUS, default='pending')
    created_by = models.IntegerField(default=1)
    created_at = models.DateField(auto_now_add=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, default='f3f2a8ce-175a-4dbd-bd78-744d01b4a2be')
    
    class Meta:
        ordering = ['-id']