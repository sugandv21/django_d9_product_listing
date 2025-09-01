from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Product

def home(request):
    return render(request, "products/layout/home.html")
def product_list(request):
    query = request.GET.get("q", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    availability = request.GET.get("availability", "").strip()

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(brand__icontains=query))

    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    if availability == "available":
        products = products.filter(is_available=True)
    elif availability == "unavailable":
        products = products.filter(is_available=False)

    total_results = products.count()

    paginator = Paginator(products.order_by("name"), 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "products/layout/product_list.html",
        {
            "page_obj": page_obj,
            "query": query,
            "min_price": min_price,
            "max_price": max_price,
            "availability": availability,
            "total_results": total_results,
        },
    )

