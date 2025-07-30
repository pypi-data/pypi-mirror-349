import datetime
from django.apps import apps
from django.core.paginator import Paginator
from django.db.models import Manager, QuerySet, FileField

from .meta_frame import load_meta_frame
from ..file import minio_remove_path
from ..orm.detacher import detach_props, save_detached
from ..orm.meta_loader import load_meta, load_view, load_meta_field
from ..models import VModel, VTree
from ..query import Query


load_meta_frame()

def load_model(entity=None):
    mapping = {}
    for mod in apps.get_models():
        if issubclass(mod, VModel):
            path, name = mod.__module__, mod.__name__
            __old = 'src.valar.' if path.startswith('src') else 'valar.'
            app = path.replace('.models', '').replace(__old,'')
            key = '%s.%s' % (app, name)
            verbose_name = mod._meta.verbose_name
            mapping[key] = [mod, verbose_name]
    return mapping.get(entity) if entity else mapping




class OrmDao:
    def __init__(self, entity):
        self.entity = entity
        param = load_model(entity)
        if param is None:
            raise Exception('no entity named %s' % entity)
        self.model = param[0]
        self.isTree = issubclass(self.model, VTree)
        self.name: str = param[1]
        self.manager: Manager = self.model.objects
        self.meta_fields = {}
        self.model_fields = {}
        for field in self.model._meta.get_fields():
            _field = load_meta_field(field, self.isTree)
            prop = _field['prop']
            self.model_fields[prop] = field
            self.meta_fields[prop] = _field


    def tree(self, query: Query, root_id = 0):
        all_set, _ = self.find_many(Query())
        includes, excludes = query.orm_conditions()
        if not len(includes) + len(excludes) + root_id:
            return all_set
        values = all_set.values('id','pid')
        mapping = {item['id']: item['pid'] for item in values}
        results, _ = self.find_many(query)
        id_set = {root_id}
        for item in results:
            _id = item.id
            route = []
            while _id is not None:
                route.append(_id)
                _id = mapping.get(_id)
            if root_id in route:
                id_set.update(route)
        return all_set.filter(id__in=id_set).order_by('-sort')

    def __check_remove_file__(self, query_set, template:dict = None):
        props = [key for key in self.model_fields if type(self.model_fields[key]) == FileField]
        keys = [ key for key in props if template.get(key, 1) is None] if template else  props
        if len(keys):
            values = query_set.values(*props)
            for row in values:
                for path in row.values():
                    if path:
                        print(path)
                        minio_remove_path(path)



    def save_one(self, item):
        _item = detach_props(item, self.meta_fields.values())
        _id = item.get('id',0)
        query_set = self.manager.filter(id=_id)
        if len(query_set):
            del item['id']
            item['modify_time'] = datetime.datetime.now()
            self.__check_remove_file__(query_set,item)
            query_set.update(**item)
            bean = query_set.first()
        else:
            bean = self.manager.create(**item)
            bean.sort = bean.id
            bean.save()
        save_detached(bean, _item, self.model_fields)
        return bean

    def update_many(self, query: Query, template):
        query_set, total = self.find_many(query)
        query_set.update(**template)

    def delete_one(self, _id):
        query_set = self.manager.filter(id=_id)
        self.__check_remove_file__(query_set)
        query_set.delete()

    def delete_many(self, query: Query):
        query_set, total = self.find_many(query)
        self.__check_remove_file__(query_set)
        query_set.delete()

    def find_one(self, _id):
        return self.manager.filter(id=_id).first()

    def find_many(self, query: Query, size=0, page=1):
        includes, excludes = query.orm_conditions()
        query_set = self.manager.filter(includes).exclude(excludes).order_by(*query.orm_orders())
        total = query_set.count()
        if size:
            paginator = Paginator(query_set, size)
            query_set = paginator.page(page).object_list
        return query_set, total


    def meta(self, code:str = 'default'):
        omit = [ 'id', 'saved', 'sort', 'create_time', 'modify_time']
        fields = [ self.meta_fields[prop] for prop in self.meta_fields if prop not in omit]
        view =  load_view(self.entity, code, self.name, fields)
        _view = load_meta(view)
        _view['isTree'] = self.isTree
        return _view



