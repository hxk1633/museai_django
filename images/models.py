from django.db import models
from io import BytesIO
from django.db.models import F
from ffmpy import FFmpeg
from django.utils.crypto import get_random_string
import os
import sys
import base64
import uuid
import zipfile
from celery import Celery
import json
import images.make_json_serializable
from functools import partial
from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.urls import reverse_lazy

MODEL_STATUS = [
    ('s','Not trained'),
    ('t', 'Training'),
    ('c', 'Created'),
]

ALBUM_STATUS = [
    ('o', 'Open'),
    ('c', 'Closed'),
]

def new_pin(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.pin = get_random_string(length=6).upper()
        print("Creating an album")
    else:
        print("Updating an album")

def file_cleanup(sender, instance, **kwargs):
    """
    File cleanup callback used to emulate the old delete
    behavior using signals. Initially django deleted linked
    files when an object containing a File/ImageField was deleted.

    Usage:
    >>> from django.db.models.signals import post_delete
    >>> post_delete.connect(file_cleanup, sender=MyModel, dispatch_uid="mymodel.file_cleanup")
    """
    if isinstance(instance, Video):
        try:
            print("instance:" + str(instance))
            path = instance.getFilePath()
            os.remove(path)
            print(instance.getAlbumName())
            print(instance.getFileName())
            basePath = "media/albums/" + instance.getAlbumName() + "/data/images/"
            dirPath = "media/albums/" + instance.getAlbumName() + "/data/images/" + instance.getFileName()
            fileList = os.listdir(dirPath)
            for fileName in fileList:
                os.remove(dirPath+"/"+fileName)
            os.remove(basePath + instance.getFileName() + ".zip")
            os.rmdir(dirPath)
        except:
            pass
    elif isinstance(instance, Album):
        try:
            os.system("sudo rm -R " + "media/albums/" + instance.name + "/data/*")
            os.rmdir("media/albums/" + instance.name + "/data/")
            os.rmdir("media/albums/" + instance.name + "/")
        except:
            pass



def zip_folder(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(parent_folder + '\\',
                                                      '')
                zip_file.write(absolute_path, relative_path)
    except IOError as message:
        print(message)
        sys.exit(1)
    except OSError as message:
        print(message)
        sys.exit(1)
    except zipfile.BadZipfile as message:
        print(message)
        sys.exit(1)
    finally:
        zip_file.close()

def convertVideo(video):
    #print(video.getFileName())
    os.mkdir("media/albums/" + video.getAlbumName() + "/data/images/" + video.getFileName())
    #convert = FFmpeg(inputs={"media/videos/" + video.getFileName() + ".MOV": None}, outputs={"media/videos/" + video.getFileName() + ".mp4": None})
    ff = FFmpeg(inputs={"media/videos/" + video.getFileName() + ".mp4": None}, outputs={"media/albums/" + video.getAlbumName() + "/data/images/" + video.getFileName() + "/" + video.getFileName() + "%d.jpg": ['-vf', 'fps=30']})
    #convert.run()
    ff.run()
    zip_folder("media/albums/"+video.getAlbumName()+"/data/images/"+ video.getFileName(), "media/albums/" +video.getAlbumName()+"/data/images/"+video.getFileName()+".zip")

def update_filename(instance, filename):
    name = instance.title + ".mp4"
    return os.path.join("videos/", name)

# Create your models here.
class Album(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    pin = models.CharField(max_length=6)
    status = models.CharField(max_length=1, choices=ALBUM_STATUS, default='o')
    model_status = models.CharField(max_length=1, choices=MODEL_STATUS, default='s')
    id = models.AutoField(primary_key=True, auto_created=True)
    organization = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy('albums')

    def save(self, *args, **kwargs):
        #self.pin = get_random_string(length=6).upper()
        try:
            os.mkdir("media/albums/" + self.name)
            os.mkdir("media/albums/" + self.name + "/data/")
            os.mkdir("media/albums/" + self.name + "/data/images/")
        except:
            pass
        super(Album, self).save(*args, **kwargs)


    def to_json(self):  # New special method.
        return '{"name": "%s", "description": "%s", "pin": "%s", "status": "%s", "model_status": "%s"}' % (self.name, self.description, self.pin, self.status, self.model_status)

    def __str__(self):
        return self.name

class TFModel(models.Model):
    name = models.CharField(max_length=50)
    videos = models.IntegerField(max_length=5, editable=False, default=0)
    album_model = models.ForeignKey(Album, on_delete=models.CASCADE, default="", null=True)

    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=50)
    file = models.FileField(upload_to=update_filename)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, default="")
    pin = models.CharField(max_length=6)
    id = models.AutoField(primary_key=True, auto_created=True)

    def getFilePath(self):
        return self.file.path

    def getFileName(self):
        return self.file.name.split("/")[-1].split(".")[0]

    def getImages(self):
        name = getFileName()
        return "media/albums/" + name + ".zip"

    def getAlbumName(self):
        return self.album.name

    def save(self, *args, **kwargs):
        print("Converting video")
        self.album.model_status = 's'
        super(Video, self).save(*args, **kwargs)
        print(self.pin)
        convertVideo(self)
        self.album.save()
        print("Conversion successful")

    """
    @classmethod
    def create(cls, title, file, pin):
        album = Album.objects.get(pin=pin)
        video = cls(title=title, file=file, album=album)
        return video
    """

    def __str__(self):
        return self.title

post_delete.connect(file_cleanup, sender=Video, dispatch_uid="video.file_cleanup")
post_delete.connect(file_cleanup, sender=Album, dispatch_uid="album.file_cleanup")
pre_save.connect(new_pin, sender=Album, dispatch_uid="album.new_pin")
