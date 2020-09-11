from .models import *
from django import forms

MOTIF_CHOICES = ( 
    ("vers_cuisine", "vers cuisine"), 
    ("vers_caisse", "vers caisse"), 
    ("perime", "perimé"),
)

class ConnexionForm(forms.Form):
	username = forms.CharField(
		widget=forms.TextInput(
			attrs={'placeholder':'Username ', 'class':'input'}),
		# label=""
	)
	password = forms.CharField(
		widget=forms.PasswordInput(
			attrs={'placeholder':'Password ', 'class':'input', 'type':'password'}
		),
		# label=""
	)

class InStockForm(forms.ModelForm):
	offre = forms.ModelChoiceField(
		widget = forms.Select(
			attrs={'placeholder':'offre','class':'input'}),
		queryset=None)
	quantite_initiale = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'quantite','class':'input'}))
	expiration = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'délais de validité(en jours)',
					'class':'input'}),
		required=False);
	class Meta:
		model = Stock
		fields = ("offre", "quantite_initiale", "expiration")

	def __init__(self, produit_id, *args, **kwargs):
		self.base_fields["offre"].queryset = Offre.objects.filter(produit=produit_id)
		super(InStockForm, self).__init__(*args, **kwargs)

class OffreForm(forms.ModelForm):
	fournisseur = forms.ModelChoiceField(
		widget = forms.Select(
			attrs={'placeholder':'offre','class':'input'}),
		queryset=Fournisseur.objects.all())
	prix = forms.IntegerField(widget=forms.NumberInput(
			attrs={'placeholder':'prix','class':'input'}
		)
	);
	class Meta:
		model = Offre
		fields = ("fournisseur", "prix")

class PayForm(forms.ModelForm):
	payee = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'la somme payée','class':'input', 'id':"saisies"}),
		label='la somme payée'
		)
	class Meta:
		model = Commande
		fields = ("payee",)

class OutStockForm(forms.ModelForm):
	stock = forms.ModelChoiceField(
		widget = forms.Select(
			attrs={'placeholder':'stock','class':'input'}),
		queryset=None)
	quantite = forms.IntegerField(
		widget=forms.NumberInput(
			attrs={'placeholder':'quantite','class':'input'}))

	motif = forms.ChoiceField(
		widget=forms.Select(
			attrs={'placeholder':'motif ', 'class':'input'}),
		# label="motif"
		choices=MOTIF_CHOICES
	)

	def __init__(self, produit_id, *args, **kwargs):
		self.base_fields["stock"].queryset = Stock.objects.filter(\
			produit=produit_id, quantite_actuelle__gt=0)
		super(OutStockForm, self).__init__(*args, **kwargs)

	class Meta:
		model = DetailStock
		fields = ("stock", "quantite", "motif")

	def clean_quantite(self, *args, **kwargs):
		stock = self.cleaned_data.get("stock")
		quantite = self.cleaned_data.get("quantite")
		if quantite > stock.quantite_actuelle:
			raise forms.ValidationError("quantité demandée est énorme")
		return quantite

class Register2Form(forms.Form):
	cni_recto = forms.ImageField( widget=forms.FileInput(attrs={'placeholder':'CNI Picture 1','class':'form-control'}), label='CNI Picture 1')
	cni_verso = forms.ImageField( widget=forms.FileInput(attrs={'placeholder':'CNI Picture 2','class':'form-control'}), label='CNI Picture 2')

class DateForm(forms.Form):
	sdate = forms.DateField(
		widget=forms.SelectDateWidget(
			years=range(2020, date.today().year),
			attrs={'placeholder':'date delivrated ', 'class':'search-input',
			'style':'display:inline-block; width:auto'}),
		initial=datetime.now(),
		label='Du')

	edate = forms.DateField(
		widget=forms.SelectDateWidget(
			years=range(2020, date.today().year),
			attrs={'placeholder':'yyyy-mm-dd ', 'class':'search-input',
				'style':'width: auto;display: inline-block;'}),
		initial=datetime.now(),
		label='Au')