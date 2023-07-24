from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True) #null=True means it is not required
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, null=True) #null=True means it is not required
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    # if the image is not available, then we will return a default image
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class Order(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) # if the customer is deleted, then set the order to null
    date_ordered = models.DateTimeField(auto_now_add=True) #auto_now_add=True means that the date will be added automatically
    complete = models.BooleanField(default=False, null=True, blank=False) #blank=False means that the field is required
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id) #return the order id


    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all() #get all the order items
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping


    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all() #get all the order items
        total = sum([item.get_total for item in orderitems]) #sum all the order items
        return total


    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all() #get all the order items
        total = sum([item.quantity for item in orderitems]) #sum all the order items
        return total
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL) # if the product is deleted, then set the order item to null
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL) # if the order is deleted, then set the order item to null
    quantity = models.IntegerField(default=0, null=True, blank=True) #blank=False means that the field is required
    date_added = models.DateTimeField(auto_now_add=True) #auto_now_add=True means that the date will be added automatically

    def __str__(self):
        return str(self.id) #return the order item id


    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL) # if the customer is deleted, then set the shipping address to null
    order = models.ForeignKey(Order, null=True, on_delete=models.SET_NULL) # if the order is deleted, then set the shipping address to null
    address = models.CharField(max_length=200, null=False) #null=False means that the field is required
    city = models.CharField(max_length=200, null=False) #null=False means that the field is required
    state = models.CharField(max_length=200, null=False) #null=False means that the field is required
    zipcode = models.CharField(max_length=200, null=False) #null=False means that the field is required
    date_added = models.DateTimeField(auto_now_add=True) #auto_now_add=True means that the date will be added automatically

    def __str__(self):
        return self.address #return the address
    


