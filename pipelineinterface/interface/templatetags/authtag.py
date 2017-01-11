from django import template

notification = template.Library()

@notification.simple_tag
def custom_tag(arg_a):
    
