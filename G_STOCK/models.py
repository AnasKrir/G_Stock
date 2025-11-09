from django.db import models

# Create your models here.

catégorie_choix = (
	  ('Fourniture', 'Fourniture'),
	  ('Matériel informatique', 'Matériel informatique'),
	  ('Téléphone', 'Téléphone'),
    )

class Catégorie(models.Model):
    nom = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.nom

class Stock(models.Model):
	catégorie = models.ForeignKey(Catégorie, on_delete=models.CASCADE, blank=True)
	nom = models.CharField(max_length=50, blank=True, null=True)
	quantité = models.IntegerField(default='0', blank=False, null=True)
	recevoir_quantité = models.IntegerField(default='0', blank=True, null=True)
	reçu_par = models.CharField(max_length=50, blank=True, null=True)
	quantité_émis = models.IntegerField(default='0', blank=True, null=True)
	émis_par = models.CharField(max_length=50, blank=True, null=True)
	émis_à = models.CharField(max_length=50, blank=True, null=True)
	Tel_num = models.CharField(max_length=50, blank=True, null=True)
	créé_par = models.CharField(max_length=50, blank=True, null=True)
	niveau_de_réapprovisionnement = models.IntegerField(default='0', blank=True, null=True)
	dernière_mise_à_jour = models.DateTimeField(auto_now_add=False ,auto_now=True)
	#exporter_au_format_CSV = models.BooleanField(default=False)
	date_d_ajout = models.DateTimeField(auto_now_add=True ,auto_now=False)
	#date = models.DateTimeField(auto_now_add=False ,auto_now=False)



	def __str__ (self):
		return self.nom+ ' ' + str(self.quantité)




class StockHistory(models.Model):
	catégorie = models.ForeignKey(Catégorie, on_delete=models.CASCADE, blank=True, null=True)
	nom = models.CharField(max_length=50, blank=True, null=True)
	quantité = models.IntegerField(default='0', blank=True, null=True)
	recevoir_quantité = models.IntegerField(default='0', blank=True, null=True)
	reçu_par = models.CharField(max_length=50, blank=True, null=True)
	quantité_émis = models.IntegerField(default='0', blank=True, null=True)
	émis_par = models.CharField(max_length=50, blank=True, null=True)
	émis_à = models.CharField(max_length=50, blank=True, null=True)
	Tel_num = models.CharField(max_length=50, blank=True, null=True)
	créé_par = models.CharField(max_length=50, blank=True, null=True)
	niveau_de_réapprovisionnement = models.IntegerField(default='0', blank=True, null=True)
	dernière_mise_à_jour = models.DateTimeField(auto_now_add=False ,auto_now=False, null=True)
	date_d_ajout = models.DateTimeField(auto_now_add=False ,auto_now=False, null=True)



