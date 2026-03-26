from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
import uuid
from datetime import datetime






class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name= "profiles")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50 , blank=True)
    about = models.TextField(blank=True)
    profileimg_main = models.ImageField(upload_to="Profile_images/main/", default="blankimage.jpg",null=True, blank=True)
    profileimg_inner = models.ImageField(upload_to="Profile_images/inner/", default="blankimage.jpg",null=True, blank=True)
    friends = models.ManyToManyField(User,blank=True)


    phone_number = models.CharField(max_length=20, blank=True) 
    website = models.URLField(blank=True)

    # Visibility flags (default True = show everything) 
    show_email = models.BooleanField(default=True) 
    show_phone = models.BooleanField(default=True) 
    show_website = models.BooleanField(default=True)
    show_location = models.BooleanField(default=True) # <-- Add this
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_request', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_request', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField( max_length=10, choices=[("pending", "Pending"), ("accepted", "Accepted"), ("rejected", "Rejected")], default="pending" )

    class Meta:
        unique_together = ('from_user','to_user')
        ordering = ['created']

    def __str__(self):
        return f'{self.from_user} - {self.to_user}'
    



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.message}"



class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('article', 'Article'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='image')

    # Image posts
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)

    # Video posts
    video = models.FileField(upload_to='post_videos/', blank=True, null=True)

    # Article posts
    article_title = models.CharField(max_length=200, default="Untitled")
    article_body = models.TextField(default="No content")
    article_image = models.ImageField(upload_to='article_images/', blank=True, null=True)

    # Common fields
    caption = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(User, related_name="likeposts", blank=True)
    shares = models.ManyToManyField(User, related_name="shares", blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.post_type}'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='comment_likes')
    def __str__(self):
        return f"{self.user.username}'s comment on {self.post.user.username}'s post"
    
class Reply(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='reply_likes')

    def __str__(self):
        return f"{self.user.username}'s reply to {self.comment.user.username}'s comment"



    

    

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} liked {self.post.user.username}'s post"
    
class Reaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} reacted to {self.post.user.username}'s post"




    


class Education(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    school_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255)
    start_year = models.IntegerField(default=True)
    end_year = models.IntegerField(blank=True,null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}'s Education"
        else:
            return "Education (no user associated)"

    

class Experience(models.Model):
    EMPLOYMENT_TYPE_CHOICES =[
        ('full-time','full-time'),
        ('part-time','part-time'),
        ('Trainee','Trainee'),
        ('Experience','Experience'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    company_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    start_year = models.IntegerField(default=True)
    end_year = models.IntegerField(blank=True,null=True)
    description = models.TextField(max_length=255)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, null=True)
   

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}'s Experience"
        else:
            return "Experience (no user associated)"
    

class Skill(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    skill_name = models.CharField(max_length=255)
    level = models.CharField(
    max_length=255,
    choices=[
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advance', 'Advance'),
        ('Expert', 'Expert'),
    ]
)

    def __str_(self):
        return f"{self.user.username}'s skill in {self.skill_name}"
    

class Language(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    language_name = models.CharField(max_length=255)

    def __str_(self):
        return f"{self.user.username}'s language in {self.language_name}"
    
class Share(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform = models.CharField(max_length=20, choices=[
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('linkedin', 'LinkedIn'),
        ('whatsapp', 'Whatsapp'),
    ])
    message = models.CharField(max_length=255, default="")
    shared_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.content} shared on {self.platform}"


class About(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    description = models.TextField(blank=True,null=True)

    def __str__(self):
        if self.user is not None:
            return f"{self.user.username}'s About"
        else:
            return "About (no user associated)"



class Message(models.Model):
    STATUS_CHOICES = [
        ("sent", "Sent"),
        ("delivered", "Delivered"),
        ("seen", "Seen"),
    ]

    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="sent")

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.content[:20]}"


