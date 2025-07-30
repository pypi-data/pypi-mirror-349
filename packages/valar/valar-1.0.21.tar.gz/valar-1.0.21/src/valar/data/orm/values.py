from django.db.models import (ManyToOneRel,  ManyToManyRel, OneToOneField, CharField,ManyToManyField,
                              OneToOneRel, IntegerField, BooleanField, FloatField, FileField, JSONField, DateField,
                              DateTimeField, TimeField, TextField, QuerySet)
from django.db.models.fields.related import ForeignKey

from ..models import VModel, MetaField


def get_props(model:VModel, code):

    simple_props,  referred_fields, date_props = [], {}, {}
    fields = model._meta.get_fields()
    for field in fields:
        clazz = type(field)
        prop = field.name
        if clazz in [ForeignKey,ManyToOneRel,
                     ManyToManyRel,ManyToManyField,
                     OneToOneRel, OneToOneField]:
            referred_fields[prop] = {
                'value': 'id', 'label': 'name', 'display': 'id',
                'field': field
            }
        else:
            simple_props.append(prop)
        if clazz in [ForeignKey, OneToOneField, OneToOneRel]:
            simple_props.append(prop)
        if clazz in [DateField, DateTimeField]:
            date_props[prop] = clazz

    module, name = model.__module__, model.__name__
    entity = '%s.%s' % (module.replace('.models', '').split('.')[-1], name)
    if code:
        field_set = MetaField.objects.filter(view__code=code, view__meta__entity=entity)
        customs = field_set.filter(domain='Custom').values('prop')
        for row in customs:
            simple_props.append(row['prop'])
        refers =field_set.filter(prop__in=referred_fields.keys()).values('prop','refer__value','refer__label','refer__display')
        for row in refers:
            prop, value, label, display = row['prop'], row['refer__value'], row['refer__label'], row['refer__display']
            referred_fields[prop]['value'] = value
            referred_fields[prop]['label'] = label
            referred_fields[prop]['display'] = display
    return simple_props, referred_fields, date_props


def __get_ref_keys__(related_model):
    """新增功能"""
    return [f.name for f in related_model._meta.get_fields()
      if type(f) not in [ManyToManyField, ManyToOneRel, ManyToManyRel, ForeignKey, OneToOneField, OneToOneRel]
      and f.name not in ['create_time', 'modify_time', 'saved', 'sort']
    ]

def to_dict(query_set: QuerySet, code=None):
    model = query_set.model
    simple_props, referred_fields, date_props = get_props(model, code)
    values = query_set.values(*[*simple_props]) if len(query_set) else []
    results = list(values)
    pks = []
    for row in results:
        pks.append(row['id'])
        for prop in date_props:
            formating = '%Y-%m-%d' if date_props[prop] == DateField else '%Y-%m-%d %H:%M:%S'
            val = row[prop]
            row[prop] =val.strftime(formating) if val else val
    for prop in referred_fields:
        _field = referred_fields[prop]
        value, label, display, field = _field['value'], _field['label'], _field['display'], _field['field']
        clazz = type(field)
        keys = {'id', value, display, label}
        if clazz in [ForeignKey, OneToOneField, OneToOneRel]:
            related_model = field.related_model
            __keys = __get_ref_keys__(related_model)
            related_pks = set([row.get(prop) for row in results if row.get(prop)])
            related_items = related_model.objects.filter(id__in=related_pks).values(*__keys)
            mapping = {item['id']: item  for item in related_items}
            for row in results:
                value = row.get(prop)
                if value:
                    row[prop] = mapping[value]
                    row[f'{prop}_id'] = value
        elif clazz in [ ManyToManyField, ManyToOneRel, ManyToManyRel]:
            _prop = f'{prop}__id'
            linkage = model.objects.filter(id__in=pks).exclude(**{f'{_prop}__isnull':True}).values('id',_prop)
            row_mapping = {}
            _pks = set()
            for link in linkage:
                _id, _pk = link['id'], link[_prop]
                _pks.add(_pk)
                array = row_mapping.get(_id,[])
                array.append(_pk)
                row_mapping[_id] = array
            related_model = field.related_model
            __keys = __get_ref_keys__(related_model)
            related_items = related_model.objects.filter(id__in=_pks).values(*__keys)
            mapping = {item['id']: item  for item in related_items}
            for row in results:
                _id = row.get('id')
                __ids = row_mapping.get(_id, [])
                __set = [ mapping[__id] for __id in __ids]
                row[prop] = __ids
                row[f'{prop}_set'] = __set
    return results