from django.template.defaultfilters import register

@register.filter(name='to_range')

def to_range(dic, index):
    return range(dic[index])
