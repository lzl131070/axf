from django.db import models

# Create your models here.
class Goods(models.Model):
    productid, productimg, productname, productlongname, isxf, pmdesc, specifics, price, marketprice, categoryid, childcid, childcidname, dealerid, storenums, productnum=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]

class Wheel(models.Model):
    img, name, trackid=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]

class Nav(models.Model):
    img, name, trackid=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]

class Mustbuy(models.Model):
    img, name, trackid=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]
class Shop(models.Model):
    img, name, trackid=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]


class Mainshow(models.Model):
    trackid, name, img, categoryid, brandname, img1, childcid1, productid1, longname1, price1, marketprice1, img2, childcid2, productid2, longname2, price2, marketprice2, img3, childcid3, productid3, longname3, price3, marketprice3=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]

class Foodtypes(models.Model):
    typeid, typename, childtypenames, typesort=[models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),models.CharField(max_length=200),]


class User(models.Model):
    account = models.CharField(max_length=255,unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=20)
    adv = models.CharField(max_length=255)
    img = models.CharField(max_length=255,default='/static/uploads/axf.png')
    rank = models.IntegerField(default=1)
    token= models.CharField(max_length=255)

class Cart(models.Model):
    userid = models.ForeignKey(User)
    goodid = models.ForeignKey(Goods)
    num = models.IntegerField()
    isselect=models.BooleanField(default=True)

