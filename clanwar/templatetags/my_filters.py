# my_filters.py
# Some custom filters for dictionary lookup.
from django.template.defaultfilters import register

@register.filter(name='lookup')

def lookup(dic, index):
    if index in dic:
        return dic[index]
    return ''
