import json
import base64
import hmac
import hashlib
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.utils import timezone
from account.models import Notification

# Create your views here.
def success(request):
    encoded_data = request.GET.get("data") 
    if not encoded_data: 
        return HttpResponse("Invalid response", status=400) 
 
    # Step 1: Decode Base64 → JSON 
    try: 
        decoded_json = base64.b64decode(encoded_data).decode("utf-8") 
        payload = json.loads(decoded_json) 
    except Exception: 
        return HttpResponse("Invalid data", status=400) 
 
    # Step 2: Verify Signature 
    try: 
        signed_fields = payload["signed_field_names"].split(",") 
        # Build message in the order of signed_fields excluding 'signed_field_names' 
        message = ",".join([f"{field}={payload[field]}" for field in signed_fields]) 
 
        # Use Test Secret Key 
        secret_key = "8gBm/:&EnhH.1/q"  # Test mode key 
        expected_signature = base64.b64encode( 
            hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest() 
        ).decode() 
 
        # Compare signature (strip '=' padding for safety) 
        if expected_signature.rstrip('=') != payload["signature"].rstrip('='): 
            # Debugging: show mismatch 
            return HttpResponse("Invalid signature", status=400) 
    except KeyError as e: 
        return HttpResponse(f"Missing field: {e}", status=400) 
     
    txn,created=Transaction.objects.get_or_create(transaction_uuid=payload['transaction_uuid'],transaction_code=payload['transaction_code'],product_code=payload['product_code'],total_amount=payload['total_amount'],user=request.user,status=payload['status'])
    Notification.objects.create(user=request.user,title="Payment successful"
)
    order,created=Order.objects.get_or_create(transaction_code=payload['transaction_code'],product_code=payload['product_code'],total_amount=payload['total_amount'],user=request.user,status=payload['status'])
    cart = request.session.get('checkout')

    if cart:
        product = Product.objects.get(id=cart['product_id'])
        created_at = timezone.now()
        booked_till = created_at + timedelta(days=cart['days'])
        OrderItem.objects.create(
            order=order,
            product=product,
            price=cart['price'],
            quantity=cart['days'],
            created_at=created_at,
            booked_till=booked_till
        )
        request.session['cart']={}
        Notification.objects.create(user=request.user,title="Vehicle booked successfully")
    context = {
        'amount': payload['total_amount']
    }

    return render(request, 'success_esewa.html', context)

def failure(request):
    return render(request,'success_esewa.html')