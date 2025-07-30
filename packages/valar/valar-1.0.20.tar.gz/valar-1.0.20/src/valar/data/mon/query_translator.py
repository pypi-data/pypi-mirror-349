class MongoQueryTranslator:
    # 将Django ORM查询操作符映射到MongoDB操作符的字典
    MONGO_OPERATORS = {
        'exact': lambda v, e: {'$ne': v} if e else v,
        'iexact': lambda v, e: {'$not': {'$regex': f'^{v}$', '$options': 'i'}} if e else {'$regex': f'^{v}$', '$options': 'i'},
        'contains': lambda v, e: {'$not': {'$regex': f'{v}'}} if e else {'$regex': f'{v}'},
        'icontains': lambda v, e: {'$not': {'$regex': f'{v}', '$options': 'i'}} if e else {'$regex': f'{v}', '$options': 'i'},
        'startswith': lambda v, e: {'$not': {'$regex': f'^{v}'}} if e else {'$regex': f'^{v}'},
        'istartswith': lambda v, e: {'$not': {'$regex': f'^{v}', '$options': 'i'}} if e else {'$regex': f'^{v}', '$options': 'i'},
        'endswith': lambda v, e: {'$not': {'$regex': f'{v}$'}} if e else {'$regex': f'{v}$'},
        'iendswith': lambda v, e: {'$not': {'$regex': f'{v}$', '$options': 'i'}} if e else {'$regex': f'{v}$', '$options': 'i'},
        'gt': lambda v, e: {'$not': {'$gt': v}} if e else {'$gt': v},
        'gte': lambda v, e: {'$not': {'$gte': v}} if e else {'$gte': v},
        'lt': lambda v, e: {'$not': {'$lt': v}} if e else {'$lt': v},
        'lte': lambda v, e: {'$not': {'$lte': v}} if e else {'$lte': v},
        'in': lambda v, e: {'$nin': v} if e else {'$in': v},
        'exists': lambda v, e: {'$eq': None} if (e and bool(v)) or (not e and not bool(v)) else {'$ne': None},
        'isnull': lambda v, e: {'$ne': None} if e else {'$eq': None},
    }
    
    @classmethod
    def process_field_query(cls, key, value, is_exclude=False):
        """处理单个字段查询"""
        if '__' in key:
            field, op = key.split('__', 1)
            if op in cls.MONGO_OPERATORS:
                return field, cls.MONGO_OPERATORS[op](value, is_exclude)
        return key, {'$ne': value} if is_exclude else value
    
    @classmethod
    def process_condition(cls, condition_dict, is_exclude=False):
        """处理条件字典，返回MongoDB查询条件"""
        return {field: query for field, query in 
                [cls.process_field_query(k, v, is_exclude) for k, v in condition_dict.items()]}
    
    @classmethod
    def process_finder(cls, finder):
        """处理finder字段，转换为MongoDB查询条件"""
        if not finder:
            return {}
        mongo_query = {}
        if 'term' in finder and finder['term'] and isinstance(finder['term'], str):
            term = finder['term']
            fields = finder.get('fields', [])
            if fields:
                mongo_query['$or'] = [{field: {'$regex': term, '$options': 'i'}} for field in fields]
            else:
                mongo_query['$text'] = {'$search': term}
        if 'range' in finder:
            for field, ranges in finder['range'].items():
                field_query = {f'${op}': val for op, val in ranges.items() if op in ['gt', 'gte', 'lt', 'lte']}
                if field_query:
                    mongo_query[field] = field_query
        for query_type, operator in [('match', None), ('exists', '$ne')]:
            if query_type in finder:
                for field, value in finder[query_type].items():
                    if operator == '$ne':
                        # 处理exists查询，检查字段是否为空
                        mongo_query[field] = {'$ne': None} if bool(value) else {'$eq': None}
                    else:
                        mongo_query[field] = value
        return mongo_query
    
    @classmethod
    def translate_query(cls, query_obj):
        """
        将Query对象转换为MongoDB查询
        Args:
            query_obj: Query对象，包含condition, search和finder
        Returns:
            转换后的MongoDB查询条件
        """
        query = {}
        query.update(cls.process_condition(query_obj.condition.includes))
        query.update(cls.process_condition(query_obj.condition.excludes, True))
        # 处理搜索条件
        if query_obj.search:
            or_conditions = []
            for sea in query_obj.search:
                search_query = {}
                search_query.update(cls.process_condition(sea.includes))
                search_query.update(cls.process_condition(sea.excludes, True))
                if search_query:
                    or_conditions.append(search_query)
            if or_conditions:
                query["$or"] = or_conditions
        # 处理和合并finder条件
        finder_query = cls.process_finder(query_obj.finder)
        if finder_query and query:
            return {"$and": [query, finder_query]}
        return finder_query or query 