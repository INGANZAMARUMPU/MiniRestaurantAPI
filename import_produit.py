import ast
import os
from typing import List
from datetime import date, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MiniRestaurant.settings")

import django
django.setup()

from resto.models import *

recettes:List[Recette] = []
with open("miami.csv", "r") as file:
	for line in file.readlines():
		line = line[:-1].split(";")
		print(line)
		if(line[2]):
			produit = Produit(
				nom = line[0],
				unite = "bouteilles",
				unite_sortant = "bouteilles",
				rapport = 1,
				quantite = line[2]
			)
			produit.save()
			recette = Recette(
				nom = line[0],
				prix = line[1],
				is_active = True,
				produit = produit
			)
			recette.save()
		else :
			recette = Recette(
				nom = line[0],
				prix = line[1],
				is_active = True
			)
			recette.save()