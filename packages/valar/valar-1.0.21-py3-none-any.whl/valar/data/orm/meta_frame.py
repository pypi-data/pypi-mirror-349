
from django.db import OperationalError

from ...data.models import MetaFieldDomain, MetaFieldTool


def load_meta_frame():
    try:
        MetaFieldTool.objects.all().delete()
        MetaFieldDomain.objects.all().delete()
        for row in meta_field_tool:
            row['saved'] = True
            MetaFieldTool.objects.create(**row)
        for row in meta_field_domain:
            row['saved'] = True
            tools = row.get('tools', '').split(';')
            del row['tools']
            item = MetaFieldDomain.objects.create(**row)
            for tk in tools:
                item.tools.add(tk)
    except OperationalError as e:
        print('initialization')


def convert_meta_fields(fields, entity):
    values = MetaFieldDomain.objects.all().values('name', 'default__code', 'align')
    mapping = {vs['name']: {
        "tool": vs['default__code'],
        "align": vs['align']
    } for vs in values}
    array = []
    for field in fields:
        node = mapping[field.domain]
        _field = field.json
        if field.tool == 'default':
            _field['tool'] = node['tool']
        _field['align'] = node['align']
        _field['entity'] = entity
        array.append(_field)
    return array



meta_field_tool = [
    {'id': 2, 'sort': 32, 'pid': 7, 'isLeaf': True, 'name': '输入框', 'code': 'text'},
    {'id': 3, 'sort': 17, 'pid': 0, 'isLeaf': False, 'name': 'SPEC', 'code': '特殊工具集'},
    {'id': 5, 'sort': 22, 'pid': 0, 'isLeaf': False, 'name': 'DATE', 'code': '日期时间工具集'},
    {'id': 6, 'sort': 21, 'pid': 8, 'isLeaf': True, 'name': '数字输入', 'code': 'number'},
    {'id': 7, 'sort': 36, 'pid': 0, 'isLeaf': False, 'name': 'TEXT', 'code': '文本工具集'},
    {'id': 8, 'sort': 26, 'pid': 0, 'isLeaf': False, 'name': 'NUMB', 'code': '数字工具集'},
    {'id': 9, 'sort': 10, 'pid': 0, 'isLeaf': False, 'name': 'FILE', 'code': '文件工具集'},
    {'id': 10, 'sort': 27, 'pid': 0, 'isLeaf': False, 'name': 'BOOL', 'code': '逻辑工具集'},
    {'id': 11, 'sort': 31, 'pid': 0, 'isLeaf': False, 'name': 'LIST', 'code': '列表工具集'},
    {'id': 12, 'sort': 8, 'pid': 3, 'isLeaf': True, 'name': '对象', 'code': 'object'},
    {'id': 13, 'sort': 5, 'pid': 9, 'isLeaf': True, 'name': '图片上传', 'code': 'image'},
    {'id': 14, 'sort': 2, 'pid': 9, 'isLeaf': True, 'name': '文件上传', 'code': 'file'},
    {'id': 15, 'sort': 13, 'pid': 9, 'isLeaf': True, 'name': '富文本', 'code': 'rich'},
    {'id': 17, 'sort': 11, 'pid': 10, 'isLeaf': True, 'name': '开关', 'code': 'switch'},
    {'id': 18, 'sort': 7, 'pid': 3, 'isLeaf': True, 'name': '元数据', 'code': 'meta'},
    {'id': 19, 'sort': 9, 'pid': 7, 'isLeaf': True, 'name': '颜色选择', 'code': 'color'},
    {'id': 20, 'sort': 14, 'pid': 11, 'isLeaf': True, 'name': '穿梭框', 'code': 'transfer'},
    {'id': 21, 'sort': 16, 'pid': 7, 'isLeaf': True, 'name': '自动填充', 'code': 'auto'},
    {'id': 22, 'sort': 35, 'pid': 5, 'isLeaf': True, 'name': '日期选择', 'code': 'date'},
    {'id': 23, 'sort': 12, 'pid': 10, 'isLeaf': True, 'name': '逻辑选择', 'code': 'boolean'},
    {'id': 24, 'sort': 24, 'pid': 11, 'isLeaf': True, 'name': '列表选择', 'code': 'select'},
    {'id': 25, 'sort': 15, 'pid': 11, 'isLeaf': True, 'name': '树形选择', 'code': 'tree'},
    {'id': 26, 'sort': 23, 'pid': 11, 'isLeaf': True, 'name': '及联选择', 'code': 'cascade'},
    {'id': 27, 'sort': 39, 'pid': 0, 'isLeaf': True, 'name': '默认', 'code': 'default'},
    {'id': 28, 'sort': 25, 'pid': 7, 'isLeaf': True, 'name': '图标', 'code': 'icon'},
    {'id': 31, 'sort': 6, 'pid': 0, 'isLeaf': True, 'name': '无', 'code': 'none'},
    {'id': 32, 'sort': 30, 'pid': 7, 'isLeaf': True, 'name': '文本框', 'code': 'textarea'},
    {'id': 33, 'sort': 18, 'pid': 36, 'isLeaf': True, 'name': '时间区间', 'code': 'timerange'},
    {'id': 35, 'sort': 33, 'pid': 5, 'isLeaf': True, 'name': '时间选择', 'code': 'time'},
    {'id': 36, 'sort': 20, 'pid': 0, 'isLeaf': False, 'name': 'RANGE', 'code': '区间工具集'},
    {'id': 37, 'sort': 38, 'pid': 36, 'isLeaf': True, 'name': '日期区间', 'code': 'daterange'},
    {'id': 39, 'sort': 3, 'pid': 36, 'isLeaf': True, 'name': '多日期', 'code': 'dates'},
    {'id': 54, 'sort': 54, 'pid': 7, 'isLeaf': True, 'name': '集合', 'code': 'set'}
]

