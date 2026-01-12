from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from cart.models import Cart
from django.contrib import messages

@login_required
def order_create(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart or not cart.items.exists():
        messages.warning(request, "Your cart is empty")
        return redirect('product_list')

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_cost=cart.get_total_cost()
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                price=item.product.price,
                quantity=item.quantity
            )
        
        # Clear cart
        cart.items.all().delete() # Or cart.delete(), but keeping the cart object is fine for persistent user cart logic if modified
        # Actually deleting the items is enough.
        
        messages.success(request, f"Order {order.id} placed successfully!")
        return render(request, 'orders/created.html', {'order': order})

    return render(request, 'orders/create.html', {'cart': cart})
