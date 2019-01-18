from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory_count = models.IntegerField()

    def isAvailable(self):
        return self.inventory_count > 0

    def purchase(self):
        if self.isAvailable():
            self.inventory_count -= 1
            return True
        else:
            return False

    def __str__(self):
        return self.title
