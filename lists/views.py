from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.forms import ExistingListItemForm, ItemForm
from lists.models import Item, List

# We need to officially register our 'lists' app with Django. Therefore, need to add 'lists' to
# INSTALLED_APPS in superlists/settings.py

# A messy views.py is bad. Try to shift the implementation to something like a form

# Create your views here.
def home_page(request):
	# if request.method == 'POST':
	# 	Item.objects.create(text=request.POST['item_text']) # creates a new Item, without needing to call .save()
	# 	return redirect('/lists/the-only-list-in-the-world') # https://en.wikipedia.org/wiki/Post/Redirect/Get
	

	return render(request, 'home.html', {'form': ItemForm()})
		
	# return render(request, 'home.html', {
	# 	'new_item_text': new_item_text  # render takes a dictionary as its third argument, which maps template variable names
	# 	# to their values, so we can use it for the POST case as well as the normal case. Also, request.POST would create an error in the
	# 	# case where we don't send a POST. Therefore, request.POST.get returns a default value '' when we're doing a normal GET request.
	# 	})
	# return render(request, 'home.html') # Django searches all app's directories to find a file named
										# templates then builds an HttpResonse based on content of file

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	form = ExistingListItemForm(for_list=list_)

	if request.method == 'POST':
		form = ExistingListItemForm(for_list=list_, data=request.POST)
		if form.is_valid():
			form.save()	
			return redirect(list_)
		# try:
		# 	item = Item(text=request.POST['item_text'], list=list_)
		# 	item.full_clean()
		# 	item.save()

		# 	# Item.objects.create(text=request.POST['item_text'], list=list_)
		# 	return redirect(list_)

	return render(request, 'list.html', {'list': list_, "form": form})

def new_list(request):
	form = ItemForm(data=request.POST)
	if form.is_valid(): # checks whether the form's data is a good or bad submission
		list_ = List.objects.create()
		form.save(for_list=list_)
		# Item.objects.create(text=request.POST['text'], list=list_)
		return redirect(list_)
	else:
		return render(request, 'home.html', {"form": form})

	# return redirect(list_) # we can do this because every list item is associated with a URL (an absolute URL)
	# return redirect(f'/lists/{list_.id}/')

# def add_item(request, list_id):
# 	list_ = List.objects.get(id=list_id)
# 	Item.objects.create(text=request.POST['item_text'], list=list_)
# 	return redirect(f'/lists/{list_.id}/')