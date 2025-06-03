from django.shortcuts import render , redirect ,get_object_or_404
from django.http import HttpResponse
from .models import skin , customer , cart ,order , bid , Admin
from django.contrib.auth.hashers import make_password,check_password
from datetime import date ,datetime
from django.contrib import messages
import razorpay
from django.core.mail import send_mail
from django.utils.timezone import now 
from django.utils import timezone
from django.conf import settings

def index(request):
    return render(request,'index.html')

def addskin(request):
    if request.method=='POST':
        name=request.POST['name']
        details=request.POST['details']
        price=request.POST['price']
        image=request.FILES.get('image')
        bid_end_time = request.POST.get('bid_end_time')
        if bid_end_time: 
            bid_end_time = timezone.make_aware(datetime.strptime(bid_end_time, "%Y-%m-%dT%H:%M"))

        else:
            bid_end_time = now() + timedelta(minutes=5) 

        data = skin.objects.create(sname=name, sdetails=details, sprice=price, skin_image=image, bid_end_time=bid_end_time)
        data.save()
        return Httpresponse("<h1>Successfully added</h1>")
    else:
        return render(request, 'addskin.html')
    
def skinlist(request):
    data=skin.objects.all() #select * from skin
    current_time = now()  # Get current time
    return render(request, 'skinlist.html', {"slist": data, "current_time": current_time})

def shopcust(request):
    data = skin.objects.all()
    current_time = now()
    user_email = "abc@gmail.com"
    user = customer.objects.get(cemailid=user_email)

    for s in data:
        if s.bid_end_time < current_time and s.highest_bidder == user:
            if not cart.objects.filter(cartid=s, emailid=user, is_bid_winner=True).exists():
                cart.objects.create(
                    cartid=s,
                    emailid=user,
                    totalprice=s.highest_bid,
                    is_bid_winner=True
                )
    
    return render(request, 'shopcust.html', {"slist": data, "current_time": current_time})


def updateskin(request):
    if request.method=='POST':
        uid=request.POST['uid']
        name=request.POST['name']
        details=request.POST['details']
        price=request.POST['price']
        image=request.FILES.get('image')
        old_data=skin.objects.filter(sid=uid)
        if image:  # Only update image if provided
            old_data.update(skin_image=image)
        old_data.update(sname=name,sdetails=details,sprice=price)
        return HttpResponse("<h1>Updated successfully</h1>")
    else:
        return render(request,'updateskin.html')
    
def editbyid(request,sid):
    old_data=skin.objects.get(sid=sid)
    return render(request,"updateskin.html",{"skin":old_data})

def deletebyid(request,sid):
    old_data=skin.objects.get(sid=sid)
    old_data.delete()
    return HttpResponse("<h1>Deleted successfully</h1>")

#bid
def bidding(request):
    all_bids = bid.objects.all() 
    return render(request, "bidding.html", {"all_bids": all_bids})

def place_bid(request, sid):
    if request.method == 'POST':
        product = get_object_or_404(skin, sid=sid)

        # Prevent bidding if time has expired
        if product.bid_end_time < now():
            messages.error(request, 'Bidding for this item has ended.')
            return redirect('shopcust')

        bid_amount = float(request.POST['bid_amount'])
        user_email = "abc@gmail.com"
        user = customer.objects.get(cemailid=user_email)

        if bid_amount > product.highest_bid:
            bid.objects.create(skin=product, customer=user, bid_amount=bid_amount)
            product.highest_bid = bid_amount
            product.highest_bidder = user
            product.save()
            messages.success(request, 'Bid placed successfully')
        else:
            messages.error(request, 'Your bid must be higher than the current bid')

    return redirect('shopcust')


def add_bid_to_cart(request,sid):
    product = get_object_or_404(skin, sid=sid)
    user_email = "abc@gmail.com"
    user = customer.objects.get(cemailid=user_email)

    if product.highest_bidder == user:
        cart.objects.create(cartid=product, emailid=user, totalprice=product.highest_bid, is_bid_winner=True)
        messages.success(request, "Winning bid item added to cart!")
    else:
        messages.error(request, "Only the highest bidder can add this item.")

    return redirect('showcart')
        
