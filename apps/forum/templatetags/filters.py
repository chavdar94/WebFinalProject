from django import template

register = template.Library()


@register.filter
def user_has_liked(comment, user):
    try:
        return comment.like_set.filter(user=user).exists()
    except:
        return False
