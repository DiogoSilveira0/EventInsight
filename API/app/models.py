from django.db import models

# Create your models here.
class Test(models.Model):
    machine = models.IntegerField()
    value = models.IntegerField()

    def __str__(self):
        return str(self.machine)
