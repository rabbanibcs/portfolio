from django.conf import settings
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import Post,Comment,category,Like
from user.models import User
from user.forms import ProfileForm
from django.views.generic import (ListView,
                                    DetailView,
                                    CreateView,
                                    UpdateView,
                                    DeleteView,
                                  )
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin


class PostListView(ListView):
    model = Post
    template_name = 'blog/abstract/index.html' # default: app/model_list.html
    context_object_name = 'posts'   #default: object_list
    ordering = ['-date_posted']
    paginate_by=5

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["home"]=True
        return context

class CategoryView(ListView):
    model = Post
    template_name = 'blog/abstract/category.html' 
    # template_name = 'blog/abstract/index.html' 
    context_object_name = 'posts' 
    ordering = ['-date_posted']
    paginate_by=3

    def get_queryset(self):
        return Post.objects.filter(category=self.kwargs.get('category')).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        for key,value in category:
            if key==self.kwargs.get('category'):
                context['category'] = value
        return context




class UserPostsView(ListView):
    template_name = "blog/abstract/category.html" # default: app/model_list.html
    context_object_name = 'posts'   #default: object_list
    paginate_by=3

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-date_posted')
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        context['page_name'] = "Own Posts"
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/abstract/single-standard.html' 
    context_object_name = 'post'   #default: object_list

    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['likes'] = Like.objects.filter(post_id=self.kwargs.get('pk')).count()
        # print(context['likes'])
        print(self.request.user)
        return context


def create_post(request):
    if request.method=="POST":
        post=Post(
            title=request.POST["title"],
            category=request.POST["category"],
            content=request.POST["content"],
            image=request.FILES.get('image'),
            author=request.user)
        
        post.save()
        print(request.FILES)
        return redirect('post-detail', post.id)
    else:
        return render(request,'blog/post_create_form.html',{
        "page_name":"create_post"
    })

    
    


def create_comment(request,pk):

    post = Post.objects.get(pk=pk)
    comment=Comment(
        author_name=request.POST["name"],
        author_email=request.POST["email"],
        content=request.POST["content"],
        post=post
    )
    comment.save()
    
    return redirect('post-detail', pk)
    

def search(request):
    print(request.GET["words"])
    posts=Post.objects.filter(title__contains=request.GET["words"])
    return render(request,"blog/abstract/category.html",context={
        "posts":posts
    })

from django.contrib.auth import authenticate
from django.contrib.auth import login

def signin(request):
    if request.method=="POST":
        user = authenticate(username=request.POST["email"], password=request.POST["password"])

        if user:
            login(request, user)
            return redirect("post-index")
        else:
            message='Please enter the correct Email and Password for a account.'
            return render(request,"signin.html",{
        "message":message
    })

    return render(request,"signin.html",{
        "page_name":"signin"
    })



from django.contrib.auth import logout
def signout(request):
    logout(request)
    return redirect('signin')

from django.contrib.auth.decorators import login_required

@login_required
def like(request,pk):
    post=Post.objects.get(pk=pk)
    like=Like.objects.get_or_create(post=post,user=request.user)
    return redirect('post-detail', pk)

def liked_posts(request):
    likes=Like.objects.filter(user=request.user)
    print(likes)
    ids=[]
    for like in likes:
        print(like.post.id)
        ids.append(like.post.id)
    print(ids)
    posts=Post.objects.filter(pk__in=ids)
    print(posts)
    return render(request,"blog/abstract/category.html",context={
        "posts":posts,
        "page_name":"Liked Posts"
    })


def signup(request):
    if request.method=="POST":
        password=request.POST.get("password") 
        password_=request.POST.get("password_") 
        if password!=password_:
            return render(request,"signup.html",{
                "message":"Both password must match."
            })

        user=User(email=request.POST.get("email"))
        user.set_password(request.POST.get("password") ) 
        user.is_active = True
        user.save()    
        login(request, user)
        return redirect('post-index')

    return render(request,"signup.html")

def edit_profile(request):
    if request.method=="POST":
        profile=ProfileForm(request.POST,request.FILES)
        if profile.is_valid():
            print(profile.cleaned_data)
            first_name=profile.cleaned_data.get("fname")
            last_name=profile.cleaned_data.get("lname")
            image=profile.cleaned_data.get("image")
            gender=profile.cleaned_data.get("gender")
            about=profile.cleaned_data.get("about")
            email=profile.cleaned_data.get("email")
            user=request.user
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.about=about
            user.gender=gender 
            if image:
                user.image=image

            user.save()
    return render(request,"edit_profile.html",{
        "page_name":"edit_profile"
    })