# customer
def addcustomer(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        hashed_password = make_password(password)
        contact=request.POST['contact']
        data=customer.objects.create(cname=name,cemailid=email,cpassword=hashed_password,c_contactno=contact)
        data.save()
        return render(request,"login.html")
    else:
        return render(request,'addcustomer.html')

def admin(request):
    if request.method=='POST':
        adminid='aishwarya@gmail,com'
        adminpassword='123456'
        data=Admin.objects.create()
        data.save()

def customerlist(request):
    data=customer.objects.all()
    return render(request,'customerlist.html',{"clist":data})

def updatecustomer(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        contact=request.POST['contact']
        old_data=customer.objects.filter(cemail=email)
        old_data.update(cname=name,cpassword=password,c_contactno=contact)
        return HttpResponse("<h1>Updated successfully</h1>")
    else:
        return render(request,'updatecustomer.html')       

def editbyemail(request ,cemailid):
    old_data=customer.objects.get(cemailid=cemailid)
    return render(request,"updatecustomer.html",{"customer":old_data})

def deletebyemail(request,cemailid):
    old_data=customer.objects.get(cemailid=cemailid)
    old_data.delete()
    return HttpResponse("<h1>Deleted successfully</h1>")
    
# cart
def addtocart(request,sid):
    data=skin.objects.get(sid=sid)
    email="abc@gmail.com"
    cust=customer.objects.get(cemailid=email)
    quantity=1
    totalprice=data.sprice*quantity
    cart.objects.create(cartid=data, emailid=cust, quantity=quantity, totalprice=totalprice)
   
    return HttpResponse("Added to cart")

def showcart(request):
    user_email="abc@gmail.com"
    user=customer.objects.get(cemailid=user_email)
    cart_data=cart.objects.filter(emailid=user)
    totalprice = sum(item.cartid.highest_bid for item in cart_data)
    return render(request, 'showcart.html', {'data': cart_data,'totalprice': totalprice})
    
def updateprice(request,cid,q,tprice):
    cart_data=cart.objects.filter(id=cid)
    cart_data.update(quantity=q,totalprice=tprice)
    return redirect ('showcart')

#login
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        cust = customer.objects.filter(cemailid=email).first()
        admin = Admin.objects.filter(adminid=email).first()

        if admin:
            if admin.adminpassword == password:
                request.session['adminid'] = email
                return render(request, 'index.html')
            else:
                return HttpResponse('Login Failed: Incorrect Password')
        elif cust:
            if check_password(password, cust.cpassword):
                request.session['cemailid'] = email
                return render(request, 'index.html')
            else:
                return HttpResponse('Login Failed: Incorrect Password')
        else:
            return HttpResponse('Login Failed: User Not Found')

    return render(request, 'login.html')
        
def logout(request):
    session_key=list(request.session.keys())
    for key in session_key:
        del request.session[key]
    return render(request,'index.html')
                        
#order placing

def placeorder(request):
    if request.method=='POST':
        emailid="abc@gmail.com"
        cust=customer.objects.get(cemailid=emailid)
        name=request.POST['Name']
        address=request.POST['Address']
        city=request.POST['City']
        state=request.POST['State']
        pincode=request.POST['Pincode']
        phoneno=request.POST['Phoneno']
        tprice=request.POST['tprice']
        data=order.objects.create(cust=cust,name=name,address=address,city=city,state=state,pincode=pincode,phoneno=phoneno,totalbill=tprice)
        data.save()
        day=date.today()
        day=str(day).replace("-","")
        orderno=str(data.id)+day
        data.orderno=orderno
        data.save()
        print(data.orderno)
        razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        currency = 'INR'
        amount = 20000  # Rs. 200
    
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    
        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
    
        # we need to pass these details to frontend.
        context = {}
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZORPAY_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        return render(request,'payment.html',{'orderobj':data,'totalbill':data.totalbill,'context':context})
    else:
        emailid="abc@gmail.com"
        cust=customer.objects.get(cemailid=emailid)
        Cart=cart.objects.filter(emailid=cust , is_bid_winner=True)
        tprice=0
        for i in Cart:
            tprice=tprice+i.totalprice
        return render(request,'order.html',{"tprice":tprice})
    
def paymentsuccess(request):
    # window.location.href = `paymentsuccess?order_id={{orderobj.orderNo}}&payment_id=${response.razorpay_payment_id}`;
    oid=request.GET['order_id']
    pid=request.GET['payment_id']
    tbill=request.GET['tbill']
    subject='Your Order Get Place'
    email_body='Order Id:- '+oid+'payment Id:- '+pid+'Total Bill:- '+tbill
    from_email=settings.EMAIL_HOST_USER
    send_mail(subject=subject,message=email_body,from_email=from_email,
              recipient_list=['aishwaryalohakare7@gmail.com'])
    
    return HttpResponse('Email Send Successfully')