meta_field_domain = [
    {'id': 12, 'sort': 22, 'name': 'CharField', 'default_id': 2, 'align': 'left', 'tools': '2;6;18;19;21;22;24;25;26;27;28;31;32;33;37;39;54'},
    {'id': 11, 'sort': 21, 'name': 'TextField', 'default_id': 32, 'align': 'left', 'tools': '2;27;31;32'},
    {'id': 13, 'sort': 20, 'name': 'BooleanField', 'default_id': 17, 'align': 'center', 'tools': '17;23;27;31'},
    {'id': 9, 'sort': 18, 'name': 'IntegerField', 'default_id': 6, 'align': 'right', 'tools': '6;27;31'},
    {'id': 8, 'sort': 16, 'name': 'FloatField', 'default_id': 6, 'align': 'right', 'tools': '6;27;31'},
    {'id': 4, 'sort': 15, 'name': 'ForeignKey', 'default_id': 24, 'align': 'left', 'tools': '24;25;26;27;31'},
    {'id': 2, 'sort': 13, 'name': 'ManyToOneRel', 'default_id': 24, 'align': 'center', 'tools': '20;24;25;26;27;31'},
    {'id': 1, 'sort': 12, 'name': 'ManyToManyField', 'default_id': 24, 'align': 'center', 'tools': '20;24;25;26;27;31'},
    {'id': 22, 'sort': 11, 'name': 'ManyToManyRel', 'default_id': 24, 'align': 'center', 'tools': '20;24;25;26;27;31'},
    {'id': 5, 'sort': 10, 'name': 'OneToOneRel', 'default_id': 31, 'align': 'left', 'tools': '27;31'},
    {'id': 21, 'sort': 9, 'name': 'OneToOneField', 'default_id': 31, 'align': 'left', 'tools': '27;31'},
    {'id': 6, 'sort': 8, 'name': 'DateField', 'default_id': 22, 'align': 'center', 'tools': '22;27;31'},
    {'id': 20, 'sort': 7, 'name': 'TimeField', 'default_id': 35, 'align': 'center', 'tools': '27;31;35'},
    {'id': 7, 'sort': 6, 'name': 'DateTimeField', 'default_id': 22, 'align': 'center', 'tools': '22;27;31'},
    {'id': 3, 'sort': 5, 'name': 'JSONField', 'default_id': 12, 'align': 'center', 'tools': '12;27;31'},
    {'id': 15, 'sort': 4, 'name': 'FileField', 'default_id': 14, 'align': 'center', 'tools': '13;14;15;27;31'},
    {'id': 16, 'sort': 3, 'name': 'BigAutoField', 'default_id': 31, 'align': 'right', 'tools': '27;31'},
    {'id': 18, 'sort': 2, 'name': 'UUIDField', 'default_id': 31, 'align': 'left', 'tools': '27;31'},
    {'id': 10, 'sort': 1, 'name': 'Custom', 'default_id': 31, 'align': 'left', 'tools': '27;31'}
]
