class Cart():
    def __init__(self, request):
        session = request.session
        self.session = session
        if not session.get('cart'): session['cart'] = []
        self.cart = session.get('cart')

    def __iter__(self):
        for item in self.cart:
            yield item

    def add(self, id):
        if not id in self.cart:
            self.cart.append(id)
        self.save()

    def save(self):
        self.session.modified = True