import ast
import os
from typing import List
from datetime import date, timedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MiniRestaurant.settings")

import django
django.setup()

from resto.models import *

commandes:List[Commande] = Commande.objects.all()

for commande in commandes:
	Commande.objects.update(
		a_payer = models.F("payee")
	)