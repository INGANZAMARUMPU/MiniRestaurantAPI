from django.db import models, transaction
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date

class Serveur(models.Model):
	id = models.AutoField(primary_key=True)
	firstname = models.CharField(verbose_name='nom', max_length=24)
	lastname = models.CharField(verbose_name='prenom', max_length=24)
	avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
	tel = models.CharField(max_length=24)
	is_active = models.BooleanField(default=True)

	class Meta:
		unique_together = ('firstname', 'tel')

	def __str__(self):
		return f"{self.firstname} {self.lastname}"

class Table(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=32, default="Table")
	number = models.IntegerField()

	def __str__(self):
		return f"{self.nom} {self.number}"

	class Meta:
		unique_together = "nom", "number"

class Produit(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=64, unique=True)
	unite = models.CharField(max_length=64, verbose_name='unité de mesure')
	unite_sortant = models.CharField(max_length=64, null=True,blank=True)
	rapport = models.FloatField(default=1)
	quantite = models.PositiveIntegerField(default=0, editable=False)

	def __str__(self):
		return self.nom

	class Meta:
		ordering = ["nom"]

class Achat(models.Model):
	id = models.AutoField(primary_key=True)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	quantite = models.FloatField()
	prix = models.FloatField()
	date = models.DateTimeField(blank=True, default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	def __str__(self):
		return f"{self.quantite} {self.produit.unite} de {self.produit} du {self.date}"

	class Meta:
		ordering = ["produit"]

class Sortie(models.Model):
	id = models.AutoField(primary_key=True)
	produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
	quantite = models.FloatField()
	date = models.DateTimeField(blank=True, default=timezone.now)
	motif = models.CharField(max_length=64)
	user = models.ForeignKey(User, on_delete=models.PROTECT)

	def __str__(self):
		return f"{self.quantite} {self.produit.unite} de {self.produit} le {self.date}"

	class Meta:
		ordering = ["produit"]
		
class Recette(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=64)
	image = models.ImageField(upload_to="recettes/", null=True, blank=True)
	disponible = models.BooleanField(default=True)
	details = models.URLField(null=True, blank=True)
	prix = models.FloatField()
	produit = models.ForeignKey(Produit, null=True, blank=True, on_delete=models.SET_NULL)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.nom}"

class Client(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(verbose_name='nom', max_length=64)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('nom', 'tel')

	def __str__(self):
		return f"{self.nom} {self.tel}"

class Commande(models.Model):
	id = models.BigAutoField(primary_key=True)
	table = models.ForeignKey(Table, null=True, on_delete=models.SET_NULL)
	date = models.DateTimeField(blank=True, default=timezone.now)
	a_payer = models.PositiveIntegerField(default=0, blank=True)
	payee = models.PositiveIntegerField(default=0, blank=True)
	serveur = models.ForeignKey(Serveur, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)

	class Meta:
		ordering = ("-id", )

	def paniers(self):
		return DetailCommande.objects.filter(commande=self)

class DetailCommande(models.Model):
	id = models.BigAutoField(primary_key=True)
	commande = models.ForeignKey(Commande, null=True, on_delete=models.CASCADE,related_name='details')
	recette = models.ForeignKey(Recette, null=False, on_delete=models.PROTECT)
	quantite = models.PositiveIntegerField(default=1)
	somme = models.PositiveIntegerField(editable=False, blank=True, verbose_name='à payer')
	date = models.DateTimeField(default=timezone.now)

	class Meta:
		unique_together = ('commande','recette')
		ordering = ['date']
			
	def __str__(self):
		return f"{self.recette}"

class Paiement(models.Model):
	id = models.BigAutoField(primary_key=True)
	commande = models.ForeignKey(Commande, null=True, on_delete=models.SET_NULL)
	somme = models.PositiveIntegerField(verbose_name='somme payée', default=0)
	date = models.DateField(blank=True, default=timezone.now)