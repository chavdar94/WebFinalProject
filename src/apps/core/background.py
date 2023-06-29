from django.templatetags.static import static


def background_image(request):
    url = request.path

    if url.startswith('/profile'):
        background = static('images/profile-bg.jpg')
    else:
        background = static('images/bg-darken.jpg')

    return {'background': background}
