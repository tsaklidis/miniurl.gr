import secrets
import string

def get_random_url_string(length=8, prefix='', suffix=''):
    # RFC3986 unreserved characters
    allowed_chars = string.ascii_letters + string.digits
    if not isinstance(length, int) or length < 4:
        length = 8
    rand_part = ''.join(secrets.choice(allowed_chars) for _ in range(length))
    return f'{prefix}{rand_part}{suffix}'
