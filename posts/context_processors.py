from django.contrib.auth.models import User


def author(request):
    """Return current author's name (if present) or username"""
    nick = request.resolver_match.kwargs.get("username", "")
    if nick:
        username = User.objects.get(username=nick)
        author_name = username.get_full_name() or nick
    else:
        author_name = ""
    return {"author_name": author_name}
