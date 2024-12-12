from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.db import connection


from .models import *

# Create your views here.
def index(request):
    x=category.objects.all().order_by('-id')[0:6]
    pdata=myproduct.objects.all().order_by('-id')[0:7]
    mydict={"data":x,"prodata":pdata}
    return render(request,'user/index.html',context=mydict)
def about(request):
    return render(request,'user/aboutus.html')
##########################################
def product(request):
    return render(request,'user/product.html')
##########################################
def myorder(request):
    user=request.session.get('userid')
    data=""
    if user:
        cursor=connection.cursor()
        cursor.execute("select p.*,o.* form user_myproduct p,user_morder o where p.id=o.pid and o.userid='"+str(user)+"'")
        data=cursor.fetchall()
    mydict={"odata":data}
    return render(request,'user/myorder.html',mydict)
##########################################
def enquiry(request):
    status=False
    if request.method=="POST":
        a=request.POST.get('name')
        b=request.POST.get('email')
        c=request.POST.get('mob')
        d=request.POST.get('msg')
        contactus(Name=a,Mobile=c,Email=b,Message=d).save()
        status=True

        #mdict={"Name":a,"Email":b,"Mobile":c,"Message":d}

    msg={"m":status}
    return render(request,'user/enquiry.html',context=msg)
##########################################
def showcart(request):
    user=request.session.get('userid')
    cid=a=request.GET.get('cid')
    pid=request.GET.get('pid')
    md={}
    a = request.GET.get('msg')
    if user:
        if a is not None:
            mcart.objects.all().filter(id=a).delete()
            return HttpResponse("<script>alert('your iteam is deleted from card..');location.href='/user/showcart/'</script>")
        elif pid is not None:
            mcart.objects.all().filter(id=cid).delete()
            morder(userid=user,pid=pid,remarks="pending",status=True,odate=datetime.now().date()).save()
            return HttpResponse("<script>alert('your order has been placed successfully..');location.href='/user/myorder/'</script>")
        cursor=connection.cursor()
        cursor.execute("select p.*,c.*from user_myproduct p,user_mcart c where p.id=c.pid and c.userid='"+str(user)+"'")
        cdata=cursor.fetchall()
        md={"cdata":cdata}

    return render(request,'user/showcart.html',md)
def cpdetail(request):
    c=request.GET.get('cid')
    p=myproduct.objects.all().filter(pcategroy=c)
    return render(request,'user/cpdetail.html',{"pdata":p})
##########################################
##########################################
def signup(request):
    if request.method=="POST":
        Name=request.POST.get('name').G
        Email=request.POST.get('email')
        Mobile=request.POST.get('mob')
        password=request.POST.get('passwd')
        Address=request.POST.get('Address')
        picture=request.FILE.get('pic')
        x=register.objects.all().filter(email=Email).count()
        if x==0:
            request.session['userid']=Email
            register(name=Name, email=Email, mobile=Mobile, ppic=picture, passwd=password, address=Address).save()
            return HttpResponse("<script>alert('you ar registre successfully');location.href='/user/signup/'</script>")
        else:
            return HttpResponse("<script>alert('you email id is already registered');location.href='/user/signup/'</script>")
    return render(request,'user/signup.html')
##########################################
def myprofile(request):
    user=request.session.get('userid')
    x=""
    if user:
        x=register.object.all().filter(email=user)
    d={"mdata":x}
    return render(request,'user/myprofile.html')
##########################################
def signin(request):
    if request.method=="post":
        Email=request.POST.get('email')
        Passwd=request.POST.get('password')
        x=register.object.all().filter(email=Email,passwd=Passwd).count()
        if x==1:
            request.session['userid']=Email
            return HttpResponse("<script>alert('you are login..');location.href='/user/signin/'</script>")
        else:
            return HttpResponse("<script>alert('your userid or password is incorrect..');location.href='/user/signin/'</script>")
    return render(request,'user/signin.html')
###########################################
def mens(request):
    cid=request.GET.get('msg')
    cat=category.objects.all().order_by('-id')
    d=myproduct.objects.all().filter(mcategory=1)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=1,pcategory=cid)
    mydict={"cats":cat,"data":d,"a":cid}
    return render(request,'user/mens.html',mydict)
###########################################
def womens(request):
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=2)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=2, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid}
    return render(request,'user/womens.html',mydict)
############################################
def kids(request):
    cid = request.GET.get('msg')
    cat = category.objects.all().order_by('-id')
    d = myproduct.objects.all().filter(mcategory=3)
    if cid is not None:
        d = myproduct.objects.all().filter(mcategory=3, pcategory=cid)
    mydict = {"cats": cat, "data": d, "a": cid}
    return render(request,'user/kids.html',mydict)

def viewproduct(request):
    a = request.GET.get('abc')
    x = myproduct.objects.all().filter(id=a)
    return render(request, 'user/viewproduct.html', {"pdata": x})
def signout(request):
    if request.session.get('userid'):
        return HttpResponse("<script>alert('you are signed out..');location.href='/user/index/'</script>")
def myordr(request):
    user=request.session.get('userid')
    pid=request.GET.get('msg')
    print(pid)
    print(user)
    if user:
        if pid is not None:
            morder(userid=user,pid=pid,remarks="pending",odate=datetime.now().date(),status=True).save()
            return HttpResponse ("<script>alert('you order confired...').location.href='user/index/'</script>")

    else:
        return HttpResponse("<script>alert('you have to login first...');loaction.href='/user/index/'</script>")
    return render(request,'user/myordr.html')
def mycart(request):
    p=request.GET.get('pid')
    user=request.session.get('userid')
    if user:
        if p is not None:
            mcart(userid=user,pid=p,cdate=datetime.now().date,status=True).save()
            return HttpResponse("<script>alert('you iteam is added cart.....');location.href='/user/index/'</script>")
    else:
        return HttpResponse("<script>alert('you have to login first....');location.href='/user/signin/'</script>")
    return render(request,'user/mcart.html')