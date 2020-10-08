from .models import Cart

def cart(request):
    # get user cart and add to request
    if(request.user.id):
        cart = Cart.objects.get(user=request.user, ordered=False)
        return {'cart': cart}
    return {}