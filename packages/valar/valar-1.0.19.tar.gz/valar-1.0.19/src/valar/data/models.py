from django.db import models
from django.db.models.fields.files import FieldFile



class VModel(models.Model):
    objects = models.Manager()
    sort = models.BigIntegerField(null=True, verbose_name='序号')
    name = models.CharField(max_length=50, null=True)
    create_time = models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')
    modify_time = models.DateTimeField(auto_now=True, null=True, verbose_name='修改时间')
    saved = models.BooleanField(default=False)

    class Meta:
        abstract = True

    @property
    def mapping(self):
        mapping = {}
        for field in self._meta.get_fields():
            prop = field.name
            domain = type(field).__name__
            mapping[prop] = {'prop': prop, 'domain': domain, 'field': field}
        return mapping

    """
        只序列化基础字段：能用value_from_object直接取出的字段。与values等价
    """

    def __str__(self):
        return str(self.json)

    @property
    def json(self):
        mapping = self.mapping
        excludes = ['ManyToOneRel', 'OneToOneRel', 'ManyToManyRel', 'ManyToManyField', 'UUIDField']
        mapping = {prop: mapping[prop] for prop in mapping if mapping[prop]['domain'] not in excludes}
        data = {}
        for prop in mapping:
            field = mapping[prop]['field']
            domain = mapping[prop]['domain']
            value = field.value_from_object(self)
            if domain in ['ForeignKey', 'OneToOneField']:
                prop = prop + '_id'
            elif domain in ['DateField']:
                value = value.strftime('%Y-%m-%d') if value else None
            elif domain in ['DateTimeField']:
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            elif domain in ['FileField']:
                file: FieldFile = value
                value = file.name
            # elif domain in ['BigAutoField']:
            #     value = str(value)
            data[prop] = value
        return data

    @property
    def full(self):
        data = self.json
        mapping = self.mapping
        excludes = ['ManyToManyField', 'ManyToManyRel', 'ForeignKey', 'ManyToOneRel', 'OneToOneField', 'OneToOneRel']
        mapping = {prop: mapping[prop] for prop in mapping if mapping[prop]['domain'] in excludes}
        for prop in mapping:
            field = mapping[prop]['field']
            domain = mapping[prop]['domain']
            if domain in ['ForeignKey', 'OneToOneField', 'OneToOneRel']:
                if hasattr(self, prop):
                    bean: VModel = getattr(self, prop)
                    data[prop] = bean.json if bean else None
                    data['%s_id'%prop] = bean.id if bean else None
            elif domain in ['ManyToManyField', 'ManyToManyRel', 'ManyToOneRel']:
                accessor = prop if domain == 'ManyToManyField' else field.get_accessor_name()
                try:
                    _set = getattr(self, accessor).all().order_by('sort')
                    data[prop] = [item.id for item in _set]
                    data[f'{prop}_set'] = [item.json for item in _set]
                except Exception as e:
                    print(e)
                    pass
        return data


class VTree(VModel):
    pid = models.IntegerField(null=False, default=0, verbose_name='父节点')
    isLeaf = models.BooleanField( default=False, verbose_name='叶子节点')
    icon = models.CharField(max_length=255, null=True, verbose_name='图标')
    class Meta:
        abstract = True


class Meta(VModel):
    entity = models.CharField(max_length=100, verbose_name='数据源', null=True, unique=True)
    name = models.CharField(max_length=50, verbose_name='实体别名', null=True)

    class Meta:
        verbose_name = '数据实体'
        # unique_together = ('domain', 'entity')


class MetaView(VModel):
    meta = models.ForeignKey('Meta', on_delete=models.CASCADE, verbose_name='元数据')

    code = models.CharField(max_length=50, verbose_name='类视图', default='default ')
    view_name = models.CharField(max_length=50, verbose_name='视图名称', null=True)

    form_width = models.IntegerField(default=0, verbose_name='表单宽度')
    form_height = models.IntegerField(default=0, verbose_name='表单高度')
    table_width = models.IntegerField(default=0, verbose_name='表格宽度')
    table_height = models.IntegerField(default=0, verbose_name='表格高度')

    enable = models.BooleanField(default=True, verbose_name='是否启用')
    show_header = models.BooleanField(default=True, verbose_name='展示头部')
    allow_batch = models.BooleanField(default=True, verbose_name='批处理')
    allow_search = models.BooleanField(default=True, verbose_name='检索功能')
    allow_sort = models.BooleanField(default=True, verbose_name='排序功能')
    allow_pop = models.BooleanField(default=True, verbose_name='移动功能')
    allow_insert = models.BooleanField(default=True, verbose_name='新增功能')
    allow_edit = models.BooleanField(default=True, verbose_name='编辑功能')
    allow_remove = models.BooleanField(default=True, verbose_name='删除功能')
    allow_download = models.BooleanField(default=True, verbose_name='下载功能')
    allow_upload = models.BooleanField(default=True, verbose_name='上传功能')

    class Meta:
        verbose_name = '数据视图'
        unique_together = ('meta', 'code')


