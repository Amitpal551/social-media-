from urllib import request
from django.shortcuts import render,redirect,HttpResponse
from django.http import HttpResponseBadRequest
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseNotFound
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from django.contrib import messages
from django.db import connections, models
from django.core.mail import EmailMessage
from django.contrib.auth.views import PasswordResetView
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.utils import timezone
from django.contrib.auth.forms import SetPasswordForm
from .models import Profile,Post,Education,Experience,Skill,Language,Message,Like,Share,About,Comment,Reaction,FriendRequest,Notification
from .forms import EducationForm,ProfileForm,ExperienceForm,LanguageForm,SkillForm,ImagePostForm,VideoPostForm,ArticlePostForm,CommentForm,ReplyForm,ShareForm,AboutForm,PostForm





@login_required(login_url='login')
def home(request):
    user_objects = User.objects.get(username=request.user.username)
    user_profile =Profile.objects.get(user=user_objects)

    posts = Post.objects.all()
    return render(request,'home.html',{'user_profile' : user_profile,'posts':posts})

@login_required(login_url='login')
def skillchoice(request):
    user_objects = User.objects.get(username=request.user.username)

    user_profile =Profile.objects.get(user=user_objects)
    return render(request,'skillchoice.html')


def get_connection_data(user):
    connections = FriendRequest.objects.filter(
        Q(from_user=user) | Q(to_user=user),
        status="accepted"
    )

    connected_users = set()
    for fr in connections:
        if fr.from_user == user:
            connected_users.add(fr.to_user)
        else:
            connected_users.add(fr.from_user)

    return len(connected_users), connected_users

