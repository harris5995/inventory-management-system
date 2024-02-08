from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *

#User Register Form
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'role')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'


#Add Inventory Products Form
class AddProductInventoryForm(forms.ModelForm):
    category = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Category", "class": "form-control"}), label="")
    product_sku = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Product SKU", "class": "form-control"}), label="")
    product_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Product Name", "class": "form-control"}), label="")
    location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder": "Location", "class": "form-control"}), label="")
    quantity = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Quantity", "class": "form-control"}), label="")
    remarks = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Remarks", "class": "form-control"}), label="")
    tags = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder": "Tags", "class": "form-control"}), label="")
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.widgets.Select(attrs={"placeholder": "Supplier", "class": "form-control"}), label="", required=False)

    class Meta:
        model = Product
        exclude = ("user", "supplier")

#CSV file import
class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Upload CSV File')

#Search Feature
class ProductSearchForm(forms.ModelForm):
    category = forms.CharField(required=False)
    product_name = forms.CharField(required=False)
    tags = forms.CharField(required=False)

    class Meta:
        model = Product
        fields = ['category', 'product_name', 'tags']

#Add Inbound Products
class AddInboundProductForm(forms.ModelForm):
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.widgets.Select(attrs={"placeholder": "Supplier", "class": "form-control"}), label="", required=False)

    class Meta:
        model = Inbound_Product
        fields = ['product', 'quantity_received', 'supplier', 'remarks', 'tags']

#Add Inbound Products Form
# class InboundProductForm(forms.ModelForm):
#     category = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Category", "class":"form-control"}), label="")
#     product_sku = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Product SKU", "class":"form-control"}), label="")
#     product_name = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Product Name", "class":"form-control"}), label="")
#     location = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Location", "class":"form-control"}), label="")
#     quantity = forms.IntegerField(required=True, widget=forms.widgets.NumberInput(attrs={"placeholder": "Quantity", "class": "form-control"}), label="")
#     supplier = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Supplier", "class":"form-control"}), label="")
#     remarks = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Remarks", "class":"form-control"}), label="")
#     tags = forms.CharField(required=False, widget=forms.widgets.TextInput(attrs={"placeholder":"Tags", "class":"form-control"}), label="")
    
#     class Meta:
#         model = Inbound_Product 
#         exclude = ("user",)

class AddInboundProductForm(forms.ModelForm):
    category = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Category", "class": "form-control"}))
    product_sku = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Product SKU", "class": "form-control"}))
    product_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Product Name", "class": "form-control"}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Location", "class": "form-control"}))
    quantity_received = forms.IntegerField(widget=forms.NumberInput(attrs={"placeholder": "Quantity Received", "class": "form-control"}))
    remarks = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Remarks", "class": "form-control"}))
    tags = forms.CharField(required=False, widget=forms.TextInput(attrs={"placeholder": "Tags", "class": "form-control"}))
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), widget=forms.Select(attrs={"class": "form-control"}))
    
    class Meta:
        model = Inbound_Product
        fields = ['product', 'quantity_received', 'supplier', 'remarks', 'tags']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


