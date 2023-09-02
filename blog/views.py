from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.
def index(request):
    blogs=Blogpost.objects.all()
    params={'blogs':blogs}
    return render(request,'blog/index.html',params)

def blogpost(request,id):
    # allpost=Blogpost.objects.all()
    # post=[]
    # i=0
    # if id>0 :
    #     post[0]=Blogpost.objects.filter(post_id=id-1)[0]
        
    # while(i<=id+1 and i<=allpost.__len__()):
    #     post.append(Blogpost.objects.filter(post_id=i)[0])
    post=Blogpost.objects.filter(post_id=id)[0]
          

    return render(request,'blog/blogpost.html',{'post':post})

    