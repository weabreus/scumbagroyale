from datetime import datetime
from time import strftime
import pytz
from django.template.defaultfilters import register

@register.filter(name='to_datetime')

def to_datetime(dic, index):
    return datetime.utcfromtimestamp(dic[index]).replace(tzinfo=pytz.utc)
