import django_tables2 as tables
from .models import Album
from django.contrib.auth.mixins import LoginRequiredMixin
import inspect
#<a href="{% url some_url_edit record.pk %}" class="tbl_icon edit">Edit</a>
TEMPLATE = '''
    <div class="dropdown show">
    <button class="btn btn-light" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
        <i class="fas fa-ellipsis-v"></i>
    </button>

      <div class="dropdown-menu" aria-labelledby="dropdownMenuLink">
        <a class="dropdown-item" href="#" id="viewAlbum" data-toggle="collapse">View Album</a>
        <a class="update-album dropdown-item" data-toggle="modal" data-id="{% url 'update_album' record.pk %}">Edit Album</a>
        <a class="delete-album dropdown-item" data-toggle="modal" data-id="{% url 'delete_album' record.pk %}">Delete Album</a>
      </div>
    </div>
'''

UPLOAD_BUTTON = '''
<a class="btn btn-light js-upload-videos" data-id="{{ record.pk }}">
    <i class="fas fa-upload"></i>
</a>
<input id="fileupload{{ record.pk }}" type="file" accept="video/*" name="file" multiple
   style="display: none;"
   data-url="{% url 'basic_upload' record.pk %}"
   data-form-data='{"csrfmiddlewaretoken": "{{ csrf_token }}"}'>
'''

class AlbumTable(LoginRequiredMixin, tables.Table):
    actions = tables.TemplateColumn(TEMPLATE, orderable=False)
    upload = tables.TemplateColumn(UPLOAD_BUTTON, orderable=False)
    selection = tables.CheckBoxColumn(accessor='pk', attrs = { "th__input":
                                        {"onclick": "toggle(this)"}}, orderable=False)

    def __init__(self, *args, _overriden_value="",**kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Album
        template_name = 'django_tables2/bootstrap.html'
        sequence = ('selection', 'name', 'description', 'pin', 'status', 'model_status', 'upload', 'actions')
        exclude = ('id', 'organization',)
        row_attrs = {
            #'data-toggle': 'collapse',
            'id': lambda record: "row" + str(record.pk),
            #'class':'accordion-toggle',
        }
        attrs = {
            'id': 'albumTable',
            'class':'table table-hover',
            'style':'border-collapse:collapse;'
        }
