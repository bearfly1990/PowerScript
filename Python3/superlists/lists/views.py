from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item, List
def home_page(request):
    # if request.method == 'POST':
        # return HttpResponse(request.POST['item_text'])
    # items = Item.objects.all()
    return render(request, 'home.html')
    # return render(request, 'home.html', {'items': items})
    # return render(request, 'home.html', {
        # 'new_item_text': new_item_text,
    # })
# Create your views here.
def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
    
def new_list(request):
    _list = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=_list)
    return redirect('/lists/the-only-list-in-the-world/')