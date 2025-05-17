import os
import django
import csv

# to make configuration error go away
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'steamserve.settings')
django.setup()

from serve.models import Game

#f = os.getcwd()
#print("current directory: \n" + f)

# script to import rows in the csv, adapted from this:
# https://python.plainenglish.io/importing-csv-data-into-django-models-c92a303623fe
def importGames(importpath):
    with open(importpath, 'r') as file:
        gamedict = csv.DictReader(file)
        for row in gamedict:
            Game.objects.create(
                app_id = row['AppID'],
                name = row['Name'],
                release_date = row['Release date'],
                price = row['Price'],
                dlc_count = row['DLC count'],
                header_image = row['Header image'],
                positive = row['Positive'],
                negative = row['Negative'],
                achievements = row['Achievements'],
                developers = row['Developers'],
                publishers = row['Publishers'],
                categories = row['Categories'],
                genres = row['Genres']
            )

csvimport = "serve/steam.csv"
importGames(csvimport)