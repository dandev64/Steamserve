from django.db import models

# retained columns:
# AppID,Name,Release date,Price,DLC count,Header image,Positive,Negative,Achievements,Developers,Publishers,Categories,Genres

# Create your models here.
class Game(models.Model):
    # required
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    release_date = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dlc_count = models.IntegerField()
    header_image = models.CharField(max_length=100)
    positive = models.IntegerField()
    negative = models.IntegerField()
    achievements = models.IntegerField()

    # nullable
    developers = models.TextField(null=True)
    publishers = models.CharField(max_length=255, null=True)
    categories = models.TextField(null=True)
    genres = models.CharField(max_length=255, null=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.app_id) + ": " + self.name + " (" + self.release_date + ")"