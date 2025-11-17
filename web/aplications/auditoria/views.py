from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Auditoria

@login_required
@user_passes_test(lambda u: u.is_staff)
def auditoria_list(request):
    registros = Auditoria.objects.select_related('usuario').all()
    return render(request, 'auditoria/auditoria_list.html', {'registros': registros})
