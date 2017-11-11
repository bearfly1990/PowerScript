from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item
def home_page(request):
    # if request.method == 'POST':
        # return HttpResponse(request.POST['item_text'])
    if request.method == 'POST':
        new_item_text = request.POST['item_text']
        Item.objects.create(text=new_item_text)
        return redirect('/')
    else:
        new_item_text = ''
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
    # return render(request, 'home.html', {
        # 'new_item_text': new_item_text,
    # })
# Create your views here.
