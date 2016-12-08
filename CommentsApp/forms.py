from django import forms
class CommentForm(forms.Form):
    comment = forms.CharField(label='Text',widget=forms.Textarea, max_length=500)