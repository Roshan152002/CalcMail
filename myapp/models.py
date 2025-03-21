from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Arithmatic(models.Model):
    a  = models.IntegerField()
    b  = models.IntegerField()
    operation_type = models.CharField(max_length=10,default='add')
    operation = models.IntegerField(default=None)
    USER = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.operation