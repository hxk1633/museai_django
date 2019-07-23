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
        <a class="dropdown-item" id="view">View Album</a>
        <a class="update-album dropdown-item" data-toggle="modal" data-id="{% url 'update_album' record.pk %}">Edit Album</a>
        <a class="delete-album dropdown-item" data-toggle="modal" data-id="{% url 'delete_album' record.pk %}">Delete Album</a>
      </div>
    </div>

'''

class AlbumTable(LoginRequiredMixin, tables.Table):
    actions = tables.TemplateColumn(TEMPLATE, orderable=False)
    selection = tables.CheckBoxColumn(accessor='pk', attrs = { "th__input":
                                        {"onclick": "toggle(this)"}}, orderable=False)

    def __init__(self, *args, _overriden_value="",**kwargs):
        super().__init__(*args, **kwargs)
        self.base_columns['actions'].verbose_name = _overriden_value


    class Meta:
        model = Album
        template_name = 'django_tables2/bootstrap.html'
        sequence = ('selection', 'name', 'description', 'pin', 'status', 'model_status', 'actions')
        exclude = ('id', 'organization',)
        row_attrs = {
            'data-toggle': 'collapse',
            'data-target': lambda record: "#album" + str(record.pk),
            'class':'accordion-toggle',
            'id': lambda record: record.pk
        }
        attrs = {
            'id': 'albumTable',
            'class':'table table-hover',
            'style':'border-collapse:collapse;'
        }
