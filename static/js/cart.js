total = document.getElementById('cart-total');
var cartTotal = 0;
updateCartTotal();

function updateCartTotal() {
	url = "http://127.0.0.1:8000/api/order-details/";
	total.innerHTML = '0';
	
	fetch(url)
	.then((resp) => resp.json)
	.then(data => {
		cartTotal = data.get_cart_total;
		total.innerHTML = data.get_cart_items;
	})

}



function addCookieItem(productID, action){
	console.log('Not Logged In...');

	if(action=='add') {
		if(cart[productID]==undefined) {
			cart[productID] = {'quantity':1};
		} else {
			cart[productID]['quantity'] += 1;
		}
	}
	if(action=='remove') {
		cart[productID]['quantity'] -= 1;

		if(cart[productID]['quantity'] <= 0) {
			delete cart[productID];
		}
	}
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/";
	console.log('Cart:', cart);
	location.reload();
}





