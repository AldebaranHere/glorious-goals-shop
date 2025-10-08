from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers
from main.forms import ProductForm
from main.models import Product
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags

# Create your views here.
# Assignment 2
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'

    if filter_type == "all":
        products_list = Product.objects.all()
    else:
        products_list = Product.objects.filter(user=request.user)

    context = {
        'npm': '2406365370',
        'name': request.user.username,
        'class': 'PBP KKI',
        'products_list': products_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html",context)

# Assignment 3
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit = False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    
    return render(request, "create_product.html", context) # create_product

@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)

    context = {
        'product': product
    }

    return render(request, "product_detail.html", context) # product_detail

def show_xml(request):
    products_list = Product.objects.all()
    xml_data = serializers.serialize("xml", products_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    products_list = Product.objects.all()
    json_data = serializers.serialize("json", products_list)
    return HttpResponse(json_data, content_type="application/json")

def show_xml_by_id(request, product_id):
    try:
        news_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        news_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [news_item])
        return HttpResponse(json_data, content_type="application/json")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

# Assignment 4    
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)

   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product.delete()
        messages.success(request, 'Product has been deleted successfully.')
    return HttpResponseRedirect(reverse('main:show_main'))

# Assignment 6
@csrf_exempt
def add_product_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = ProductForm(data)
        if form.is_valid():
            product_entry = form.save(commit=False)
            product_entry.user = request.user
            product_entry.save()
            return JsonResponse({"message": "Product added successfully!"}, status=201)
        else:
            errors = {field: [strip_tags(error) for error in errors] for field, errors in form.errors.items()}
            return JsonResponse({"errors": errors}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

@csrf_exempt
def edit_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        data = json.loads(request.body)
        form = ProductForm(data, instance=product)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Product updated successfully!"}, status=200)
        else:
            errors = {field: [strip_tags(error) for error in errors] for field, errors in form.errors.items()}
            return JsonResponse({"errors": errors}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

def delete_product_ajax(request, id):
    product = get_object_or_404(Product, pk=id)
    if request.method == "POST":
        product.delete()
        return JsonResponse({"message": "Product has been deleted successfully!"}, status=200)
    return JsonResponse({"error": "Invalid request method."}, status=405)

def get_product_json(request):
    products_list = Product.objects.all()
    json_data = serializers.serialize("json", products_list)
    return JsonResponse(json.loads(json_data), safe=False)

def show_json(request):
    products_list = Product.objects.all()
    json_data = serializers.serialize("json", products_list)
    return JsonResponse(json.loads(json_data), safe=False)

def show_xml(request):
    products_list = Product.objects.all()
    xml_data = serializers.serialize("xml", products_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json_by_id(request, product_id):
    try:
        news_item = Product.objects.get(pk=product_id)
        json_data = serializers.serialize("json", [news_item])
        return JsonResponse(json.loads(json_data), safe=False)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)
    
def show_xml_by_id(request, product_id):
    try:
        news_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def register_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = UserCreationForm(data)
        if form.is_valid():
            form.save()
            return JsonResponse({"message": "Your account has been successfully created!"}, status=201)
        else:
            errors = {field: [strip_tags(error) for error in errors] for field, errors in form.errors.items()}
            return JsonResponse({"errors": errors}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)

def login_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        form = AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = JsonResponse({"message": "Login successful!"}, status=200)
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            errors = {field: [strip_tags(error) for error in errors] for field, errors in form.errors.items()}
            return JsonResponse({"errors": errors}, status=400)
    return JsonResponse({"error": "Invalid request method."}, status=405)