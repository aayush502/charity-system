from django import template
from django.contrib.auth.models import User
from django.template.loader import get_template
register = template.Library()
import pdb

@register.simple_tag(takes_context=True)
def get_user(context):
    request = context['request']
    users = User.objects.get(id=request.session['user_id'])
    admin = users.is_superuser
    return admin
    
@register.filter()
def to_int(value):
    return int(value)

@register.simple_tag(takes_context=True)
def set_breakpoint(context, *args):
    vars = [arg for arg in locals()['args']]
    pdb.set_trace()
