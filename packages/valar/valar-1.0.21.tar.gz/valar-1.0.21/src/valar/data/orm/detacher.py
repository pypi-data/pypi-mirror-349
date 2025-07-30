from django.db.models import (ManyToOneRel, ForeignKey, ManyToManyRel, ManyToManyField, OneToOneField, CharField,
                              OneToOneRel, IntegerField, BooleanField, FloatField, FileField, JSONField, DateField,
                              DateTimeField, TimeField, QuerySet)

from ..models import VModel


def detach_props(item, fields):
    keys = [field['prop'] for field in fields if
            field['domain'] in ['ManyToOneRel', 'ManyToManyField', 'ManyToManyRel', 'OneToOneRel', 'OneToOneField']]
    _item = {}
    for key in keys:
        value = item.get(key)
        if value is not None:
            _item[key] = value
            del item[key]
    return _item

def save_detached(bean, _item, model_fields ):
    for prop in _item:
        value = _item[prop]
        field = model_fields.get(prop)
        clazz = type(field)
        if clazz == ManyToManyField:
            m2m = getattr(bean, prop)
            m2m.clear()
            m2m.add(*value)
        elif clazz == ManyToOneRel:
            getattr(bean, field.get_accessor_name()).clear()
            remote_model: VModel = field.related_model
            new_set: QuerySet = remote_model.objects.filter(id__in=value)
            remote_field: ForeignKey = field.remote_field
            k = remote_field.get_attname()
            new_set.update(**{k: bean.id})
        elif clazz == ManyToManyRel:
            getattr(bean, field.get_accessor_name()).clear()
            remote_model: VModel = field.related_model
            remote_items: QuerySet = remote_model.objects.filter(id__in=value)
            remote_field: ManyToManyField = field.remote_field
            remote_field_prop = remote_field.get_attname()
            for _bean in remote_items:
                bean_set = getattr(_bean, remote_field_prop)
                bean_set.add(bean)
        elif clazz == OneToOneRel:
            remote_model: VModel = field.related_model
            remote_field: OneToOneField = field.remote_field
            remote_field_prop = remote_field.get_attname()
            _bean = remote_model.objects.get(id=value)
            __bean = remote_model.objects.filter(**{remote_field_prop: bean.id}).first()
            if __bean:
                setattr(__bean, remote_field_prop, None)
                __bean.save()
            setattr(_bean, remote_field_prop, bean.id)
            _bean.save()
        elif clazz == OneToOneField:
            __bean = field.model.objects.filter(**{prop: value}).first()
            if __bean:
                setattr(__bean, prop, None)
                __bean.save()
            setattr(bean, prop, value)
            bean.save()