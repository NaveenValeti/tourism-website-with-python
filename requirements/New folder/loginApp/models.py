from django.db import models
import bcrypt
from datetime import date
import re

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        duplicateEmail = User.objects.filter(email_address = postData['email'])
        # add keys and values to errors dictionary for each invalid field
        if len(postData['fname']) == 0:
            errors["fnameReq"] = "First name required"
        if len(postData['lname']) == 0:
            errors["lnameReq"] = "Last name required"
        if len(postData['email']) == 0:
            errors["emailReq"] = "Email Address required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['validEmail'] = "Invalid email address"
        elif len(duplicateEmail) > 0:
            errors['taken'] = "There is already and account associated with that email address"
        if len(postData['pw']) == 0:
            errors["pwReq"] = "Password required"
        elif len(postData['pw']) < 8:
            errors["pwLen"] = "Password must be 8 characters or more"
        return errors

    def login_validator(self, postData):
        errors = {}
        duplicateEmail = User.objects.filter(email_address = postData['email'])
        if len(duplicateEmail) == 0:
            errors['emailNotFound'] = "Email address not found. Please register as New User."
        else:
            # if duplicateEmail[0].password != postData['pw']:
            #     errors['wrongPassword'] = "Password is incorrect."
            if not bcrypt.checkpw(postData['pw'].encode(), duplicateEmail[0].password.encode()):
                errors['wrongPassword'] = "Password is incorrect."
        return errors

class ItemManager(models.Manager):
    def item_validator(self, postData):
        errors = {}
        today = str(date.today())
        if len(postData['itemName']) == 0:
            errors["itemReq"] = "Item Name required"
        elif len(postData['itemName']) < 3:
            errors["itemLen"] = "Item Name must be 3 characters or more"
        if len(postData['plan']) == 0:
            errors["itemReq"] = "Description required"
        elif len(postData['plan']) < 3:
            errors["planLen"] = "Description must be 3 characters or more"
        if len(postData['td']) == 0:
            errors["rdReq"] = "Travel Date required"
        elif postData['td'] < today:
            errors["nA"] = "Travel Date must be before Return Date"
        if len(postData['rd']) == 0:
            errors["rdReq"] = "Return Date required"
        elif postData['rd'] < postData['td']:
            errors["nA"] = "Return Date must be after Travel Date"
        # if len(postData['lname']) == 0:
        #     errors["lnameReq"] = "Last name required"
        # if len(postData['email']) == 0:
        #     errors["emailReq"] = "Email Address required"
        # elif not EMAIL_REGEX.match(postData['email']):
        #     errors['validEmail'] = "Invalid email address"
        # elif len(duplicateEmail) > 0:
        #     errors['taken'] = "There is already and account associated with that email address"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Item(models.Model):
    item = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, related_name = 'items_created', on_delete = models.CASCADE)
    wishlist = models.ManyToManyField(User, related_name = 'fav_items')
    start_date = models.DateField(null=True)
    release_date = models.DateField()
    plan = models.CharField(max_length=255, null= True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ItemManager()