class MetaField(VModel):
    # 标识
    view = models.ForeignKey('MetaView', on_delete=models.CASCADE, verbose_name='数据视图')
    prop = models.CharField(max_length=100, verbose_name='字段名称')  #
    label = models.CharField(max_length=100, verbose_name='字段标签')  #
    name = models.CharField(max_length=100, verbose_name='字段别名')  #

    """tool"""
    domain = models.CharField(max_length=100, verbose_name='字段类型')  #
    tool = models.CharField(max_length=100, default='default', verbose_name='工具组件')
    refer = models.JSONField(default=dict, verbose_name='索引')  #
    format = models.JSONField(default=dict, verbose_name='格式')  #


    """rest"""
    not_null = models.BooleanField(default=False, verbose_name='不为空') #
    allow_edit = models.BooleanField(default=True, verbose_name='可编辑')
    allow_sort = models.BooleanField(default=True, verbose_name='可排序')
    allow_search = models.BooleanField(default=True, verbose_name='可搜索')
    allow_download = models.BooleanField(default=True, verbose_name='可下载')
    allow_upload = models.BooleanField(default=False, verbose_name='可上传')
    allow_update = models.BooleanField(default=False, verbose_name='可更新')

    """table"""
    unit = models.CharField(max_length=55, verbose_name='单位符', null=True)
    column_width = models.FloatField(default=0, verbose_name='表头宽度')
    align = models.CharField(max_length=55, default='left', verbose_name='对齐方式') #
    fixed = models.CharField(max_length=100, verbose_name='固定位置', null=True)
    header_color = models.CharField(max_length=55, verbose_name='表头颜色', null=True)
    cell_color = models.CharField(max_length=55, verbose_name='单元颜色', null=True)
    edit_on_table = models.BooleanField(default=True, verbose_name='表格编辑')
    hide_on_table = models.BooleanField(default=False, verbose_name='表内隐藏')

    """form"""
    span = models.IntegerField(default=0, verbose_name='表单占位')
    hide_on_form = models.BooleanField(default=False, verbose_name='表单隐藏')
    hide_on_form_edit = models.BooleanField(default=False, verbose_name='编辑隐藏')
    hide_on_form_insert = models.BooleanField(default=False, verbose_name='新增隐藏')
    hide_on_form_branch = models.BooleanField(default=False, verbose_name='分支隐藏')
    hide_on_form_leaf = models.BooleanField(default=False, verbose_name='叶子隐藏')


    class Meta:
        verbose_name = '视图字段'



class MetaFieldTool(VTree):
    name = models.CharField(max_length=255, null=True, verbose_name='名称')
    code = models.CharField(max_length=100, unique=True, null=True, verbose_name='代码')  #
    format = models.JSONField(default=dict, verbose_name='格式参数')  #

    class Meta:
        verbose_name = '元数据字段工具'
#
#
class TestM(models.Model):
    name = models.CharField(max_length=100, verbose_name='<UNK>')

class MetaFieldDomain(VModel):
    name = models.CharField(max_length=255, unique=True, null=True, verbose_name='名称')
    tools = models.ManyToManyField(to=MetaFieldTool, verbose_name='工具集')
    default = models.ForeignKey(
        to=MetaFieldTool, null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='默认工具')
    search = models.ForeignKey(
        to=MetaFieldTool, null=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name='搜索工具')
    align = models.CharField(max_length=10, null=True, verbose_name='对齐方式')
    class Meta:
        verbose_name = '元数据字段类型'


class ValaTree(VTree):
    text = models.TextField(null=True, verbose_name='text')
    class Meta:
        verbose_name = '树形测试'

class Vala(VModel):
    text_field = models.TextField(null=True, verbose_name='text')
    boolean_field = models.BooleanField(null=True, verbose_name='boolean')
    integer_field = models.IntegerField(null=True, verbose_name='integer')
    float_field = models.FloatField(null=True, verbose_name='float')
    date_field = models.DateField(null=True, verbose_name='date')
    datetime_field = models.DateTimeField(null=True, verbose_name='datetime')
    time_field = models.TimeField(null=True, verbose_name='time')
    json_field = models.JSONField(null=True, verbose_name='json')
    file = models.FileField(null=True, verbose_name='File')
    # menus = models.ManyToManyField(to=MetaField, related_name='+')
    # menu = models.ForeignKey(to=MetaField, null=True, on_delete=models.CASCADE, verbose_name='vala')


class M2O(VModel):
    vala = models.ForeignKey(to=Vala, null=True, on_delete=models.CASCADE, verbose_name='vala')
    name = models.CharField(max_length=100, null=True, verbose_name='name')


class O2O(VModel):
    vala = models.OneToOneField(to=Vala, null=True, on_delete=models.CASCADE, verbose_name='vala')
    name = models.CharField(max_length=100, null=True, verbose_name='name')


class M2M(VTree):
    valas = models.ManyToManyField(to=Vala, verbose_name='valas')
    name = models.CharField(max_length=100, null=True, verbose_name='name')