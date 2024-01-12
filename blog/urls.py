from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.homePage, name='home'),
    path('register/', views.register, name ='register'),
    path('login/', views.login_user, name='login'),
    path('detail-page/<slug:slug>/', views.detail_page, name='detail-page'),
    path('my-blog/', views.second_home, name='second_home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my-blog/detail-page/<slug:slug>/', views.DetailPageView.as_view(), name = 'myblog-detail-page'),
    path('my-blog/read-later/', views.ReadLaterView.as_view(), name = 'read-later'),
    path('my-blog/delete/<slug:slug>/', views.delete_post, name='delete'),
    path('my-blog/<slug:slug>/delete-comment/<int:comment_id>/', views.delete_comment, name='delete-comment'),
    path('my-blog/edit-post/<slug:slug>/', views.edit_post, name='edit-post'),
    path('my-blog/create-post/', views.create_post, name='create-post'),
    path('profile/<int:post_id>/', views.profile_detail, name='profile'),
    path('my-blog/profile/<int:post_id>/', views.logged_profile_detail, name='logged_profile'),
    path('my-blog/my-profile/', views.my_profile, name='my-profile'),
    path('my-blog/my-profile/edit-profile/', views.edit_profile, name='edit-profile'),
]
