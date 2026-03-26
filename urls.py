from django.urls import path,include
from good import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home,name = 'home' ),
   # path('about/', views.about_view, name= 'about'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('', views.base_view, name = 'base'),
    path('my_network/', views.my_network_view, name = 'my_network'),
    path('signup/', views.signup_view, name = 'signup'),
    path('profile/<username>/', views.profile, name = 'profile'),
    path('people/', views.people_view, name='people'),
    path("connection-count/", views.connection_count_api, name="connection_count_api"),
    #path("connections/<str:username>/", views.connections_api, name="connections_api"),
    path("mutual-connections/<str:username>/", views.mutual_connections_api, name="mutual_connections_api"),
    path("profile/<str:username>/toggle_visibility/", views.toggle_visibility, name="toggle_visibility"),
    path('profile_settings/', views.profile_settings, name='profile_settings'),
    
    path('feed/', views.feed, name='feed'),
   # path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path("upload-main-picture/", views.upload_main_picture, name="upload_main_picture"),
    path("upload-inner-picture/", views.upload_inner_picture, name="upload_inner_picture"),
    path('education/<int:education_id>/edit/', views.edit_education, name = 'edit_education'),
    path('education/<int:education_id>/delete/', views.delete_education, name = 'delete_education'),
    #path('add_education/', views.add_education, name = 'add_education'),
    #path('add_experience/', views.add_experience, name = 'add_experience'),
    path('experience/<int:experience_id>/edit/', views.edit_experience, name = 'edit_experience'),
    path('experience/<int:experience_id>/delete/', views.delete_experience, name = 'delete_experience'),
    #path('profile/skill/add/', views.add_skill, name = 'add_skill'),
    path('skill/<int:skill_id>/edit/', views.edit_skill, name = 'edit_skill'),
    path('skill/<int:skill_id>/delete/', views.delete_skill, name = 'delete_skill'),
    path('language/<int:language_id>/delete/', views.delete_language, name = 'delete_language'),
    path('language/<int:language_id>/edit/', views.edit_language, name = 'edit_language'),
    path('skillchoice/', views.skillchoice,name = 'skillchoice' ),
    path('write_post/', views.write_post, name = 'write_post'),
    path('create_postimage/', views.create_postimage, name = 'create_postimage'),
    path('create_postvideo/', views.create_postvideo, name = 'create_postvideo'),
    path('create_postarticle/', views.create_postarticle, name = 'create_postarticle'),
    path('delete-post/<uuid:post_id>/', views.delete_post, name='delete_post'),
    path("post/<uuid:post_id>/save/", views.save_post, name="save_post"),
    path('like-post/', views.like_post, name='like_post'),
    path('react-post/', views.react_post, name='react_post'),
    path('get-reactions/', views.get_reactions, name='get_reactions'),
    path('send-request/', views.send_friend_request, name='send_friend_request'),
    path("notification/", views.notification_page, name="notification"),
    path("notifications/json/", views.get_notifications, name="notifications"),  # for AJAX
    path("friend-request/<int:request_id>/accept/", views.accept_request, name="accept_request"), 
    path("friend-request/<int:request_id>/reject/", views.reject_request, name="reject_request"),
    
    path("users/", views.user_list, name="user_list"),
    path("chat/random/", views.random_chat, name="random_chat"),
    path("chat/<int:user_id>/", views.chat_messages, name="chat_messages"),
    path("chat/<int:user_id>/send/", views.send_message, name="send_message"),
    path("profile/<int:user_id>/", views.user_profile, name="user_profile"),
    




   
   path('password_reset/', auth_views.PasswordResetView.as_view(
         template_name='registration/password_reset_form.html',
         email_template_name='registration/password_reset_email.html',
         subject_template_name='registration/password_reset_subject.txt'
     ),
     name='password_reset'),


    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view( 
          template_name='registration/password_reset_done.html' 
          ), name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
         template_name='registration/password_reset_confirm.html'
     ),
     name='password_reset_confirm'),




    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
        ), name='password_reset_complete'),

    

]
