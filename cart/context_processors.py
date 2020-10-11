from .models import Cart

def cart(request):
    try:
        if(request.user.id):
            cart = Cart.objects.get(user=request.user)
            return {'cart': cart}
        # handles anonymous user    
        return {}
    except:
        return {}