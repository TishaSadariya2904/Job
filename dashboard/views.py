from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from datetime import date
#from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request,'index.html')

def about_us(request):
    return render(request,'about_us.html')

def contact_us(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        m = request.POST['message']

        try:
            ContactUs.objects.create(fname=f,lname=l,mobile=c,message=m)
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'contact_us.html',d)

def admin_login(request):
    error=""
    if request.method=='POST':
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error="yes"
        except:
            error="yes"
    d = {'error':error}        
    return render(request,'admin_login.html',d)

def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    pcount = Provider.objects.all().count()
    scount = SeekerUser.objects.all().count()
    d = {'pcount':pcount,'scount':scount}
    return render(request,'admin_home.html',d)


def user_login(request):
    error=""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = SeekerUser.objects.get(user=user)
                if user1.utype == "seeker":
                    login(request,user)
                    error="no"
                else:
                    error="yes"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'user_login.html',d)


def user_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        e = request.POST['email']
        p = request.POST['pwd']
        g = request.POST['gender']
        i = request.FILES['image']

        try:
            user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
            SeekerUser.objects.create(user=user,mobile=c,image=i,gender=g,utype="seeker")
            error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'user_signup.html',d)


def user_home(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    return render(request,'user_home.html')

def Logout(request):
    logout(request)
    return redirect('index')



def provider_login(request):
    error=""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u,password=p)
        if user:
            try:
                user1 = Provider.objects.get(user=user)
                if user1.utype == "provider" and user1.status!="pending":
                    login(request,user)
                    error="no"
                else:
                    error="not"
            except:
                error="yes"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'provider_login.html',d)


def provider_signup(request):
    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        com = request.POST['company']
        e = request.POST['email']
        p = request.POST['pwd']
        g = request.POST['gender']
        i = request.FILES['image']

        try:
           user = User.objects.create_user(first_name=f,last_name=l,username=e,password=p)
           Provider.objects.create(user=user,mobile=c,image=i,gender=g,company=com,utype="provider",status="pending")
           error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'provider_signup.html',d)

