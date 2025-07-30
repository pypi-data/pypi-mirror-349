import os

from django.db import OperationalError

from ...data.models import MetaFieldDomain, MetaFieldTool
import pandas as pd


def load_meta_frame():
    try:
        MetaFieldTool.objects.all().delete()
        MetaFieldDomain.objects.all().delete()
        project_root = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(project_root, 'meta_frame.xlsx')
        array = pd.read_excel(file_path, sheet_name='tool').to_dict("records")
        for row in array:
            row['saved'] = True
            MetaFieldTool.objects.create(**row)
        array = pd.read_excel(file_path, sheet_name='domain').to_dict("records")
        for row in array:
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



