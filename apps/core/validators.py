from django.core.exceptions import ValidationError

IMAGE_MAX_SIZE = 5242880  # 5MB


def validate_file_size(image_obj):
    if image_obj.size > IMAGE_MAX_SIZE:
        raise ValidationError(
            'The maximum file size that can be uploaded is 5MB')