@login_required(login_url='login')
def base_view(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    posts = Post.objects.all()
    comments = {}
    replies = {}
    for post in posts:
        comments[post.id] = post.comment_set.all()
        for comment in comments[post.id]:
            replies[comment.id] = comment.replies.all()
    image_form = ImagePostForm()
    video_form = VideoPostForm()
    article_form = ArticlePostForm()
    comment_form = CommentForm()
    reply_form = ReplyForm()

    count, connected_users = get_connection_data(request.user)

    

    if request.method == 'POST':
        post_type = request.POST.get('post_type')
        if post_type == 'image':
            image_form = ImagePostForm(request.POST, request.FILES)
            if image_form.is_valid():
                post = image_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('base')
        elif post_type == 'video':
            video_form = VideoPostForm(request.POST, request.FILES)
            if video_form.is_valid():
                post = video_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('base')
        elif post_type == 'article':
            article_form = ArticlePostForm(request.POST, request.FILES)
            if article_form.is_valid():
                post = article_form.save(commit=False)
                post.user = request.user
                post.post_type = "article"   # force article type
                post.save()
                return redirect('base')
        elif 'comment' in request.POST:
            post_id = request.POST.get('post_id')
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.post = Post.objects.get(id=request.POST['post_id'])
                comment.save()
                return redirect('base')
        elif 'reply' in request.POST:
            reply_form = ReplyForm(request.POST)
            if reply_form.is_valid():
                reply = reply_form.save(commit=False)
                reply.user = request.user
                reply.comment = Comment.objects.get(id=request.POST['comment_id'])
                reply.save()
                return redirect('base')

            


    return render(request, 'base.html', {
        'user_profile': user_profile,
        'posts': posts,
        'comments': comments,
        'replies': replies, 
        'image_form': image_form,
        'video_form': video_form,
        'article_form': article_form,
        'comment_form': comment_form,
        'reply_form': reply_form,
        "count": count,
    })



def create_postimage(request):
    if request.method == 'POST':
        form = ImagePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            # Redirect to base.html after saving
            return redirect('base')   # 'base' should be the name of your urlpattern for base.html
    else:
        form = ImagePostForm()
    return render(request, 'create_postimage.html', {'form': form})






def create_postvideo(request):
    if request.method == 'POST':
        form = VideoPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('base')
    else:
        form = VideoPostForm()
    return render(request, 'create_postvideo.html', {'form': form})



@login_required
def create_postarticle(request):
    if request.method == 'POST':
        form = ArticlePostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.post_type = "article"
            post.save()
            return redirect('base')  # redirect to feed
        else:
            print(form.errors)  # Debugging: see why form fails
    else:
        form = ArticlePostForm()
    return render(request, 'create_postarticle.html', {'form': form})






from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post  # adjust to your actual Post model

@login_required
def write_post(request):
    if request.method == "POST":
        text = request.POST.get("post-text")
        image = request.FILES.get("image")
        video = request.FILES.get("video")

        if not text and not image and not video:
            return JsonResponse({"success": False, "error": "Post cannot be empty"})

        # Save post (adjust fields to your Post model)
        post = Post.objects.create(
            user=request.user,
            content=text,
            image=image if image else None,
            video=video if video else None
        )

        return JsonResponse({"success": True, "post_id": post.id})

    return JsonResponse({"success": False, "error": "Invalid request"})




@require_http_methods(['POST'])
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user == request.user:
        post.delete()
        messages.success(request, 'Post deleted successfully')

    return redirect('base')



@login_required
def save_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # You can store saves in a ManyToMany field (like likes/shares)
    post.shares.add(request.user)   # or create a dedicated "saved_posts" relation
    messages.success(request, "Post saved successfully!")

    return redirect("base")


def like_post(request):
    post_id = request.POST.get('post_id')
    post = Post.objects.get(id=post_id)
    user = request.user
    like, created = Like.objects.get_or_create(post=post, user=user)
    if not created:
        like.delete()
        action = 'unlike'
    else:
        action = 'like'
    return JsonResponse({'action': action})


def react_post(request):
    post_id = request.POST.get('post_id')
    emoji = request.POST.get('emoji')
    post = Post.objects.get(id=post_id)
    user = request.user
    reaction = Reaction.objects.get_or_create(post=post, user=user)[0]
    reaction.emoji = emoji
    reaction.save()
    reaction_count = Reaction.objects.filter(post=post).count()
    return JsonResponse({'emoji': emoji, 'reaction_count': reaction_count})

def get_reactions(request):
    post_id = request.GET.get('post_id')
    reactions = Reaction.objects.filter(post_id=post_id)
    reaction_count = reactions.count()
    data = {
        'reactions': [{'emoji': reaction.emoji} for reaction in reactions],
        'reaction_count': reaction_count
    }
    return JsonResponse(data)


def select_emoji(request,pk):
    post = Post.objects.get(pk=pk)
    like = Like.objects.get(user=request.user, post=post)
    emoji = request.POST.get('emoji')
    like.emoji = emoji
    like.save()
    return redirect('base')



def signup_view(request):
    if request.method == 'POST':
        firstname = request.POST.get ('firstname')
        lastname = request.POST.get ('lastname')
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        username = request.POST.get ('username')


        myuser = User.objects.filter(username = username)
        if myuser.exists():
            messages.info(request,'username already taken')
            return redirect('signup')
    
        myuser=User.objects.create_user(username,email,password)
        myuser.first_name = firstname
        myuser.last_name = lastname
        myuser.save()
        messages.success(request,'Account created successfully')
        return redirect('base')


    return render(request,'signup.html')
   


def login_view(request):
    if request.method == "POST":

        username = request.POST.get ('username')
        password = request.POST.get ('password')

        if  not User.objects.filter(username = username).exists():
            messages.error(request,'invalid username')
            return redirect('login')

        myuser = authenticate(username=username,password=password)

        if myuser is not None :
           # messages.info(request,'invalid username and password.')
           auth.login(request,myuser)
           return redirect('base')

            
        else:
         # messages.info(request,f'{username},you are logged in.')
         messages.info(request,'credentials invalid')
        return redirect('login')

    
    return render(request,"login.html")

    
@login_required(login_url='login')
def logout_view(request):
    logout(request)
   
    messages.info(request,"logged Out successfully")
    return redirect('login')

def feed(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'base.html', {'posts':posts[::-1]})


def profile(request,username):

    user = get_object_or_404(User, username=username)
    #profile = Profile.objects.get(user=user)
    #user_profile = Profile.objects.get(user=request.user)

    try: 
        profile = Profile.objects.get(user=user) 
    except Profile.DoesNotExist:
        profile = None
        
        
        mutual_connections = []
    if request.user.is_authenticated and profile:
      try:
          logged_in_profile = Profile.objects.get(user=request.user)
          mutual_connections = get_mutual_connections(logged_in_profile, profile)
          suggested = User.objects.exclude(id=request.user.id)

        # Exclude already friends
          suggested = suggested.exclude(id__in=logged_in_profile.friends.all())

          pending_ids = FriendRequest.objects.filter( 
              Q(from_user=request.user) | Q(to_user=request.user), 
              status="pending" 
          ).values_list("from_user_id", "to_user_id", flat=False)
          exclude_ids = set() 
          for from_id, to_id in pending_ids:
            exclude_ids.add(from_id)
            exclude_ids.add(to_id)
          suggested = suggested.exclude(id__in=exclude_ids) 
          suggested = suggested.filter(profiles__isnull=False).distinct()
          suggested = suggested[:3]
      except Profile.DoesNotExist: 
            suggested = [] 
            mutual_connections = []
    else: 
            suggested = []
            mutual_connections = []

    educations = Education.objects.filter(user=user)
    experiences = Experience.objects.filter(user=user)
    skills = Skill.objects.filter(user=user)
    languages = Language.objects.filter(user=user)
    about = About.objects.filter(user=user).first()
    current_user = request.GET.get('user')
    logged_in_user = request.user.username
    education_form = EducationForm()
    exprience_form = ExperienceForm()
    skill_form = SkillForm()
    language_form = LanguageForm()
    about_form = AboutForm(instance=about)

    if request.method == 'POST' :
        if 'education_submit' in request.POST:
            education_id = request.POST.get('education_id')
            if education_id:
                education = Education.objects.get(id=education_id)
                education_form = EducationForm(request.POST, instance=education)
            else:
                education_form = EducationForm(request.POST)
            if education_form.is_valid():
                education = education_form.save(commit=False)
                education.user = request.user
                education.save()
                return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#education-section')
        elif  'experience_submit' in request.POST:
            exprience_id = request.POST.get('experience_id')
            if exprience_id:
                experience = Experience.objects.get(id=exprience_id)
                exprience_form = ExperienceForm(request.POST, instance=experience)
            else:
                exprience_form = ExperienceForm(request.POST)
            if exprience_form.is_valid():
                experience = exprience_form.save(commit=False)
                experience.user = request.user
                experience.save()
                return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#experience-section')
            
        elif  'skill_submit' in request.POST:
            skill_id = request.POST.get('skill_id')
            if skill_id:
                skill = skill.objects.get(id=skill_id)
                skill_form = SkillForm(request.POST, instance=skill)
            else:
                skill_form = SkillForm(request.POST)
            if skill_form.is_valid():
                skill = skill_form.save(commit=False)
                skill.user = request.user
                skill.save()
                return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#skill-section')
            
        elif  'language_submit' in request.POST:
            language_id = request.POST.get('language_id')
            if language_id:
                language = language.objects.get(id=language_id)
                language_form = LanguageForm(request.POST, instance=language)
            else:
                language_form = LanguageForm(request.POST)

            if language_form.is_valid():
                language = language_form.save(commit=False)
                language.user = request.user
                language.save()
            
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#language-section')
    
        elif 'about_submit' in request.POST:
            about_id = request.POST.get('about_id')
            
            if about_id:
                about_instance = About.objects.get(id=about_id)
                about_form = AboutForm(request.POST, instance=about_instance)
            else:
                about_form = AboutForm(request.POST)
            if about_form.is_valid():
                about = about_form.save(commit=False)
                about.user = request.user
                about.save()
                return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#about-section')
    
           

    return render(request, 'profile.html', {
        'educations': educations,
        'experiences': experiences,
        'skills': skills,
        'languages':languages,
        'profile': profile,
        'about': about,
        'user':user,
        'curren_user':current_user,
        'education_form': education_form,
        'exprience_form': exprience_form,
        'skill_form': skill_form,
        'language_form':language_form,
        'about_form': about_form,
        's_friends': suggested,
        'mutual_connections': mutual_connections,
    })

def get_mutual_connections(logged_in_profile, viewed_profile):
    # Mutuals = overlap between both users' friends
    return logged_in_profile.friends.filter(id__in=viewed_profile.friends.all())

def mutual_connections_api(request, username):
    profile_user = get_object_or_404(User, username=username)
    try:
        viewed_profile = Profile.objects.get(user=profile_user)

        if request.user.is_authenticated:
            logged_in_profile = Profile.objects.get(user=request.user)
            mutuals = get_mutual_connections(logged_in_profile, viewed_profile)
            data = [u.username for u in mutuals]
        else:
            # Anonymous fallback: show all connections of viewed profile
            data = [u.username for u in viewed_profile.friends.all()]

        return JsonResponse({"count": len(data), "connections": data})
    except Profile.DoesNotExist:
        return JsonResponse({"count": 0, "connections": []})
    


@csrf_exempt
def toggle_visibility(request, username):
    if request.method == "POST":
        data = json.loads(request.body)
        field = data.get("field")
        visible = data.get("visible", True)

        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)

            if field == "email":
                profile.show_email = visible
            elif field == "phone":
                profile.show_phone = visible
            elif field == "website":
                profile.show_website = visible

            profile.save()
            return JsonResponse({"status": "success", "field": field, "visible": visible})
        except (User.DoesNotExist, Profile.DoesNotExist):
            return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)
        


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from geopy.geocoders import Nominatim

