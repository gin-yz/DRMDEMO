from django import forms

from apps.music.models import MusicComments, Music


class CommentsForm(forms.ModelForm):
    class Meta:
        model = MusicComments
        fields = ["music", "comments"]


class CommentsDeleteForm(forms.Form):
    comment_id = forms.IntegerField()


class receiveUploadSystemForm(forms.Form):
    purchase_bcId = forms.CharField(max_length=128)
    ipfshash = forms.CharField(max_length=64)

class modifyMusicInfoForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ["music_bcId","music_detail"]