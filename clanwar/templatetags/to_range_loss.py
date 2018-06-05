from django.template.defaultfilters import register

@register.filter(name='to_range_loss')

def to_range_loss(dic, index):
    loss = dic['battlesPlayed'] - dic[index]
    return range(loss)
