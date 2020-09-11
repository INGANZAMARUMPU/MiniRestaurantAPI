from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date

class Personnel(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class DetailStock(models.Model):
	stock = models.ForeignKey('Stock', on_delete=models.CASCADE)
	quantite = models.FloatField()
	date = models.DateTimeField(blank=True, default=timezone.now)
	motif = models.CharField(max_length=64, blank=True, null=True)

	def save(self, *args, **kwargs):
		stock = self.stock
		stock.quantite_actuelle -= abs(self.quantite)
		stock.save() 
		super(DetailStock, self).save(*args, **kwargs)

	def __str__(self):
		return f"{self.stock.produit} du {self.stock.date} -\
			{self.quantite} {self.stock.produit.unite}"

class Stock(models.Model):
	produit = models.ForeignKey("Produit", on_delete=models.CASCADE)
	offre = models.ForeignKey("Offre", null=True, on_delete=models.SET_NULL)
	quantite_initiale = models.FloatField(verbose_name='quantité initial')
	quantite_actuelle = models.FloatField(editable=False, verbose_name='quantité actuelle')
	date = models.DateField(blank=True, default=timezone.now)
	expiration = models.PositiveIntegerField(default=7, null=True, blank=True, verbose_name="délais de validité(en jours)")
	expiration_date = models.DateField(editable=False, null=True)
	personnel = models.ForeignKey("Personnel", null=True, on_delete=models.SET_NULL)
	# is_valid = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.produit} {self.quantite_actuelle} {self.produit.unite} du {self.date}"

	def save(self, *args, **kwargs):
		if self.quantite_actuelle == None:
			self.quantite_actuelle = self.quantite_initiale
		if self.expiration:
			self.expiration_date=self.date+timedelta(days=self.expiration)
		super(Stock, self).save(*args, **kwargs)
		self.calculateProxy()

	def calculateProxy(self):
		somme = Stock.objects.filter(produit=self.produit, \
				quantite_actuelle__gt=0)\
			.aggregate(somme=Sum('quantite_actuelle'))
		self.produit.quantite = somme['somme']
		self.produit.save()

	def somme(self):
		return self.quantite_initiale*self.offre.prix

	class Meta:
		ordering = ["produit"]

class Offre(models.Model):
	produit = models.ForeignKey("Produit", null=True, on_delete=models.SET_NULL)
	fournisseur = models.ForeignKey("Fournisseur", null=True, on_delete=models.SET_NULL)
	prix = models.FloatField()

	def __str__(self):
		try:
			return f"{self.fournisseur} - {self.prix} - {self.produit.nom}"
		except:
			return ""

	class Meta:
		unique_together = ('produit', 'fournisseur', 'prix')

class Fournisseur(models.Model):
	nom = models.CharField(verbose_name='nom et prenom', max_length=64)
	adresse = models.CharField(max_length=64)
	tel = models.CharField(verbose_name='numero de télephone', max_length=24)

	class Meta:
		unique_together = ('adresse', 'tel')
	def __str__(self):
		return f"{self.nom}"

class Recette(models.Model):
	nom = models.CharField(max_length=64)
	image = models.ImageField(upload_to="recettes/")
	disponible = models.BooleanField(default=True)
	details = models.URLField(null=True, blank=True)

	def __str__(self):
		return f"{self.nom}"

	def prix(self):
		try:
			return PrixRecette.objects.filter(recette=self).last().prix
		except:
			return 0

class PrixRecette(models.Model):
	recette = models.ForeignKey("Recette", null=True, on_delete=models.SET_NULL)
	prix = models.PositiveIntegerField()
	date = models.DateTimeField(default=timezone.now)
	
	def __str__(self):
		return f"{self.recette.nom} à {self.prix}"

class DetailCommande(models.Model):
	commande = models.ForeignKey("Commande", null=True, on_delete=models.CASCADE, related_name='details')
	recette = models.ForeignKey("Recette", null=True, on_delete=models.SET_NULL)
	quantite = models.PositiveIntegerField(default=1)
	somme = models.PositiveIntegerField(editable=False, blank=True, verbose_name='à payer')
	date = models.DateTimeField(default=timezone.now)

	def save(self, *args, **kwargs):
		self.somme = self.recette.prix()*self.quantite
		super(DetailCommande, self).save(*args, **kwargs)
		self.updateCommande()

	class Meta:
		unique_together = ('commande','recette')
		ordering = ['date']
			
	def __str__(self):
		return f"{self.recette}"

	def updateCommande(self):
		commande = self.commande
		commande.a_payer += self.somme
		commande.save()

class Commande(models.Model):
	table = models.ForeignKey(Table, default=1, on_delete=models.SET_DEFAULT)
	tel = models.CharField(verbose_name='numero de télephone', blank=True, default=0, max_length=24)
	date = models.DateField(blank=True, default=timezone.now)
	a_payer = models.FloatField(default=0, blank=True)
	payee = models.FloatField(default=0, blank=True)
	reste = models.FloatField(default=0, blank=True)
	serveur = models.ForeignKey(Serveur, blank=True, null=True, on_delete=models.SET_NULL)

	def save(self, *args, **kwargs):
		self.reste = self.a_payer-self.payee
		super(Commande, self).save(*args, **kwargs)

	class Meta:
		ordering = ("-id", )

	def paniers(self):
		return Panier.objects.filter(commande=self)

class Paiement(models.Model):
	commande = models.ForeignKey("Commande", null=True, on_delete=models.SET_NULL)
	somme = models.PositiveIntegerField(verbose_name='somme payée', default=0)
	date = models.DateField(blank=True, default=timezone.now)

	def save(self, *args, **kwargs):
		commande = self.commande
		super(Paiement, self).save(*args, **kwargs)
		# paiements = Paiement.objects.filter(commande=commande).aggregate(Sum("somme"))["somme__sum"]
		# commande.payee = paiements
		commande.payee += self.somme
		commande.reste = commande.a_payer-paiements
		commande.save()