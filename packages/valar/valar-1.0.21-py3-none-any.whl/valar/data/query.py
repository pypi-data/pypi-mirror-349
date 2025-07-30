from functools import reduce
from django.db.models import Q




class Condition:
    def __init__(self, condition):
        self.includes = condition.get('includes', {})
        self.excludes = condition.get('excludes', {})



class Query:
    def __init__(self, body=None):
        if body is None:
            body = {}
        self.template = body.get('template', {})
        self.condition = Condition(body.get('condition', {}))
        self.search = [Condition(condition) for condition in body.get('search', [])]
        self.orders = body.get('orders', {})
        self.finder = body.get('finder', {})
        self.page = body.get('page',1)
        self.size = body.get('size', 0)

    def orm_orders(self):
        array = []
        for key in self.orders:
            value = self.orders.get(key)
            prefix = '-' if value == -1 else ''
            array.append(f'{prefix}{key}')
        return array

    def orm_conditions(self):
        includes, excludes = self.condition.includes, self.condition.excludes
        if len(self.search):
            inc = [Q(**{**includes, **sea.includes}) for sea in self.search]
            exc = [Q(**{**excludes, **sea.excludes}) for sea in self.search]
            def fun(x, y): return x | y
            return [reduce(fun, inc), reduce(fun, exc)]
        else:
            return [Q(**self.condition.includes), Q(**self.condition.excludes)]

    def mon_conditions(self):
        from .mon.query_translator import MongoQueryTranslator
        return MongoQueryTranslator.translate_query(self)

    # def _mon_conditions(self):