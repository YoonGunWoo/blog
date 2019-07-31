from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog
from .form import BlogPost

# Create your views here.
def home(request):
    blogs = Blog.objects #쿼리셋

    blog_list = Blog.objects.all()
    #모든 블로그 글들을 대상으로

    paginator = Paginator(blog_list, 3)
    #3개를 1개의 페이지로

    page = request.GET.get('page')
    #request된 페이지가 뭔디 알아냄

    posts = paginator.get_page(page)
    #request된 페이지를 얻어온 뒤 return 해준다.

    return render(request, 'home.html', {'blogs': blogs, 'posts':posts})

def detail(request, blog_id):
    details = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'detail.html',{'details': details})

def new(request): #단순히 new.html을 띄워주는 함수
    return render(request, 'new.html')

#render는 프로젝트 내에서 사전형으로 데이터 넘길 수 있다
#redirect는 외부 url도 이동가능

def create(reqeust): #입력받은 내용을 데이터베이스에 넣어주는 함수
    blog = Blog()
    blog.title = reqeust.GET['title']
    blog.body = reqeust.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save() #data base에 저장해라

    return redirect('/blog/'+str(blog.id))
    #위에거 다 처리하고 해당 url로 이동해라 blog.id는 int형이니까 str로 형변환

def blogpost(request):
    #1. 입력된 내용을 처리하는 기능 -> POST
    #2. 빈 페이지를 띄어주는 기능 -> GET
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.now()
            post.save()
            return redirect('home')
    else :
        form = BlogPost()
        return render(request, 'new.html', {'form' : form})