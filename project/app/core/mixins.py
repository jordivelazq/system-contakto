from django.utils.deprecation import MiddlewareMixin

from app.core.models import UserManager


class UserActiveMixin(MiddlewareMixin):
    def process_request(self, request):
        if not hasattr(request, 'session') or request.session.is_empty():
            return
        else:
            if request.user.username:
                if request.user.is_authenticated and request.user.is_superuser:
                    request.session['user_main'] = request.user.id
                    usuario = UserManager.objects.filter(main=request.user, active=True) if request.user.is_authenticated else None
                    if usuario:
                        usuario = usuario.first()
                        request.user = usuario.copy