@csrf_exempt
def update_location(request):
    if request.method == 'POST' and request.user.is_authenticated:
        data = json.loads(request.body)
        lat = data.get('latitude')
        lon = data.get('longitude')

        if lat and lon:
            geolocator = Nominatim(user_agent="myapp")
            location = geolocator.reverse(f"{lat}, {lon}")
            if location:
                profile = request.user.profiles
                profile.location = location.address
                profile.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from .models import Profile

@login_required
def profile_settings(request):
    profile = Profile.objects.get(user=request.user)
    about, _ = About.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        about_form = AboutForm(request.POST, instance=about)

        if profile_form.is_valid() and about_form.is_valid():
            profile_form.save()
            about_form.save()
            return redirect('profile', username=request.user.username)
    else:
        profile_form = ProfileForm(instance=profile)
        about_form = AboutForm(instance=about)

    return render(request, 'profile_settings.html', {
        'profile_form': profile_form,
        'about_form': about_form,
    })





@login_required
def people_view(request):
    # Suggestions
    all_users = User.objects.exclude(id=request.user.id)
    sent_ids = FriendRequest.objects.filter(
        from_user=request.user
    ).values_list("to_user_id", flat=True)
    s_friends = all_users.exclude(id__in=sent_ids)[:150]
    count, connected_users = get_connection_data(request.user)

    return render(
        request,
        "people.html",
        {
            "s_friends": s_friends,
            "count": count,
            "connected_users": connected_users,
        },
    )


