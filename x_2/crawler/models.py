from django.db import models

# Create your models here.
class Crawler(models.Model):
    occurencies = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'crawler'