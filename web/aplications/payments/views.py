import mercadopago
from django.conf import settings
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.urls import reverse
from aplications.orders.models import Order
from aplications.cart.utils import get_cart

@require_POST
def mp_create_preference(request):
    cart = get_cart(request)
    if not cart:
        return JsonResponse({'error':'Carrito vacío'}, status=400)
    sdk = mercadopago.SDK(settings.MP_ACCESS_TOKEN)
    order = Order.objects.create()
    items, total = [], 0.0
    for line in cart:
        items.append({
            'id': str(line['id']),'title': line['name'],'quantity': int(line['qty']),
            'currency_id':'ARS','unit_price': float(line['price']),
        })
        total += float(line['price']) * int(line['qty'])
    order.total_amount = total
    order.save()
    pref_data = {
        'items': items,
        'back_urls': {
            'success': settings.SITE_URL + reverse('payments:mp_feedback'),
            'failure': settings.SITE_URL + reverse('payments:mp_feedback'),
            'pending': settings.SITE_URL + reverse('payments:mp_feedback'),
        },
        'auto_return': 'approved',
        'notification_url': settings.SITE_URL + reverse('payments:mp_webhook'),
        'external_reference': str(order.id),
    }
    pref = sdk.preference().create(pref_data)
    order.mp_preference_id = pref['response']['id']
    order.save()
    return JsonResponse({'init_point': pref['response']['init_point']})

def mp_feedback(request):
    status = request.GET.get('collection_status') or request.GET.get('status')
    payment_id = request.GET.get('payment_id') or request.GET.get('collection_id')
    order_id = request.GET.get('external_reference')
    if order_id:
        try:
            order = Order.objects.get(pk=order_id)
            if status: order.status = status
            if payment_id: order.mp_payment_id = payment_id
            order.save()
        except Order.DoesNotExist:
            pass
    return redirect('orders:detail', pk=order_id)

@csrf_exempt
def mp_webhook(request):
    secret = request.headers.get('X-Webhook-Secret')
    if settings.MP_WEBHOOK_SECRET and secret != settings.MP_WEBHOOK_SECRET:
        return HttpResponseForbidden('forbidden')
    return JsonResponse({'ok': True})
