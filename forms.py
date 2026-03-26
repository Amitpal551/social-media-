from django import forms
from .models import Education,Profile,Experience,Skill,Language,Post,Comment,Like,Share,About,Reaction,Reply

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('school_name', 'field_of_study', 'degree', 'start_year', 'end_year')

    def clean_start_year(self):
        start_year = self.cleaned_data['start_year']
        if not start_year:
            raise forms.ValidationError('Start year is required')
        return start_year

    def clean_end_year(self):
        end_year = self.cleaned_data['end_year']
        if not end_year:
            raise forms.ValidationError('Please enter an end year')
        return end_year

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('skill_name', 'level')

class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('language_name',)
    def clean_language_name(self):
        language_name = self.cleaned_data['language_name']
        if not language_name:
            raise forms.ValidationError('Please Enter Your Language')
        return language_name
    
class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('description',)
        labels = {'description': 'Text'}
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Enter your text about yourself'}),
}



    
class ExperienceForm(forms.ModelForm):
    class Meta:
        model= Experience
        fields = ('company_name','job_title','start_year','end_year','description','employment_type')


    employment_type = forms.ChoiceField(choices=Experience.EMPLOYMENT_TYPE_CHOICES)


    def clean_start_year(self):
        start_year = self.cleaned_data['start_year']
        if not start_year:
            raise forms.ValidationError('Start year is required')
        return start_year

    def clean_end_year(self):
        end_year = self.cleaned_data['end_year']
        if not end_year:
            raise forms.ValidationError('Please enter an end year')
        return end_year


    

class ImagePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'image')

class VideoPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('caption', 'video')

class ArticlePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['article_title', 'article_body', 'article_image', 'caption']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['article_title'].required = True
        self.fields['article_body'].required = True



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_type',
            'image',
            'video',
            'article_title',
            'article_body',
            'article_image',
            'caption',
        ]





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('reply',)



class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ()

class ReactionForm(forms.ModelForm):
    class Meta:
        model = Reaction
        fields = ('emoji',)


class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ('platform', 'message')

from django import forms
from .models import Profile, About

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [ 'location', 'website','phone_number','show_phone','show_email', 'show_website', 'show_location']

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ('description',)


