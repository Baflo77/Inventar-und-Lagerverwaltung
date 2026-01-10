from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    is_mitarbeiter = request.user.groups.filter(name="Mitarbeiter").exists()

    return render(request, 'inventory/index.html', {"is_mitarbeiter": is_mitarbeiter,})