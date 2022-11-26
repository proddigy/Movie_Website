from django import template
from films.forms import CommentForm
from films.models import Genre


register = template.Library()


@register.simple_tag(name='get_list_genres')
def get_genres():
    return Genre.objects.all()


# @register.inclusion_tag('_add_comment_form.html')
# def add_comment():
#     form = CommentForm
#     form.instance =
#     return {'form': form}

