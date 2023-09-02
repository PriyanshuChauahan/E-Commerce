from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Order, OrderUpdate
from math import ceil
import json

# Create your views here.


def index(request):
    def nSlides(n):
        return n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        allProds.append([prod, range(1, nSlides(len(prod)))])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thank = False
    if (request.method == "POST"):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank = True

    return render(request, 'shop/contact.html', {'thank': thank})


def tracker(request):
    if (request.method == "POST"):
        order_id = request.POST.get('order_id', '')
        email = request.POST.get('email', '')

        try:
            order = Order.objects.filter(order_id=order_id, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=order_id)
                updates = []
                totalAmount = order[0].amount
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps(
                    [updates, order[0].items_json, totalAmount], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    query = request.GET.get('search', '')
    query = query.lower()

    def nSlides(n):
        return n//4 + ceil((n/4)-(n//4))

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}

    def searchMatch(query, item):
        ''' return true only if query matches the item'''
        if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():

            return True
        else:

            return False
    for cat in cats:

        prodtemp = Product.objects.filter(category=cat)

        prod = [item for item in prodtemp if searchMatch(query, item)]

        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides(len(prod)))])
    params = {'allProds': allProds, 'msg': ""}

    if len(allProds) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter Revelant search Query"}
    print
    return render(request, 'shop/search.html', params)


def productView(request, myid):
    # fetch the product using id
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/product.html', {'product': product[0]})


def checkout(request):
    if (request.method == "POST"):
        thank = False
        name = request.POST.get('inputName', '')
        email = request.POST.get('inputEmail', '')
        phone = request.POST.get('inputPhone', '')
        address = request.POST.get('inputAddress', '')
        address2 = request.POST.get('inputAddress', '')
        city = request.POST.get('inputCity', '')
        state = request.POST.get('inputState', '')
        zip_code = request.POST.get('inputZip', '')
        itemJson = request.POST.get('itemJson', "")
        amount = request.POST.get('total_amount', "")
        order = Order(name=name, email=email, phone=phone, address=address, address2=address2,
                      city=city, state=state, zip_code=zip_code, items_json=itemJson, amount=amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id,
                             update_desc="the order has been placed")
        update.save()
        thank = True

        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
    return render(request, 'shop/checkout.html')
