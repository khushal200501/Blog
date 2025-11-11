from django.db import models

class Contact(models.Model):
    sno=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    content=models.TextField()
    email=models.CharField(max_length=50)
    time=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Message from '+self.name
    
