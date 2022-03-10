from .serializers import *
from .models import *
import json
import datetime

def getOrderDetails(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)	
		serializer = OrderSerializer(order, many=False)
		return serializer.data
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		order = {'get_cart_total':0, 'get_cart_items':0}
		for id in cart:
			product = Product.objects.get(id=id)
			order['get_cart_items'] += cart[id]['quantity']
			order['get_cart_total'] += product.price * cart[id]['quantity']
		return order

def getCartItemList(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		serializer = OrderItemSerializer(items, many=True)
		return serializer.data
	else:
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
		order = {'get_cart_total':0, 'get_cart_items':0}
		items = []
		for id in cart:
			try:
				product = Product.objects.get(id=id)
				item = {

					'product_id': product.id,
					'product_name': product.name,
					'product_price': product.price,
					'imageURL': product.imageURL,
					'quantity': cart[id]['quantity']
				}
				items.append(item)
			except:
				pass
		return items