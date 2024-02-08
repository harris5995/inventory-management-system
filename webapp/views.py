from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import *
from .decorators import manager_required
import csv


#--------------------------------------------------
#The following are the views for the user registration, authentication and management
def home(request):
    #Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, "There was an error. Please try again.")
        return redirect('home')
    else:
        return render(request, 'home.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully registered a user")
            return redirect('home')  # Assuming 'home' is the name of the URL pattern for your home page
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})

def supplier_list(request):
    supplier = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'supplier': supplier})

def customer_list(request):
    customer = Customer.objects.all()
    return render(request, 'customer_list.html', {'customer': customer})

#--------------------------------------------------
#The following are the views for the product inventory list
@manager_required
def inventory_product_list(request):
    if request.user.is_authenticated:
        form = ProductSearchForm(request.POST or None)
        queryset = Product.objects.all()
        if request.method == 'POST':
            if form.is_valid():
                queryset = Product.objects.filter(
                    category__icontains=form.cleaned_data['category'],
                    product_name__icontains=form.cleaned_data['product_name'],
                    tags__icontains=form.cleaned_data['tags']
                )
        inventory = queryset  # Assign the queryset to the inventory variable
        return render(request, 'inventory_product_list.html', {'form': form, 'inventory': inventory})
    else:
        messages.success(request, "You are not authorized to view the product inventory. Please login with the proper credentials.")
        return redirect('home')

