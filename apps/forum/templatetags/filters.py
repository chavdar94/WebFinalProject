from django import template

register = template.Library()


@register.filter
def user_has_liked(comment, user):
    try:
        return comment.like_set.filter(user=user).exists()
    except:
        return False


@register.filter
def add_field_classes(field, css_classes):
    classes = field.field.widget.attrs.get('class', '').split()
    classes.extend(css_classes.split())
    field.field.widget.attrs['class'] = ' '.join(classes)
    return field
