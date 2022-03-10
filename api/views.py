from math import prod
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import *
from .models import *
from .utils import *
import datetime
import json
# Create your views here.


@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Product List':'/products',
		'Order Details':'/order-details',
		'Cart Items List':'/cart-item-list',
		'Add/Delete Items from Cart':'/cart-update-item/<str:action>/<str:pk>',
		'Process Order':'/process-order',
	}

	return Response(api_urls)

@api_view(['GET'])
def productList(request):
	products = Product.objects.all()
	serializer = ProductSerializer(products, many=True)
	return Response(serializer.data)


@api_view(['GET'])
def orderDetails(request):
	details = getOrderDetails(request)
	return Response(details)
		
	
@api_view(['GET'])
def cartItemList(request):
	items = getCartItemList(request)
	return Response(items)



@api_view(['GET'])
def cartUpdateItem(request, action, pk):
	product = Product.objects.get(id=pk)
	customer = request.user.customer
	order, created_order = Order.objects.get_or_create(customer=customer, complete=False)
	if action=='add':
		orderitem, created_orderitem = OrderItem.objects.get_or_create(order=order, product=product)
		orderitem.quantity += 1
		orderitem.save()
		result = 'added'
	else:
		orderitem = OrderItem.objects.get(order=order, product=product)
		if orderitem.quantity > 1:
			orderitem.quantity -= 1
			orderitem.save()
		else:
			orderitem.delete()
		result = 'remove'
	return Response({f'Item {result}': orderitem.product_name})


@api_view(['POST'])
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = request.data

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		
	else:
		name = data['form']['name']
		email = data['form']['email']
		customer, created = Customer.objects.get_or_create(email=email)
		customer.name = name
		customer.save()
		order = Order.objects.create(
			customer = customer,
			complete = False,
		)
		try:
			cart = json.loads(request.COOKIES['cart'])
		except:
			cart = {}
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
		for item in items:
			product = Product.objects.get(id=item['product_id'])
			orderitem = OrderItem.objects.create(
				product = product,
				order = order,
				quantity = item['quantity'],
			)



	total = data['form']['total']
	order.transaction_id = transaction_id
	if total == float(order.get_cart_total):
		order.complete = True
	order.save()
	ShippingAddress.objects.create(
	customer=customer,
	order=order,
	address=data['shipping']['address'],
	city=data['shipping']['city'],
	state=data['shipping']['state'],
	zipcode=data['shipping']['zipcode'],
	)

	return JsonResponse('Payment submitted..', safe=False)