def provider_home(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    return render(request,'provider_home.html')


def view_user(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = SeekerUser.objects.all()
    d = {'data':data}
    return render(request,'view_user.html',d)

def view_contact_list(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = ContactUs.objects.all()
    d = {'data':data}
    return render(request,'view_contact_list.html',d)

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    seeker = SeekerUser.objects.get(id=pid)
    seeker.delete()
    return redirect('view_user')

def delete_contact(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    contactus = ContactUs.objects.get(id=pid)
    contactus.delete()
    return redirect('view_contact_list')


def provider_pending(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Provider.objects.filter(status="pending")
    d = {'data':data}
    return render(request,'provider_pending.html',d)


def provider_accepted(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Provider.objects.filter(status="Accept")
    d = {'data':data}
    return render(request,'provider_accepted.html',d)


def provider_rejected(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Provider.objects.filter(status="Reject")
    d = {'data':data}
    return render(request,'provider_rejected.html',d)


def provider_all(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    data = Provider.objects.all()
    d = {'data':data}
    return render(request,'provider_all.html',d)


def change_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    provider = Provider.objects.get(id=pid)
    if request.method=="POST":
        s = request.POST['status']
        provider.status=s
        try:
            provider.save()
            error="no"
        except:
            error="yes"
    d = {'provider':provider,'error':error}
    return render(request,'change_status.html',d)
    

def delete_provider(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    provider = Provider.objects.get(id=pid)
    provider.delete()
    return redirect('provider_all')


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordadmin.html',d)


def change_passworduser(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passworduser.html',d)


def change_passwordprovider(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    error=""
    if request.method=="POST":
        c = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(c):
                u.set_password(n)
                u.save()
                error="no"
            else:
                error="not"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'change_passwordprovider.html',d)


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    error=""
    if request.method=='POST':
        jt = request.POST['jobtitle']
        #sd = request.POST['startdate']
        #ed = request.POST['enddate']
        sal = request.POST['salary']
        #l = request.FILES['logo']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        user = request.user
        provider = Provider.objects.get(user=user)
        try:
           Job.objects.create(provider=provider,title=jt,salary=sal,description=des,experience=exp,location=loc,skills=skills,creationdate=date.today())
           error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'add_job.html',d)

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    user = request.user
    provider = Provider.objects.get(user=user)
    job = Job.objects.filter(provider=provider)
    d = {'job':job}
    return render(request,'job_list.html',d)


def edit_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    #error=""
    job = Job.objects.get(id=pid)
    error=""
    if request.method=='POST':
        # return HttpResponse(request.POST['jobtitle'])
        jt = request.POST['jobtitle']
        sal = request.POST['salary']
        exp = request.POST['experience']
        loc = request.POST['location']
        skills = request.POST['skills']
        des = request.POST['description']
        
        job.title = jt
        job.salary = sal
        job.experience = exp
        job.location = loc
        job.skills = skills
        job.description = des
        try:
            job.save()
            error="no"
        except:
            error="yes"
    d = {'error':error,'job':job}
    return render(request,'edit_jobdetail.html',d)


def delete_jobdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    job = Job.objects.get(id=pid)
    job.delete()
    return redirect('job_list')


def add_questions(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    error=""
    if request.method=='POST':
        qt = request.POST['quetitle']
        q = request.FILES['question']
        user = request.user
        provider = Provider.objects.get(user=user)
        try:
           Question.objects.create(provider=provider,title=qt,question=q)
           error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'add_questions.html',d)

def que_list(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    user = request.user
    provider = Provider.objects.get(user=user)
    que = Question.objects.filter(provider=provider)
    d = {'que':que}
    return render(request,'que_list.html',d)


def user_que_list(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    data = Question.objects.all()
        
    d = {'data':data}
    return render(request,'user_que_list.html',d)

def edit_que(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    que = Question.objects.get(id=pid)
    error=""
    if request.method=='POST':
        qt = request.POST['quetitle']
        q = request.FILES['question']
        
        que.title = qt
        que.question = q
        try:
            que.save()
            error="no"
        except:
            error="yes"
    d = {'error':error,'que':que }
    return render(request,'edit_que.html',d)


def delete_que(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    que = Question.objects.get(id=pid)
    que.delete()
    return redirect('que_list')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    user = request.user
    provider = Provider.objects.get(user=user)

    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']

        provider.user.first_name = f
        provider.user.last_name = l
        provider.mobile = c
        provider.gender = g

        try:
            provider.save()
            provider.user.save()
            error="no"
        except:
            error="yes"

        try:
            i = request.FILES['image']
            provider.image = i
            provider.save()
            error="no"
        except:
            pass
    d = {'provider':provider,'error':error}
    return render(request,'profile.html',d)



def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    user = request.user
    seeker = SeekerUser.objects.get(user=user)

    error = ""
    if request.method=='POST':
        f = request.POST['fname']
        l = request.POST['lname']
        c = request.POST['contact']
        g = request.POST['gender']

        seeker.user.first_name = f
        seeker.user.last_name = l
        seeker.mobile = c
        seeker.gender = g

        try:
            seeker.save()
            seeker.user.save()
            error="no"
        except:
            error="yes"

        try:
            i = request.FILES['image']
            seeker.image = i
            seeker.save()
            error="no"
        except:
            pass
    d = {'seeker':seeker,'error':error}
    return render(request,'user_profile.html',d)


def latest_jobs(request):
    job = Job.objects.all()
    d = {'job':job}
    return render(request,'latest_jobs.html',d)


def user_latest_jobs(request):
    job = Job.objects.all()
    user = request.user
    seeker = SeekerUser.objects.get(user=user)
    data = Apply.objects.filter(seeker=seeker)
    lst=[]
    for i in data:
        lst.append(i.job.id)
    d = {'job':job,'lst':lst}
    return render(request,'user_latest_jobs.html',d)


def job_detail(request,pid):
    job = Job.objects.get(id=pid)
    d = {'job':job}
    return render(request,'job_detail.html',d)


def applyforjob(request,pid):
    if not request.user.is_authenticated:
        return redirect('user_login')
    
    error = ""
    user = request.user
    seeker = SeekerUser.objects.get(user=user)
    job = Job.objects.get(id=pid)
    date1 = date.today()

    if request.method=='POST':
        r = request.FILES['resume']
        Apply.objects.create(job=job,seeker=seeker,resume=r,applydate=date.today())
        error="done"
    d = {'error':error}
    return render(request,'applyforjob.html',d)


def applied_candidatelist(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')

    data = Apply.objects.all()
        
    d = {'data':data}
    return render(request,'applied_candidatelist.html',d)


def delete_applied_candidate(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    apply = Apply.objects.get(id=pid)
    apply.delete()
    return redirect('applied_candidatelist')


def feedback(request):
    if not request.user.is_authenticated:
        return redirect('user_login')
    error=""
    if request.method=='POST':
        st = request.POST['subtitle']
        m = request.POST['message']
        user = request.user
        seeker = SeekerUser.objects.get(user=user)
        try:
           Feedback.objects.create(seeker=seeker,subject=st,message=m)
           error="no"
        except:
            error="yes"
    d = {'error':error}
    return render(request,'feedback.html',d)


def view_feedback(request):
    if not request.user.is_authenticated:
        return redirect('provider_login')

    feedback = Feedback.objects.all()
    d = {'feedback':feedback}
    return render(request,'view_feedback.html',d)


def delete_feedback(request,pid):
    if not request.user.is_authenticated:
        return redirect('provider_login')
    feedback = Feedback.objects.get(id=pid)
    feedback.delete()
    return redirect('view_feedback')