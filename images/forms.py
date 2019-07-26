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
        fields = ('file', )

    def save(self, pk, name, commit=True):
        print("save:" + str(pk))
        print("name:" + name.split('.')[0])
        instance = super(VideoForm, self).save(commit=False)
        instance.pin = Album.objects.get(pk=pk).pin
        instance.album = Album.objects.get(pk=pk)
        instance.title = name.split('.')[0]
        if commit:
            instance.save()
        return instance


class AlbumForm(BSModalForm):
    class Meta:
        model = Album
        fields = ['name', 'description']
    """
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop("organization", None)
        print(self.organization)
        super(PopRequestMixin, self).__init__(*args, **kwargs)
    """
    def save(self, commit=False):

        if not self.request.is_ajax():
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            instance.organization = User.objects.get(pk=self.request.user.pk)
            instance.save()
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)

        return instance
