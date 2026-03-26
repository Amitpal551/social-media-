from django.contrib import admin
from .models import Notification,FriendRequest, Profile, Post,Education,Experience,Skill,Language,Comment,Like,Share,About,Reaction,Reply,Message


# Register your models here.

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Skill)
admin.site.register(Share)
admin.site.register(Reaction)
admin.site.register(Message)
admin.site.register(Language)
admin.site.register(About)
admin.site.register(FriendRequest)
admin.site.register(Notification)




