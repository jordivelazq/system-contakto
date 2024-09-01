from django.conf import settings
from django.contrib.auth.context_processors import PermWrapper

from app.core.models import User, UserManager

def UserActive(request):
    if request.user.is_authenticated and 'user_main' in request.session and request.session.get('user_main'):
        usuario = UserManager.objects.filter(main_id=request.session.get('user_main'), active=True) if request.user.is_authenticated else None
        if usuario:
            usuario = usuario.first()
            request.user = usuario.copy
            return {'request': request, 'user': request.user, 'perms': PermWrapper(request.user), 'manager_active': True, 'user_manager': usuario}
    return {'request': request, 'user': request.user, 'perms': PermWrapper(request.user), 'manager_active': False}
