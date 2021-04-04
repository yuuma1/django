from django.template import Library
import bleach

register = Library()

@register.filter
def comment_filter(text):
    return ''.join(list(map(convert_url, bleach.clean(text).split('\n'))))

def convert_url(text_line):
    if 'https://' in text_line or 'http://' in text_line:
        return '<a href="' + text_line + '" target="_blank" rel="noopener noreferrer">' + text_line + '</a>'
    else:
        return text_line