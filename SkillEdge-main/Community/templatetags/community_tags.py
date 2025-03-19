from django import template
from django.utils.html import mark_safe
import re

register = template.Library()

@register.filter
def format_content(content):
    """Format post content with basic markdown-like features"""
    # Convert URLs to links
    url_pattern = r'(https?://[^\s]+)'
    content = re.sub(url_pattern, r'<a href="\1" target="_blank" class="text-indigo-600 hover:underline">\1</a>', content)
    
    # Convert ** for bold
    bold_pattern = r'\*\*(.*?)\*\*'
    content = re.sub(bold_pattern, r'<strong>\1</strong>', content)
    
    # Convert * for italic
    italic_pattern = r'\*(.*?)\*'
    content = re.sub(italic_pattern, r'<em>\1</em>', content)
    
    # Convert linebreaks to <br>
    content = content.replace('\n', '<br>')
    
    return mark_safe(content) 