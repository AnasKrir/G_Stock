from django.shortcuts import render, redirect

from django.http import HttpResponse

import csv

from django.contrib import messages

from .models import *

from .forms import *

from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
	title = 'Welcome This is the Home Page'
	context = { 
	"title":title,
	}
	return render(request, "home.html",context)

@login_required
def list_items(request):
	header = 'LISTE DE PRODUITS'
	form = StockSearchForm(request.POST or None)
	queryset = Stock.objects.all()
	context = { 
	"header":header,
	"queryset":queryset, 
	"form":form,
	}
	if request.method == 'POST':
		catégorie = form['catégorie'].value()
		queryset = Stock.objects.filter(#catégorie = form['catégorie'].value(),
			                            nom__icontains=form['nom'].value()
			                            )
		if (catégorie != ''):
			queryset = queryset.filter(catégorie_id=catégorie)
			
		if form['exporter_au_format_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Liste de stocks.csv"'
			writer = csv.writer(response)
			writer.writerow(['Catégorie', 'Nom', 'Quantité'])
			i = queryset
			for stock in i:
				writer.writerow([stock.catégorie, stock.nom, stock.quantité])
			return response

		context= { 
		"form":form, 
		"header":header, 
		"queryset":queryset,
	}
	return render(request, "list_items.html",context)

@login_required
def add_items(request):
	form = StockCreateForm(request.POST or None)
	if form.is_valid():
		form.save()
		messages.success(request, 'Enregistré Avec Succès')
		return redirect('/list_items')
	context = { 
	"form": form,
	"title":"AJOUTER PRODUIT",
	}
	return render(request, "add_items.html", context)

def update_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = StockUpdateForm(instance=queryset)
	if request.method == 'POST':
		form = StockUpdateForm(request.POST, instance=queryset)
		if form.is_valid():
			form.save()
			messages.success(request, 'Enregistré Avec Succès')
			return redirect('/list_items')

	context = { 
	'form': form
	}
	return render(request, 'add_items.html', context)


def delete_items(request, pk):
	queryset = Stock.objects.get(id=pk)
	if request.method == 'POST':
		queryset.delete()
		messages.success(request, 'Supprimé avec succès')
		return redirect('/list_items')
	return render(request, 'delete_items.html')

def stock_detail(request, pk):
	queryset = Stock.objects.get(id=pk)
	context = { 
	"queryset": queryset,
	}
	return render(request, "stock_detail.html", context)


def issue_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.recevoir_quantité = 0
        instance.reçu_par = " "
        instance.quantité -= instance.quantité_émis
        instance.émis_par = str(request.user)  # Corrected indentation here

        messages.success(request, "Émis avec succès. " + str(instance.quantité) + " " + str(instance.nom) + "s restent en magasin")
        instance.save()

        return redirect('/stock_detail/' + str(instance.id))
        # return HttpResponseRedirect(i.get_absolute_url())

    context = {
        "title": 'Émettre' + " " + str(queryset.nom),
        "queryset": queryset,
        "form": form,
        "username": 'Émis par:' + str(request.user),
    }
    return render(request, "add_items.html", context)




def receive_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReceiveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.quantité_émis = 0
        instance.émis_par = " "
        instance.quantité += instance.recevoir_quantité
        instance.reçu_par = str(request.user)
        instance.save()
        messages.success(request, "Reçu avec succès. " + str(instance.quantité) + " " + str(instance.nom) + "s en magasin")

        return redirect('/stock_detail/' + str(instance.id))
        # return HttpResponseRedirect(i.get_absolute_url())

    context = {
        "title": 'Recevoir' + " " + str(queryset.nom),
        "instance": queryset,
        "form": form,
        "username": 'Reçu par:' + str(request.user),
    }
    return render(request, "add_items.html", context)




def reorder_level(request, pk):
	queryset = Stock.objects.get(id=pk)
	form = ReorderLevelForm(request.POST or None, instance = queryset)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "niveau de réapprovisionnement du " + str(instance.nom) + " est mis à jour à " + str(instance.niveau_de_réapprovisionnement))
		

		return redirect("/list_items")
		

	context = {
	   "instance":queryset,
	   "form":form,
	   
	}
	return render(request, "add_items.html", context)



@login_required
def list_history(request):
	header = 'LISTE HISTORIQUE'
	queryset = StockHistory.objects.all()
	form = StockSearchForm(request.POST or None)
	context = { 
	"header": header,
	"queryset":queryset,
	"form": form,

	}

	
	if request.method == 'POST':
		catégorie = form['catégorie'].value()
		queryset = StockHistory.objects.filter(
			                    nom__icontains=form['nom'].value()
			                    )
		if (catégorie != ''):
			queryset = queryset.filter(catégorie_id=catégorie)

		if form['exporter_au_format_CSV'].value() == True:
			response = HttpResponse(content_type='text/csv')
			response['Content-Disposition'] = 'attachment; filename="Liste Historique.csv"'
			writer = csv.writer(response)
			writer.writerow(['Catégorie', 'Nom', 'Quantité', 'Quantité émis', 'Quantité reçu', 'Reçu Par', 'Émis Par', 'Date de la dernière maj'])
			i = queryset
			for stock in i:
				writer.writerow([stock.catégorie, stock.nom, stock.quantité, stock.quantité_émis, stock.recevoir_quantité, stock.reçu_par, stock.émis_par, stock.dernière_mise_à_jour])
			return response


		context = { 
	    "form": form,
	    "header":header,
		"queryset":queryset,

	}

	return render(request, "list_history.html", context)



	
























