from django.db.utils import ProgrammingError, OperationalError

# Carrusel (no rompe si faltan migraciones)
def carousel_slides(request):
    try:
        from .models import CarouselSlide
        slides = CarouselSlide.objects.filter(is_active=True).order_by('order')[:10]
    except (ProgrammingError, OperationalError, Exception):
        slides = []
    return {'carousel_slides': slides}


# Categorías + contador carrito (para navbar)
def layout_meta(request):
    try:
        from catalog.models import Category
        cats = Category.objects.all()
    except Exception:
        cats = []

    cart = request.session.get('cart', {})

    # Si el carrito no es un diccionario válido, reiniciarlo
    if not isinstance(cart, dict):
        cart = {}

    cart_count = sum(int(item.get('qty', 1)) for item in cart.values())

    return {"nav_categories": cats, "cart_count": cart_count}
