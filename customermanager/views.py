from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


# =========================
# API (Swagger / REST)  ✅ wie bei deliveries
# =========================

@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def customers_api(request):
    """
    /customers/api/
    - GET  -> Liste
    - POST -> Create
    """
    if request.method == "GET":
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    # POST
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def customer_api_detail(request, id):
    """
    /customers/api/<id>/
    - GET    -> Detail
    - PUT    -> Update
    - DELETE -> Delete
    """
    customer = get_object_or_404(Customer, pk=id)

    if request.method == "GET":
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    if request.method == "PUT":
        # partial=True ist stabiler (wie bei deliveries)
        serializer = CustomerSerializer(instance=customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE
    customer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# =========================
# OPTIONAL: extra Endpoint (wenn du ihn behalten willst)
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def show_first_customer(request):
    customer = Customer.objects.first()
    if not customer:
        return Response({"detail": "No customers found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


# =========================
# HTML (Browser View)
# =========================

def customers_page(request):
    customers = Customer.objects.all()

    create_mode = request.GET.get("create") == "1"
    edit_id = request.GET.get("edit")

    edit_customer_obj = None
    if edit_id:
        edit_customer_obj = get_object_or_404(Customer, pk=edit_id)

    return render(
        request,
        "customermanager/customers.html",
        {
            "customers": customers,
            "create_mode": create_mode,
            "edit_customer": edit_customer_obj,
        }
    )


def create_customer(request):
    # POST = wirklich anlegen
    if request.method == "POST":
        # Feldnamen müssen zu deinem customers.html passen
        salutation = request.POST.get("salutation", "").strip()
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        street = request.POST.get("street", "").strip()
        house_number = request.POST.get("house_number", "").strip()
        zip_code = request.POST.get("zip_code", "").strip()
        city = request.POST.get("city", "").strip()

        # Pflichtfelder (wie im HTML "required")
        if not (salutation and name and email and phone):
            messages.error(request, "Bitte Pflichtfelder ausfüllen (Anrede, Name, E-Mail, Telefon).")
            customers = Customer.objects.all()
            return render(
                request,
                "customermanager/customers.html",
                {"customers": customers, "create_mode": True},
            )

        # Optional: doppelte Email verhindern
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Diese E-Mail existiert bereits.")
            customers = Customer.objects.all()
            return render(
                request,
                "customermanager/customers.html",
                {"customers": customers, "create_mode": True},
            )

        # ✅ Speichern in DB
        Customer.objects.create(
            salutation=salutation,
            name=name,
            email=email,
            phone=phone,
            street=street,
            house_number=house_number,
            zip_code=zip_code,
            city=city,
        )

        messages.success(request, "Customer created successfully.")
        return redirect("customers_page")

    # GET = Create-Form anzeigen (create_mode)
    customers = Customer.objects.all()
    return render(
        request,
        "customermanager/customers.html",
        {"customers": customers, "create_mode": True},
    )


def edit_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)

    if request.method == "POST":
        serializer = CustomerSerializer(instance=customer, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Customer updated successfully.")
            return redirect("customers_page")
        messages.error(request, "Error updating customer.")

    customers = Customer.objects.all()
    return render(
        request,
        "customermanager/customers.html",
        {
            "customers": customers,
            "edit_customer": customer,
        }
    )


def delete_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)

    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect("customers_page")

    return redirect("customers_page")