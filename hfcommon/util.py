try:
    import urlparse  # py2
except ImportError:
    import urllib.parse as urlparse  # py3


def find(lst, predicate):
    return next((x for x in lst if predicate(x)), None)


def try_int(value, default=None):
    try:
        return int(value)
    except Exception:
        return default


def host_included(url, host_list):
    host = urlparse.urlsplit(url).hostname

    if not host:
        return False

    return bool(find(host_list, lambda x: host.endswith(x)))
