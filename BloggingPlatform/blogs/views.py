from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from .forms import CommentForm
from django.db.models import Q


# Create your views here.
def home(request):
    posts = BlogPost.objects.order_by('-created_at')[:5]
    context = {
        'posts': posts
    }
    return render(request,'homepage.html',context)
    
def profile(request):
    blog_posts = BlogPost.objects.all()
    blog_posts = blog_posts.filter(author=request.user).values()
    user_profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'profile.html', {'user_profile': user_profile,'blog_posts':blog_posts})

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        # Perform input validation and create the user
        try:
            if User.objects.filter(username = email).first():
                messages.error(request, "This email is already taken")
                return redirect('register')
            username = email.split('@')[0]
            user = User.objects.create_user(email=email, password=password,username=username, first_name=first_name, last_name=last_name)
            UserProfile.objects.create(user=user)
            print("Registration Successfull")
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
        except Exception as e:
            messages.error(request, 'Email Already Exists')
            return redirect('register')
    return render(request, 'accounts/register.html')
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request,"accounts/login.html")
def user_logout(request):
    logout(request)
    return redirect('home')


#Post related actions
@login_required
def createpost(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        body = request.POST['body']
        
        author = request.user
        try:
            if BlogPost.objects.filter(title = title).first():
                messages.error(request, "This email is already taken")
                return redirect('register')
            post = BlogPost.objects.create(title=title,description=description,body=body,author=author)
            print("Post Created////////")
            post.save()
            messages.success(request, 'Post Created Successfully')
            return redirect('home')  # Redirect to the home page after successful registration
        except Exception as e:
            messages.error(request, str(e))
            print("Exception")
            return redirect('home')
    return redirect('home')

#just because of this..@login_required 
def edit_blog_post(request, post_id):
    try:
        post = get_object_or_404(BlogPost, pk=post_id)
        #post = BlogPost.objects.filter(title=title).values() #now we have to pass the title along with url.
        if request.user != post.author:
            messages.error(request,"Login TO Edit Only Created By Yours")
            print("You are not allowed to edit")
            return redirect('home')
        if request.method == 'POST':
            
            title = request.POST['title']
            description = request.POST['description']
            body = request.POST['body']
            author = request.user

            #here I am updating by deleting previous versions.. As I havent used forms.. its causing error.
            post.delete()
            print("old deleted, new created")
            post = BlogPost.objects.create(title=title,description=description,body=body,author=author)
            post.save()
            print("Post Edited////////")
            messages.success(request, 'Your post has been updated.')
            return redirect('home')
    except:
        messages.error("You have to login to Edit")
    #here we need to send post details clearly..
    return render(request, 'edit_blog_post.html',{ 'post': post})

#@login_required
def delete_blog_post(request, post_id):
    #this method and above method needs to be added to a button...
    post = get_object_or_404(BlogPost, pk=post_id)
    if request.user == post.author:
        post.delete()
        print('deleted')
        messages.success(request, 'Your post has been deleted.')
    return redirect('home')

#for adding comment
def add_comment(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog_post = blog_post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'comment.html', {'form': form})

def blog_post_detail(request, post_id):
    blog_post = get_object_or_404(BlogPost, id=post_id)
    comments = Comment.objects.filter(blog_post=blog_post)
    return render(request, 'edit_blog_post.html', {'blog_post': blog_post, 'comments': comments})

#to view individual post
def viewpost(request,post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    print("post",post)    
    comments = Comment.objects.filter(blog_post=post.id).values()

    print("comments",comments)
    return render(request, 'viewpost.html',{ 'post': post,'comments':comments})


#search and Filter Functionality
def search_blog_posts(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    tag_id = request.GET.get('tag')

    blog_posts = BlogPost.objects.all()

    if query:
        blog_posts = blog_posts.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(body__icontains=query))

    if category_id:
        blog_posts = blog_posts.filter(categories__id=category_id)

    if tag_id:
        blog_posts = blog_posts.filter(tags__id=tag_id)

    return render(request, 'search_blog_posts.html', {'blog_posts': blog_posts})

def filter_categories(request):
    categories = Category.objects.all()
    return render(request, 'filter_categories.html', {'categories': categories})

def filter_tags(request):
    tags = Tag.objects.all()
    return render(request, 'filter_categories.html', {'tags': tags})

#messges are not showing..