from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date

class Personnel(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
	avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('tel', 'user')

	def __str__(self):
		string = self.user.first_name+self.user.last_name
		string = string if string else self.user.username
		return f"{string}"

class Serveur(models.Model):
	firstname = models.CharField(verbose_name='nom', max_length=24)
	lastname = models.CharField(verbose_name='prenom', max_length=24)
	avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('firstname', 'tel')

	def __str__(self):
		return f"{self.firstname} {self.lastname}"

class Table(models.Model):
	number = models.IntegerField()

	def __str__(self):
		return f"Table {self.number}"

class Produit(models.Model):
	nom = models.CharField(max_length=64, unique=True)
	unite = models.CharField(max_length=64, verbose_name='unité de mesure')
	unite_sortant = models.CharField(max_length=64, null=True,blank=True)
	rapport = models.FloatField(default=1)
	quantite = models.FloatField(default=0, editable=False)

	def __str__(self):
		return self.nom

	class Meta:
		ordering = ["nom"]

class Achat(models.Model):
	produit = models.ForeignKey("Produit", on_delete=models.CASCADE)
	quantite = models.FloatField()
	prix = models.FloatField()
	date = models.DateTimeField(blank=True, default=timezone.now)
	motif = models.CharField(max_length=64, blank=True, null=True)
	personnel = models.ForeignKey("Personnel", on_delete=models.PROTECT)

	def save(self, *args, **kwargs):
		super(Achat, self).save(*args, **kwargs)
		produit = self.produit
		produit.quantite += self.quantite
		produit.save() 

	def __str__(self):
		return f"{self.date}:{self.produit} {self.quantite} {self.produit.unite}"

	class Meta:
		ordering = ["produit"]

class PrixRecette(models.Model):
	recette = models.ForeignKey("Recette", null=True, on_delete=models.SET_NULL)
	prix = models.PositiveIntegerField()
	date = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		return f"{self.recette.nom} à {self.prix}"
		
class Recette(models.Model):
	nom = models.CharField(max_length=64)
	image = models.ImageField(upload_to="recettes/")
	disponible = models.BooleanField(default=True)
	details = models.URLField(null=True, blank=True)
	prix = models.FloatField()
	produit = models.ForeignKey("Produit", null=True, blank=True, on_delete=models.SET_NULL)

	def __str__(self):
		return f"{self.nom}"

	def save(self, *args, **kwargs):
		super(Recette, self).save(*args, **kwargs)
		prix = PrixRecette.objects.filter(recette=self)
		if(prix and prix.last().prix != self.prix):
			PrixRecette(recette=self, prix=self.prix).save()

class DetailCommande(models.Model):
	commande = models.ForeignKey("Commande", null=True, on_delete=models.CASCADE,related_name='details')
	recette = models.ForeignKey("Recette", null=True, on_delete=models.SET_NULL)
	quantite = models.PositiveIntegerField(default=1)
	somme = models.PositiveIntegerField(editable=False, blank=True, verbose_name='à payer')
	date = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		self.somme = self.recette.prix * self.quantite
		super(DetailCommande, self).save(*args, **kwargs)
		produit = self.recette.produit
		if produit:
			produit.quantite -= self.quantite
			produit.save()

	class Meta:
		unique_together = ('commande','recette')
		ordering = ['date']
			
	def __str__(self):
		return f"{self.recette}"

class Client(models.Model):
	nom = models.CharField(verbose_name='nom', max_length=64)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('nom', 'tel')

	def __str__(self):
		return f"{self.nom} {self.tel}"

class Commande(models.Model):
	table = models.ForeignKey(Table, default=1, on_delete=models.SET_DEFAULT)
	date = models.DateTimeField(blank=True, default=timezone.now)
	# a_payer = models.FloatField(default=0, blank=True)
	payee = models.FloatField(default=0, blank=True)
	reste = models.FloatField(editable=False, default=0, blank=True)
	serveur = models.ForeignKey("Serveur", null=True, on_delete=models.SET_NULL)
	personnel = models.ForeignKey("Personnel", null=True, on_delete=models.SET_NULL)
	client = models.ForeignKey("Client", null=True, on_delete=models.SET_NULL)

	class Meta:
		ordering = ("-id", )

	def save(self, *args, **kwargs):
		self.reste = self.a_payer()-self.payee
		super(Commande, self).save(*args, **kwargs)

	def paniers(self):
		return DetailCommande.objects.filter(commande=self)

	def a_payer(self):
		try:
			return float(self.paniers().aggregate(Sum('somme'))["somme__sum"])
		except Exception as e:
			return 0

class Paiement(models.Model):
	commande = models.ForeignKey("Commande", null=True, on_delete=models.SET_NULL)
	somme = models.PositiveIntegerField(verbose_name='somme payée', default=0)
	date = models.DateField(blank=True, default=timezone.now)

	def save(self, *args, **kwargs):
		commande = self.commande
		super(Paiement, self).save(*args, **kwargs)
		commande.payee += self.somme
		commande.reste = commande.a_payer()-self.somme
		commande.save()