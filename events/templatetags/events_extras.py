import bleach
import markdown as md
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Officers are trusted authors, but articles still render as raw HTML on public
# pages, so the output is sanitized to a safe subset rather than trusted outright.
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'em', 'ul', 'ol', 'li',
    'h1', 'h2', 'h3', 'h4', 'blockquote', 'code', 'pre',
    'a', 'img', 'hr',
]
ALLOWED_ATTRS = {
    'a': ['href', 'title'],
    # width/height enable the `attr_list` sizing syntax, e.g.
    # ![alt](url){: width="300" }. CSS (.article-body img { max-width: 100% })
    # still caps the rendered size regardless of the value here.
    'img': ['src', 'alt', 'title', 'width', 'height'],
}


@register.filter(name='markdownify')
def markdownify(text):
    if not text:
        return ''
    html = md.markdown(text, extensions=['extra', 'nl2br'])
    clean_html = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
    return mark_safe(clean_html)
