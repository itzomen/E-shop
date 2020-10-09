from .models import Cart

def cart(request):
    # get user cart and add to request if user is signed in
    if(request.user.id):
        cart = Cart.objects.filter(user=request.user, in_cart=True)
        return {'cart': cart}
    return {}