from .models import Video, Album
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'album', 'file' )

class AlbumForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.ModelForm):
    class Meta:
        model = Album
        fields = ['name', 'description']

    def save(self, commit=True):
        if not self.request.is_ajax():
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            instance.organization = User.objects.get(pk=self.request.user.pk)
            instance.save()
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=True)

        return instance