@login_required
def connection_count_api(request):
    count, _ = get_connection_data(request.user)
    return JsonResponse({"count": count})




@login_required
@csrf_exempt
def upload_main_picture(request):
    if request.method == "POST" and request.FILES.get("main_picture"):
        profile = request.user.profiles  # <-- FIXED
        profile.profileimg_main = request.FILES["main_picture"]
        profile.save()
        return JsonResponse({"status": "success", "new_image_url": profile.profileimg_main.url})
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
@csrf_exempt
def upload_inner_picture(request):
    if request.method == "POST" and request.FILES.get("inner_picture"):
        profile = request.user.profiles  # <-- FIXED
        profile.profileimg_inner = request.FILES["inner_picture"]
        profile.save()
        return JsonResponse({"status": "success", "new_image_url": profile.profileimg_inner.url})
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
@csrf_exempt
#
# def upload_profile_picture(request):
    #if request.method == "POST" and request.FILES.get("profile_picture"):
      #  profile = request.user.profile  # OneToOne relation
        #profile.profileimg_main = request.FILES["profile_picture"]
       # profile.save()
       # return JsonResponse({
           # "status": "success",
           # "new_image_url": profile.profileimg.url
       # })
   # return JsonResponse({"error": "Invalid request"}, status=400)


#def add_experience(request):
    #if request.method == 'POST':
       # form = ExperienceForm(request.POST)
        #if form.is_valid():
          #  experience = form.save(commit=False)
            #experience.user = request.user
            
           # experience.save()
        #return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#experience-section')
        

        
    #else:
        #form = ExperienceForm()
    #return render(request, 'add_experience.html', {'form': form})

def edit_experience(request,experience_id):
    experience = Experience.objects.get(id=experience_id)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#experience-section')
    else:
     form = ExperienceForm(instance=experience)

    return render(request, 'edit_experience.html', {'form': form})


def edit_skill(request,skill_id):
    skill = Skill.objects.get(id=skill_id)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#skill-section')
    else:
     form = SkillForm(instance=skill)

    return render(request, 'edit_skill.html', {'form': form})



def delete_experience(request,experience_id):
    experience = Experience.objects.get(id=experience_id)
    if experience.user == request.user:
        experience.delete()
        messages.success(request, 'experience deleted successfully')

    return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#experience-section')

def delete_skill(request,skill_id):
    skill = Skill.objects.get(id=skill_id)
    if skill.user == request.user:
        skill.delete()
        messages.success(request, 'skill deleted successfully')

    return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#skill-section')


