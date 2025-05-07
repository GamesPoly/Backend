from django.core.exceptions import ValidationError

def validate_file_size(value):
    limit_mb = 100
    if value.size > limit_mb * 1024 * 1024:
        raise ValidationError(f'Максимальный размер файла – {limit_mb}MB')
