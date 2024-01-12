from django.shortcuts import render ,redirect, get_object_or_404
from .models import Post, Comment, UserProfile
from .forms import RegisterForm, LoginForm, CommentForm, EditForm, CreatePostForm, EditProfile, UserImageForm
from django.contrib.auth import authenticate, login as auth_login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.utils.decorators import method_decorator
# Create your views here.

def homePage(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/index.html', {
        'posts': posts,
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        imageForm = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            if imageForm.is_valid():
                user_profile = imageForm.save(commit=False)
                user_profile.user = user
                user_profile.save()

            authenticated_user = authenticate(
                request,
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1']
            )
            if authenticated_user is not None:
                auth_login(request, authenticated_user)
                messages.success(request, "You've successfully registered.")
                return redirect('home')
        else:
            messages.error(request, "There was a problem with your registration.")
    else:
        form = RegisterForm()
        imageForm = UserImageForm()
    return render(request, 'blog/register.html', {
        'form': form,
        'user_image': imageForm,
    })

def login_user(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('second_home')
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {
        'form': form,
    })

def detail_page(request, slug):
        post = get_object_or_404(Post, slug=slug)
        return render(request, 'blog/post-detail.html', {
            'post': post,
            'tags': post.tags.all(),
            'comments': post.comments.all().order_by('-id')
        })

@login_required
def second_home(request):
    posts = Post.objects.all().order_by('-date')
    return render(request, 'blog/second_index.html', {
        'posts': posts,
    })

@method_decorator(login_required, name='dispatch')
class DetailPageView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        
        return is_saved_for_later
    
    def get(self,request, slug):
        posts = get_object_or_404(Post, slug=slug)
        return render(request, 'blog/logged_post_details.html', {
            'posts':posts,
            'tags': posts.tags.all(),
            'comment_form': CommentForm(),
            'comments': posts.comments.all().order_by('-id'),
            'saved_for_later' : self.is_stored_post(request, posts.id),
        })

    def post(self,request, slug):
        comment_form = CommentForm(request.POST)
        posts = get_object_or_404(Post, slug=slug)

        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.post = posts
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(reverse('myblog-detail-page', kwargs={'slug': slug} ))
        
        return render(request, 'blog/logged_post_details.html', {
            'posts':posts,
            'tags': posts.tags.all(),
            'comment_form': CommentForm(),
            'comments': posts.comments.all().order_by('-id'),
            'saved_for_later' : self.is_stored_post(request, posts.id),
        })
    
@login_required
def delete_comment(request, slug, comment_id):
    post = get_object_or_404(Post, slug=slug)
    comment = get_object_or_404(Comment, post=post, pk=comment_id, user=request.user)
    if request.method == 'POST':
        comment.delete()
        return redirect('myblog-detail-page', slug=slug)
    return HttpResponseForbidden('Invalid request method')

@method_decorator(login_required, name='dispatch')
class ReadLaterView(View):
        def get(self, request):
                stored_posts = request.session.get('stored_posts')

                context = {}

                if stored_posts is None or len(stored_posts) == 0:
                        context['posts'] = []
                        context['has_posts'] = False
                else:
                        posts = Post.objects.filter(id__in = stored_posts)
                        context['posts'] = posts
                        context['has_posts'] = True

                return render(request, 'blog/stored_posts.html', context)
        
        def post(self, request):
                stored_posts = request.session.get('stored_posts')
                
                if stored_posts is None:
                        stored_posts = []
                
                post_id = int(request.POST['post_id'])

                if post_id not in stored_posts:
                        stored_posts.append(post_id)
                else:
                        stored_posts.remove(post_id)

                request.session['stored_posts'] = stored_posts

                return HttpResponseRedirect(reverse('second_home'))

@login_required
def delete_post(request, slug):
    if request.method =='POST':
        post = get_object_or_404(Post, slug=slug, author= request.user)
        post.delete()
        return HttpResponseRedirect(reverse('second_home')) 
    return HttpResponseForbidden('Invalid request method')

@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug, author=request.user)
    if request.method == 'POST':
        form = EditForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
                form.save()
                messages.success(request, 'Post has been updated successfully.')
                return redirect('myblog-detail-page', slug=post.slug)
        else:
            print(form.errors)
            messages.error(request, 'Invalid input, please try again.')
    else:
        form = EditForm(instance=post)
    return render(request, 'blog/edit-post.html', {
              'form': form,
              'post': post,
         })

@login_required
def create_post(request):
    if request.method == 'POST':
            form = CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit = False)
                post.author = request.user
                post.save()


                tags = form.cleaned_data.get('tags')
                for tag in tags:
                    post.tags.add(tag) 

                messages.success(request, 'Post created successfully.')
                return redirect('second_home')
            else:
                messages.error(request, 'Invalid input, please try again.')
    else:
         form = CreatePostForm()
    return render(request, 'blog/create_post.html', {
              'form': form,
         })

def profile_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    image = get_object_or_404(UserProfile, user = post.author)
    return render(request, 'blog/user_detail.html', {
          'post': post,
          'image': image
     })
@login_required
def logged_profile_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    image = get_object_or_404(UserProfile, user = post.author)
    return render(request, 'blog/logged_user_detail.html', {
          'posts': post,
          'image': image,
     })

@login_required
def my_profile(request):
    posts = Post.objects.filter(author=request.user)
    image =  get_object_or_404(UserProfile, user= request.user)
    return render(request, 'blog/my_profile.html', {
         'posts': posts,
         'image' : image,
    })

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        password = PasswordChangeForm(request.user, request.POST)
        image = UserImageForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save()
            if password.is_valid():
                    user = password.save()
                    update_session_auth_hash(request, user)
            if image.is_valid():
                    image.save()

            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('my-profile')
        else:
               messages.error(request, 'Please correct the error below.')
    else:
        form = EditProfile(instance=request.user)
        password = PasswordChangeForm(request.POST)
        image = UserImageForm(instance=user_profile)

    return render(request, 'blog/edit_profile.html', {
         'form': form,
         'password': password,
         'image' : image,
    })

