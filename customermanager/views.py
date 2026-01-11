from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer
from .serializers import CustomerSerializer


# =========================
# API (Swagger / REST)
# =========================

@api_view(["GET"])
@permission_classes([AllowAny])
def show_customer(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([AllowAny])
def show_customer_details(request, id):
    customer = get_object_or_404(Customer, pk=id)

    if request.method == "GET":
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = CustomerSerializer(instance=customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    customer.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def show_first_customer(request):
    customer = Customer.objects.first()
    if not customer:
        return Response(
            {"detail": "No customers found"},
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = CustomerSerializer(customer)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([AllowAny])
def write_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# HTML (Browser View)

def customers_page(request):
    customers = Customer.objects.all()

    create_mode = request.GET.get("create") == "1"
    edit_id = request.GET.get("edit")

    edit_customer = None
    if edit_id:
        edit_customer = get_object_or_404(Customer, pk=edit_id)

    return render(
        request,
        "customermanager/customers.html",
        {
            "customers": customers,
            "create_mode": create_mode,
            "edit_customer": edit_customer,
        }
    )


def create_customer(request):
    if request.method == "POST":
        serializer = CustomerSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Customer created successfully.")
            return redirect("customers_page")
        messages.error(request, "Error creating customer.")

    customers = Customer.objects.all()
    return render(
        request,
        "customermanager/customers.html",
        {"customers": customers, "create_mode": True}
    )


def edit_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)

    if request.method == "POST":
        serializer = CustomerSerializer(instance=customer, data=request.POST)
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
            "edit_customer": customer,  # WICHTIG: Name wie im Template
        }
    )


def delete_customer(request, id):
    customer = get_object_or_404(Customer, pk=id)

    if request.method == "POST":
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect("customers_page")

    return redirect("customers_page")