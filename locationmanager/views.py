from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes # <--- permission_classes neu
from rest_framework.permissions import AllowAny # <--- AllowAny neu
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie

from .models import Location
from .serializers import LocationSerializer

# --- 1. HTML View ---
# ensure_csrf_cookie sorgt dafür, dass der Browser das Token bekommt
@ensure_csrf_cookie
def show_locations(request):
    # WICHTIG: Hier müssen wir die Daten aus der DB holen
    all_locations = Location.objects.all()

    context = {
        'locations': all_locations
        # Dieser Name 'locations' muss mit dem HTML {% for location in locations %} übereinstimmen
    }
    return render(request, 'locationmanager/locationmanager.html', context)

# --- 2. API: Liste (GET) ---
@api_view(['GET'])
@permission_classes([AllowAny]) # <--- Erlaubt Zugriff auch ohne Login
def get_locations(request):
    locations = Location.objects.all().order_by('-created_at')
    serializer = LocationSerializer(locations, many=True)
    return Response(serializer.data)

# --- 3. API: Speichern (POST) ---
@api_view(['POST'])
@permission_classes([AllowAny])
def write_location(request):
    """
    Erlaubt jedem (auch Nicht-Admins), Daten zu speichern.
    """
    serializer = LocationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)