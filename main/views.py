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
from django.views.decorators.http import require_POST

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
    data = [
        {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'stock': product.stock,
            'rating': product.rating,
            'user_id': product.user_id,
        }
        for product in products_list
    ]

    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
    try:
        news_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", news_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            'id': str(product.id),
            'name': product.name,
            'price': product.price,
            'description': product.description,
            'thumbnail': product.thumbnail,
            'category': product.category,
            'is_featured': product.is_featured,
            'stock': product.stock,
            'rating': product.rating,
            'user_id': product.user_id,
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({'detail': 'Not found'}, status=404)

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

@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    
    # Check if user owns the product
    if product.user != request.user:
        messages.error(request, 'You do not have permission to edit this product.')
        return redirect('main:show_main')
    
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        messages.success(request, 'Product has been updated successfully.')
        return redirect('main:show_main')

    context = {
        'form': form
    }

    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# Assignment 6
@csrf_exempt
@require_POST
def add_product_entry_ajax(request):
    title = strip_tags(request.POST.get("title")) # strip HTML tags!
    content = strip_tags(request.POST.get("content")) # strip HTML tags!
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == 'on'  # checkbox handling
    user = request.user

    new_product = Product(
        title=title, 
        content=content,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)

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

@csrf_exempt
def delete_product_ajax(request, id):
    if not request.user.is_authenticated:
        return JsonResponse({"status": "error", "message": "Authentication required."}, status=401)

    if request.method == "POST":
        try:
            product = Product.objects.get(pk=id)
            product.delete()
            return JsonResponse({"status": "success", "message": "Product deleted successfully."})
        except Product.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Product not found."}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

def get_product_json(request, id):
    product = get_object_or_404(Product, pk=id)
    data = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "thumbnail": product.thumbnail,
        "category": product.category,
        "stock": product.stock,
        "rating": product.rating,
    }
    return JsonResponse(data)

# def show_json(request):
#     products_list = Product.objects.all()
#     json_data = serializers.serialize("json", products_list)
#     return JsonResponse(json.loads(json_data), safe=False)

def show_xml(request):
    products_list = Product.objects.all()
    xml_data = serializers.serialize("xml", products_list)
    return HttpResponse(xml_data, content_type="application/xml")

# def show_json_by_id(request, product_id):
#     try:
#         news_item = Product.objects.get(pk=product_id)
#         json_data = serializers.serialize("json", [news_item])
#         return JsonResponse(json.loads(json_data), safe=False)
#     except Product.DoesNotExist:
#         return JsonResponse({"error": "Product not found."}, status=404)
    
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