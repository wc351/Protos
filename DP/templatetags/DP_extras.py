from django import template

register = template.Library()


@register.filter(name='f_type')
def f_type(value):
    name = value.__class__.__name__
    lookup = {'IntField': 1,
              'BoolField': 2,
              'DeciField': 3,
              'FloatField': 4,
              'CharField': 5,
              'ObjectOfStudy': 6,
             }
    return lookup[name]

@register.filter(name='oos_type')
def oos_type(value):
    name = value.__class__.__name__
    lookup = {'ObjectOfStudy': 1,
             }
    return lookup[name]