@manager_required    
def inventory_product_detail(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        return render(request, 'inventory_product_detail.html', {'product':product})
    else:
        messages.success(request, "You must be logged in to view product details")
        return redirect('home')  

@manager_required
def add_inventory_product(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddProductInventoryForm(request.POST)
            if form.is_valid():
                # Extract data from the form
                product_sku = form.cleaned_data['product_sku']
                quantity = form.cleaned_data['quantity']

                # Check if product with the same SKU exists
                existing_product = Product.objects.filter(product_sku=product_sku).first()

                if existing_product:
                    # Update quantity if product already exists
                    existing_product.quantity += quantity
                    existing_product.save()
                    messages.success(request, "Existing product quantity updated")
                else:
                    # Create new product if it doesn't exist
                    form.save()
                    messages.success(request, "New product added")

                return redirect('inventory_product_list')
        else:
            form = AddProductInventoryForm()
        return render(request, 'add_inventory_product.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to add products")
        return redirect('home')
    

def decrement_product_quantity(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DecrementQuantityForm(request.POST)
            if form.is_valid():
                product_sku = form.cleaned_data['product_sku']
                quantity_to_decrement = form.cleaned_data['quantity_to_decrement']

                # Check if product exists with the given SKU
                existing_product = Product.objects.filter(product_sku=product_sku).first()
                if not existing_product:
                    messages.error(request, "Product with this SKU does not exist")
                    return redirect('decrement_product_quantity')

                # Check if the current stock is greater than 0
                if existing_product.quantity == 0:
                    messages.error(request, "Current stock is 0")
                    return redirect('decrement_product_quantity')

                # Decrement the quantity
                existing_product.quantity -= quantity_to_decrement
                existing_product.save()

                messages.success(request, f"Inventory product quantity updated")
                return redirect('inventory_product_list')
        else:
            form = DecrementQuantityForm()

        return render(request, 'decrement_product_quantity.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to decrement product quantity")
        return redirect('home')
    
    

@manager_required
def csv_upload(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                product_sku = row.get('product_sku')
                quantity_received = int(row.get('quantity_received', 0))  # Use 0 as default value if 'quantity_received' is missing
                remarks = row.get('remarks', '')  # Use empty string as default value if 'remarks' is missing
                category = row.get('category', '')  # Use empty string as default value if 'category' is missing
                product_name = row.get('product_name', '')  # Use empty string as default value if 'product_name' is missing
                location = row.get('location', '')  # Use empty string as default value if 'location' is missing
                
                # Ensure 'product_sku' is not None or empty string
                if product_sku:
                    # Check if product with the same SKU exists
                    existing_product = Product.objects.filter(product_sku=product_sku).first()

                    if existing_product:
                        # Update quantity if product already exists
                        existing_product.quantity += quantity_received
                        existing_product.save()
                    else:
                        # Create new product if it doesn't exist
                        Product.objects.create(
                            category=category,
                            product_sku=product_sku,
                            product_name=product_name,
                            location=location,
                            quantity=quantity_received,
                            remarks=remarks,
                            tags=row.get('tags', '')  # Use empty string as default value if 'tags' is missing
                        )

            messages.success(request, "CSV file uploaded and processed successfully")
            return redirect('inventory_product_list')  # Redirect to the inventory product list page after successful upload
    else:
        form = CSVUploadForm()

    return render(request, 'csv_upload.html', {'form': form})
            
@manager_required    
def update_inventory_product(request, pk):
    if request.user.is_authenticated:
        current_inventory_product = get_object_or_404(Product, id=pk)
        form = AddProductInventoryForm(request.POST or None, instance=current_inventory_product)
        
        if form.is_valid():
                form.save()
                messages.success(request, "Product has been updated")
                return redirect('inventory_product_detail', pk=pk)
        
        return render(request, 'update_inventory_product.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to update product details")
        return redirect('home')

@manager_required    
def delete_inventory_product(request, pk):
    if request.user.is_authenticated:
        delete_it = Product.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete the product")
        return redirect('home')
    

#--------------------------------------------------
#The following are the views for the inbound products        
def inbound_product_list(request):
    if request.user.is_authenticated:
        inbound_product = Inbound_Product.objects.all
        return render(request, 'inbound_product_list.html', {'inbound_product':inbound_product})
    else:
        messages.success(request, "You must be logged in to view the inbound inventory.")
        return redirect('home')  
    
def inbound_product_detail(request, pk):
    if request.user.is_authenticated:
        inbound_product = Inbound_Product.objects.get(id=pk)
        return render(request, 'inbound_product.html', {'inbound_product':inbound_product})
    else:
        messages.success(request, "You must be logged in to view product details")
        return redirect('home')  
    
# def add_inbound_product(request):
#     form = InboundProductForm(request.POST or None)

#     if request.user.is_authenticated:
#         if request.method == "POST":
#             if form.is_valid():
#                 inbound_product = form.save(commit=False)
#                 inbound_product.save()

#                 product = inbound_product.product
#                 quantity_received = inbound_product.quantity_received

#                 # Update inventory quantity
#                 product.quantity += quantity_received
#                 product.save()

#                 messages.success(request, "Inbound product added successfully")
#                 return redirect('inbound_product_list')

#         return render(request, 'add_inbound_product.html', {'form': form})

#     else:
#         messages.error(request, "You must be logged in to add inbound products.")
#         return redirect('home')
    
def add_inbound_product(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddInboundProductForm(request.POST)
            if form.is_valid():
                inbound_product = form.save(commit=False)

                # Retrieve the associated product object
                product = inbound_product.product

                # Update or create the inventory product
                inventory_product, created = Product.objects.get_or_create(
                    product_sku=product.product_sku,
                    defaults={
                        'category': product.category,
                        'product_name': product.product_name,
                        'location': form.cleaned_data['location'],
                        'quantity': form.cleaned_data['quantity_received'],
                        'remarks': form.cleaned_data['remarks'],
                        'tags': form.cleaned_data['tags']
                    }
                )

                # Set tags and remarks for the inbound product
                inbound_product.tags = form.cleaned_data['tags']
                inbound_product.remarks = form.cleaned_data['remarks']

                inbound_product.save()

                # If the product already exists in inventory, update the quantity
                if not created:
                    inventory_product.quantity += form.cleaned_data['quantity_received']
                    inventory_product.save()

                messages.success(request, "Inbound product added successfully")
                return redirect('home')
        else:
            form = AddInboundProductForm()  # Pass the product queryset to the form during initialization

        return render(request, 'add_inbound_product.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to add products")
        return redirect('home')
    


# def add_inbound_product(request):
#     if request.method == "POST":
#         form = AddInboundProductForm(request.POST)
#         if form.is_valid():
#             product = form.cleaned_data['product']
#             supplier = form.cleaned_data['supplier']
#             quantity_received = form.cleaned_data['quantity_received']

#             # Update or create the product in inventory
#             try:
#                 product_in_inventory = Product.objects.get(product_sku=product.product_sku)
#                 product_in_inventory.quantity += quantity_received
#                 product_in_inventory.save()
#             except Product.DoesNotExist:
#                 # Create the product in inventory if it doesn't exist
#                 product_in_inventory = Product.objects.create(
#                     product_sku=product.product_sku,
#                     product_name=product.product_name,
#                     quantity=quantity_received
#                     # Add other fields as needed
#                 )

#             # Create the inbound product entry
#             Inbound_Product.objects.create(
#                 product=product_in_inventory,
#                 supplier=supplier,
#                 quantity_received=quantity_received
#             )

#             messages.success(request, "Inbound product added successfully")
#             return redirect('inbound_product_list')  # Redirect to the home page or any other appropriate page
#     else:
#         form = AddInboundProductForm()

#     return render(request, 'add_inbound_product.html', {'form': form})
    
def update_inbound_product(request, pk):
    if request.user.is_authenticated:
        current_inbound_product = get_object_or_404(Inbound_Product, id=pk)
        form = AddProductInventoryForm(request.POST or None, instance=current_inbound_product)
        
        if form.is_valid():
                form.save()
                messages.success(request, "Inbound product has been updated")
                return redirect('inbound_product_detail', pk=pk)
        
        return render(request, 'update_inbound_product.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to update product details")
        return redirect('home')
    
def delete_inbound_product(request, pk):
    if request.user.is_authenticated:
        delete_it = Inbound_Product.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to delete the product")
        return redirect('home')
    
#--------------------------------------------------
#The following are the views for the outbound products     
def outbound_product_list(request):
    if request.user.is_authenticated:
        outbound = Outbound_Product.objects.all
        return render(request, 'outbound_product_list.html', {'outbound':outbound})
    else:
        messages.success(request, "You must be logged in to view the inbound inventory.")
        return redirect('home')  

def outbound_product_detail(request, pk):
    if request.user.is_authenticated:
        outbound_product = Outbound_Product.objects.get(id=pk)
        return render(request, 'outbound_product_detail.html', {'outbound_product ':outbound_product })
    else:
        messages.success(request, "You must be logged in to view product details")
        return redirect('home')  

def update_outbound_product(request, pk):
    if request.user.is_authenticated:
        current_outbound_product = get_object_or_404(Outbound_Product, id=pk)
        form = AddProductInventoryForm(request.POST or None, instance=current_outbound_product)
        
        if form.is_valid():
                form.save()
                messages.success(request, "Outbound product has been updated")
                return redirect('outbound_product_detail', pk=pk)
        
        return render(request, 'update_outbound_product.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to update product details")
        return redirect('home')

def delete_outbound_product(request, pk):
    if request.user.is_authenticated:
        delete_it = Outbound_Product.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('outbound_product_list')
    else:
        messages.success(request, "You must be logged in to delete the product")
        return redirect('home')

# def inventory_product_list(request):
#     if request.user.is_authenticated:
#         form = ProductSearchForm(request.POST or None)
#         inventory = Product.objects.all
#         return render(request, 'inventory_product.html', {'inventory':inventory})
#     else:
#         messages.success(request, "You are not authorized to view the product inventory. Please login with the proper credentials.")
#         return redirect('home')


# Inventory Product Views 
# def inventory_product_list(request):
#     if request.user.is_authenticated:
#         form = ProductSearchForm(request.POST or None)
#         queryset = Product.objects.all()
#         context = { 
#             "form": form,
#             "queryset": queryset,
#             }
#         if request.method == 'POST':
#             queryset = Product.objects.filter(
#                 category__icontains=form['category'].value(),
#                 product_name__icontains=form['product_name'].value(),
#                 tags__icontains=form['tags'].value()
#                                             )
#             context = { 
#                 "form": form,
#                 "queryset": queryset,
#                 }
#         return render(request, 'inventory_product.html', context)
#     else:
#         messages.success(request, "You are not authorized to view the product inventory. Please login with the proper credentials.")
#         return redirect('home')
    
# def add_inbound_product(request):
#     form = InboundProductForm(request.POST or None)

#     if request.user.is_authenticated:
#         if request.method == "POST":
#             if form.is_valid():
#                 product_sku = form.cleaned_data['product_sku']
#                 quantity = form.cleaned_data['quantity']

#                 existing_product = Product.objects.filter(product_sku=product_sku).first()

#                 if existing_product:
#                     # Update the quantity of the existing product
#                     existing_product.quantity += quantity
#                     existing_product.save()
#                 else:
#                     # Create a new product if it doesn't exist
#                     new_product = Product(
#                         product_sku=product_sku,
#                         quantity=quantity,
#                         product_name=form.cleaned_data['product_name'],
#                         location=form.cleaned_data['location'],
#                         supplier=form.cleaned_data['supplier'],
#                         remarks=form.cleaned_data['remarks'],
#                         tags=form.cleaned_data['tags'],
#                         # Add other fields as needed
#                     )
#                     new_product.save()

#                 # Save the inbound product
#                 form.save()

#                 messages.success(request, "Product added")
#                 return redirect('home')

#         return render(request, 'add_inbound_product.html', {'form': form})

#     else:
#         messages.success(request, "You must be logged in to add products")
#         return redirect('home')