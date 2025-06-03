from django.db import models

class skin(models.Model):
    sid=models.AutoField(primary_key=True)
    sname=models.CharField(max_length=100)
    sdetails=models.CharField(max_length=100)
    sprice=models.FloatField(default=0.0)
    skin_image=models.ImageField(upload_to="media/")
    highest_bid=models.FloatField(default=0.0)
    highest_bidder=models.ForeignKey('customer',null=True,blank=True,on_delete=models.SET_NULL)
    bid_end_time = models.DateTimeField(null=True, blank=True)  # Allows user input

    def save(self, *args, **kwargs):
        if not self.bid_end_time:  
            self.bid_end_time = now() + timedelta(minutes=5)  # Default 5-minute bid time if not provided
        super().save(*args, **kwargs)
    
class customer(models.Model):
    cname=models.CharField(max_length=100,null=False)
    cemailid=models.CharField(primary_key=True,max_length=100)
    cpassword=models.CharField(max_length=100,null=False)
    c_contactno=models.IntegerField(max_length=15,null=False)

class bid(models.Model):
    skin=models.ForeignKey('skin',on_delete=models.CASCADE)
    customer=models.ForeignKey('customer',on_delete=models.CASCADE)
    bid_amount=models.FloatField()
    
class cart(models.Model):
    cartid=models.ForeignKey(skin,on_delete=models.CASCADE)
    emailid=models.ForeignKey(customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    totalprice=models.FloatField(default=0.0)
    is_bid_winner=models.BooleanField(default=False)
    
class order(models.Model):
    cust=models.ForeignKey(customer,on_delete=models.CASCADE)
    orderNo=models.CharField(max_length=100)
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.BigIntegerField()
    phoneno=models.BigIntegerField()
    totalbill=models.FloatField(default=0.0)
    
class Admin(models.Model):
    adminid=models.CharField(primary_key=True,max_length=100)
    adminpassword=models.CharField(max_length=100)