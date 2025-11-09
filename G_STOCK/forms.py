from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Stock

class StockCreateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['catégorie', 'nom', 'quantité']

    def clean_catégorie(self):
        catégorie = self.cleaned_data.get('catégorie')
        if not catégorie:
            raise forms.ValidationError('Ce champ est obligatoire')
        return catégorie

    def clean_nom(self):
        nom = self.cleaned_data.get('nom')
        if not nom:
            raise forms.ValidationError('Ce champ est obligatoire')
        return nom

    def clean_quantité(self):
        quantité = self.cleaned_data.get('quantité')
        if quantité is None or quantité < 0:
            raise forms.ValidationError('La quantité doit être positive ou nulle')
        return quantité


class StockSearchForm(forms.ModelForm):
    exporter_au_format_CSV = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['catégorie', 'nom']


class StockUpdateForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['catégorie', 'nom', 'quantité']

    def clean_quantité(self):
        quantité = self.cleaned_data.get('quantité')
        if quantité is None or quantité < 0:
            raise forms.ValidationError('La quantité doit être positive ou nulle')
        return quantité


class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['quantité_émis', 'émis_à']

    def clean_quantité_émis(self):
        quantité_émis = self.cleaned_data.get('quantité_émis')
        if quantité_émis is None or quantité_émis < 0:
            raise forms.ValidationError('La quantité émise doit être positive ou nulle')
        
        stock_id = self.instance.id
        stock = Stock.objects.get(id=stock_id)
        if quantité_émis > stock.quantité:
            raise forms.ValidationError('La quantité émise ne doit pas surpasser la quantité en stock')

        return quantité_émis


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['recevoir_quantité']

    def clean_recevoir_quantité(self):
        recevoir_quantité = self.cleaned_data.get('recevoir_quantité')
        if recevoir_quantité is None or recevoir_quantité < 0:
            raise forms.ValidationError('La quantité reçue doit être positive ou nulle')
        return recevoir_quantité


class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['niveau_de_réapprovisionnement']

    def clean_niveau_de_réapprovisionnement(self):
        niveau_de_réapprovisionnement = self.cleaned_data.get('niveau_de_réapprovisionnement')
        if niveau_de_réapprovisionnement is None or niveau_de_réapprovisionnement < 0:
            raise forms.ValidationError('Le niveau de réapprovisionnement doit être positif ou nul')
        return niveau_de_réapprovisionnement
