from django.db import models

# Create your models here.

class Csv(models.Model):
    id = models.AutoField(primary_key=True) 
    file_name = models.FileField(upload_to='upload')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"File: {self.file_name}"
