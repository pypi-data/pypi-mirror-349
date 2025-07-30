from django.db.models import (ManyToOneRel, ForeignKey, ManyToManyRel, ManyToManyField, OneToOneField, CharField,
                              OneToOneRel, IntegerField, BooleanField, FloatField, FileField, JSONField, DateField,
                              TextField,DateTimeField, TimeField)

from .meta_frame import convert_meta_fields
from ..orm.meta import meta_props, meta_defaults
from ..models import Meta, MetaView, VModel, MetaField, VTree

from deepmerge import always_merger


def __save_model(model):
    model.save()
    model.sort = model.id
    model.saved = True
    model.save()



def load_view(entity, code, name, fields):
    meta = Meta.objects.filter(entity=entity).first()
    if meta is None:
        meta = Meta(entity=entity, name=name)
        __save_model(meta)
    view = MetaView.objects.filter(meta__entity=entity, code=code).first()
    if view is None:
        view = MetaView(meta=meta, code=code, view_name=code.upper())
        __save_model(view)
    if view.metafield_set.count() == 0:
        t, p = meta_props.get(entity, {}).get(code,('omit',[]))
        _fields = [f for f in fields if f['prop'] not in p] if t=='omit' else [f for f in fields if f['prop']  in p]
        defaults = meta_defaults.get(entity,{})
        for _field in _fields:
            prop = _field['prop']
            _field = always_merger.merge(_field,defaults.get(prop,{}))
        _fields.reverse()
        for f in _fields:
            f['view'] = view
            field = MetaField.objects.create(**f)
            __save_model(field)
    return view

def load_meta(view):
    _view = view.full
    _meta = _view['meta']
    fields = view.metafield_set.all().order_by('-sort')
    _fields = convert_meta_fields(fields,_meta['entity'])
    # _fields = [f.json for f in fields]
    clear_item(_view, 'meta_id', 'metafield', 'metafield_set', 'meta')
    _view['meta_name'] = _meta['name']
    _view['entity'] = _meta['entity']
    _view['fields'] = {}
    for _field in _fields:
        clear_item(_field, 'view_id')
        prop = _field['prop']
        _view['fields'][prop] = _field
    return _view



def clear_item(item, *keys):
    del item['saved']
    del item['sort']
    del item['create_time']
    del item['modify_time']
    for key in keys:
        del item[key]


def get_default_refer():
    return {
        "entity": None,
        "value": "name", "label": 'name', "display": "id",
        "strict": False, "remote": False, "multiple": False,
        "includes": {}, "excludes": {}, "root": 0, "isTree": False
    }


def get_refer(model, multiple = False):
    module, name = model.__module__, model.__name__
    entity = '%s.%s' % (module.replace('.models', '').split('.')[-1], name)
    return {
        "entity": entity,
        "value": "id", "label": 'name', "display": "id",
        "strict": False, "remote": False, "multiple": multiple,
        "includes": {}, "excludes": {}, "root": 0, "isTree": issubclass(model, VTree)
    }

def get_align(clazz):
    if clazz in [FloatField, IntegerField]:  #, ManyToManyRel, ManyToManyField, ManyToOneRel
        return 'right'
    elif clazz in [BooleanField,FileField,JSONField,DateField,DateTimeField,TimeField]:
        return 'center'
    return 'left'

def get_default_format():
    return {
        # 文本
        "maxlength": 0,
        "type": 'text',

        # 数值
        "min": None,
        "max": None,
        "step": 1,
        "precision": None,
        "step_strictly": False,

        # 日期
        "frequency": "date",

        # 文件
        "maximum": 5,
        "width": 800,
        "height": 0,
        "accept": [],
        "file_name_field":None,
        "locked": False,

        #集合
        "set": {}
    }



def get_format(field):
    clazz = type(field)
    _format = get_default_format()
    if clazz == CharField:
        _format['maxlength'] = field.max_length
    if clazz == TextField:
        _format['type'] =  "textarea"
    elif clazz == DateTimeField:
        _format['frequency'] = "datetime"
    elif clazz == IntegerField:
        _format['precision'] = 0
        _format['step_strictly'] = True
    elif clazz == FileField:
        pass
    return _format

def get_field_column_width(field,clazz):
    if clazz in [BooleanField, FileField, JSONField]:
        return 100
    elif clazz in [ DateField, DateTimeField, TimeField]:
        return 120
    return 0



def load_meta_field(field, isTree):
    clazz = type(field)
    if clazz in [ManyToOneRel, ManyToManyField, ManyToManyRel]:
        prop = field.name
        domain = clazz.__name__
        model: VModel= field.related_model
        label = model._meta.verbose_name
        refer = get_refer(model, True)
    elif clazz in [ForeignKey]:
        prop = field.name + "_id"
        domain = field.get_internal_type()
        model: VModel = field.related_model
        label = field.verbose_name
        refer = get_refer(model)
    elif clazz in [OneToOneRel, OneToOneField]:
        prop = field.name + "_id"
        domain = clazz.__name__
        model: VModel = field.related_model
        label = model._meta.verbose_name
        refer = get_refer(model)
    else:
        prop = field.name
        domain = field.get_internal_type()
        label = field.verbose_name
        refer = get_default_refer()
    not_null = not field.null
    align = get_align(clazz)
    _format = get_format(field)
    column_width = get_field_column_width(field,clazz)
    _field =  {
        "prop": prop,
        "label":label,
        "name":label,
        "domain":domain,
        "refer":refer,
        "format":_format,
        "not_null":not_null,
        "align":align,
        "column_width":column_width
    }

    if isTree:
        if prop in ['pid','isLeaf']:
            _field['hide_on_table'] = True
            _field['hide_on_form'] = True
            _field['hide_on_form_branch'] = True
            _field['hide_on_form_leaf'] = True
        elif prop in ['icon']:
            _field['tool'] = 'icon'
    return _field