from django import forms
from django.db.models.fields import EmailField, URLField
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.forms.widgets import ClearableFileInput, EmailInput, PasswordInput, RadioSelect, Select, TextInput, Textarea, URLInput, FileInput

from .models import *

# Default form for registering users, that inherits from django's UCrF
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','id':'username', 'aria-describedby':'usernameHelp'})
        self.fields['password1'].widget.attrs.update({'class':'form-control','id':'password1', 'aria-describedby':'password1Help'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','id':'password2','aria-describedby':'password2Help'})
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'first_name', 'last_name',
         'photo', 'amazon', 'twitter', 'facebook', 'instagram', 'youtube', 'bio']
        widgets = {
            'email':EmailInput(attrs={'class':'form-control', 'id':'email', 'aria-describedby':'emailHelp'}),
            'first_name':TextInput(attrs={'class':'form-control', 'id':'first_name',}),
            'last_name':TextInput(attrs={'class':'form-control','id':'last_name', 'aria-describedby':'nameHelp'}),
            'photo':FileInput(attrs={'class':'form-control','id':'photo', 'aria-describedby':'photoHelp'}),
            'bio':Textarea(attrs={'class':'form-control', 'id':'bio', 'aria-describedby':'bioHelp'}),
            'amazon':URLInput(attrs={'class':'form-control', 'id':'amazon', 'aria-describedby':'amazonHelp'}),
            'twitter':URLInput(attrs={'class':'form-control', 'id':'twitter', 'aria-describedby':'twitterHelp'}),
            'facebook':URLInput(attrs={'class':'form-control', 'id':'facebook', 'aria-describedby':'facebookHelp'}),
            'instagram':URLInput(attrs={'class':'form-control', 'id':'instagram', 'aria-describedby':'instagramHelp'}),
            'youtube':URLInput(attrs={'class':'form-control', 'id':'youtube', 'aria-describedby':'youtubeHelp'})
        }

# Form for creating (adding) scripts.
class CreateScriptForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['upload'].widget.attrs.update({'class':'form-control','id':'upload', 'aria-describedby':'uploadHelp'})
        self.fields['cover'].widget.attrs.update({'class':'form-control','id':'cover', 'aria-describedby':'coverHelp'})
    class Meta:
        model = Script
        exclude = ['user', 'created']
        widgets = {
            'title':TextInput(attrs={'class':'form-control', 'id':'title', 'aria-describedby':'titleHelp'}),
            'script_type':Select(attrs={'class':'form-select', 'id':'type', 'aria-describedby':'typeHelp' }),
            'category':Select(attrs={'class':'form-select', 'id':'category', 'aria-describedby':'categoryHelp'}),
            'summary':Textarea(attrs={'class':'form-control', 'id':'summary', 'aria-describedby':'summaryHelp'}),
        }

# Form for adding comments
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {"comment": Textarea(attrs={
            'class':'form-control',
            'rows':'2',
            'cols':'15',
            'placeholder':'Add Comment',
            'aria-describedby':'commentHelp',
            'id':'id_comment',
        })}

# Form for adding suggestions
class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ['suggestion']
        widgets = {"suggestion": Textarea(attrs={
            'class':'form-control',
            'rows':'2',
            'cols':'15',
            'placeholder':'Suggest some changes to author.',
            'aria-describedby':'suggestionHelp',
            'id':'id_suggestion',
        })}

# Form for editing profile, that inherits from django's UChF
class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name',
         'photo', 'amazon', 'twitter', 'facebook', 'instagram', 'youtube', 'bio']
        widgets = {
            'email':EmailInput(attrs={'class':'form-control', 'id':'email', 'aria-describedby':'emailHelp'}),
            'first_name':TextInput(attrs={'class':'form-control', 'id':'first_name',}),
            'last_name':TextInput(attrs={'class':'form-control','id':'last_name', 'aria-describedby':'nameHelp'}),
            'photo':FileInput(attrs={'class':'form-control','id':'photo', 'aria-describedby':'photoHelp'}),
            'bio':Textarea(attrs={'class':'form-control', 'id':'bio', 'aria-describedby':'bioHelp'}),
            'amazon':URLInput(attrs={'class':'form-control', 'id':'amazon', 'aria-describedby':'amazonHelp'}),
            'twitter':URLInput(attrs={'class':'form-control', 'id':'twitter', 'aria-describedby':'twitterHelp'}),
            'facebook':URLInput(attrs={'class':'form-control', 'id':'facebook', 'aria-describedby':'facebookHelp'}),
            'instagram':URLInput(attrs={'class':'form-control', 'id':'instagram', 'aria-describedby':'instagramHelp'}),
            'youtube':URLInput(attrs={'class':'form-control', 'id':'youtube', 'aria-describedby':'youtubeHelp'})
        }

# Form for changing passwords, that inherits from django's PCF
class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['old_password'].widget.attrs.update({'class':'form-control','id':'old_password', 'aria-describedby':'old_passwordHelp'})
        self.fields['new_password1'].widget.attrs.update({'class':'form-control','id':'new_password1', 'aria-describedby':'new_password1Help'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control','id':'new_password2','aria-describedby':'new_password2Help'})

# Adjusting the form for reseting passwords - entering email address
class ResetPasswordForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].widget.attrs.update({'class':'form-control','id':'email_reset', 'aria-describedby':'email_resetHelp'})
        
# Adjusting the form for reseting passwords - setting new password
class SetNewPassword(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fields['new_password1'].widget.attrs.update({'class':'form-control','id':'reset_password1', 'aria-describedby':'reset_password1Help'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control','id':'reset_password2','aria-describedby':'reset_password2Help'})