@login_required
@require_POST
def delete_language(request, language_id):
    language = Language.objects.get(id=language_id)
    if language.user == request.user:
        language.delete()
        messages.success(request, 'Language deleted successfully')
    return HttpResponseRedirect(
        reverse('profile', args=[request.user.username]) + '#language-section'
    )

def edit_language(request,language_id):
    language = Language.objects.get(id=language_id)
    if request.method == 'POST':
        form = LanguageForm(request.POST, instance=language)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#language-section')
    else:
     form = LanguageForm(instance=language)

    return render(request, 'edit_skill.html', {'form': form})




def edit_education(request,education_id):
    education = Education.objects.get(id=education_id)
    if request.method == 'POST':
        form = EducationForm(request.POST, instance=education)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#education-section')

    else:
     form = EducationForm(instance=education)

    return render(request, 'edit_education.html', {'form': form})

def delete_education(request,education_id):
    education = Education.objects.get(id=education_id)
    if education.user == request.user:
        education.delete()
        messages.success(request, 'education deleted successfully')

    return HttpResponseRedirect(reverse('profile', args=[request.user.username]) + '#education-section')

def add_skill(request):

    if request.method =='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user 
            skill.save()
            return redirect('profile')
        else:
            form = SkillForm()

    return render(request,'add_skill.html',{'form':form})



def write_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('base')
    else:
        form = PostForm()
    return render(request, 'write_post.html', {'form': form})






@login_required
def my_network_view(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status="pending")
    return render(request, "my_network.html", {"requests": pending_requests})



def get_notifications(request):
    notes = Notification.objects.filter(user=request.user, is_read=False)
    data = [{"id": n.id, "message": n.message, "created": n.created.strftime("%H:%M")} for n in notes]
    return JsonResponse({"notifications": data})
    


def notification_page(request):
    notes = Notification.objects.filter(user=request.user).order_by("-created")
    return render(request, "notification.html", {"notifications": notes})


@login_required
def send_friend_request(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            to_user_id = data.get("receiver_id")
            from_user = request.user

            if not FriendRequest.objects.filter(from_user=from_user, to_user_id=to_user_id).exists():
                FriendRequest.objects.create(from_user=from_user, to_user_id=to_user_id)
                return JsonResponse({"success": True})
            return JsonResponse({"success": False, "error": "Request already sent"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request"})


def accept_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.status = "accepted"
    fr.save()
    return JsonResponse({"success": True, "status": "accepted"})

def reject_request(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    fr.status = "rejected"
    fr.save()
    return JsonResponse({"success": True, "status": "rejected"})



class CustomPasswordResetView(auth_views.PasswordResetView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = settings.DEFAULT_DOMAIN
        context['protocol'] = 'http'
        return context


import random

@login_required
def user_list(request):
    # Get IDs of accepted connections (both directions)
    accepted_from = FriendRequest.objects.filter(from_user=request.user, status="accepted").values_list('to_user_id', flat=True)
    accepted_to = FriendRequest.objects.filter(to_user=request.user, status="accepted").values_list('from_user_id', flat=True)
    connected_ids = list(accepted_from) + list(accepted_to)

    # Only connected users
    users = User.objects.filter(id__in=connected_ids).select_related("profiles")

    return render(request, "user_list.html", {"users": users})


@login_required
def random_chat(request):
    # Get all users except current one
    all_users = User.objects.exclude(id=request.user.id)

    # Get IDs of accepted connections
    accepted_from = FriendRequest.objects.filter(from_user=request.user, status="accepted").values_list('to_user_id', flat=True)
    accepted_to = FriendRequest.objects.filter(to_user=request.user, status="accepted").values_list('from_user_id', flat=True)
    connected_ids = list(accepted_from) + list(accepted_to)

    # Non-connected users
    not_connected_users = all_users.exclude(id__in=connected_ids)

    return render(request, "random_chat_list.html", {"suggested_users": not_connected_users})



def chat_messages(request, user_id):
    chat_user = User.objects.get(id=user_id)
    messages = Message.objects.filter(
        sender=request.user, receiver=chat_user
    ) | Message.objects.filter(
        sender=chat_user, receiver=request.user
    )
    messages = messages.order_by("timestamp")
    return render(request, "chat.html", {
        "messages": messages,
        "user_id": user_id,
        "chat_user": chat_user
    })


def send_message(request, user_id):
    if request.method == "POST":
        content = request.POST.get("text")
        msg = Message.objects.create(sender=request.user, receiver_id=user_id, content=content)
        return redirect("chat_messages", user_id=user_id)
    

def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "profile_page.html", {"profile_user": user})




