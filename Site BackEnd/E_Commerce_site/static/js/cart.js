// Function for loading cart items
function load_cart_items(){

    // Local storage instance
    var ls = localStorage

    // It is possible to not have cart items list in Localstorage, that's why try catch block
    try{

        // Parsing cart items and -> Product IDS
        var cart_items = JSON.parse(ls.cart)
        var cart_items_ids = JSON.parse(ls.cart_items)

        // Parent Item container where all the items will be loaded
        var item_container = document.getElementById('item-container-item')

        // Looping through each cart item available in localStorage

        cart_items.forEach((item) => {

            // New div element setting class as item
            var ele = document.createElement('div')
            ele.classList.add('item')

            // Setting attribute id for future tracking purpose
            ele.setAttribute('id', 'cart_item-'+item.p_id)

            // Cart Item innerHTML template --> with  details
            var template = `  <div class="img-title-details"><div class="left"><img src="${item.p_img}" alt="${item.p_title}"></div><div class="right"><p class="title">${item.p_title}</p>
                              <small>Size:<select onchange="change_size(${item.p_id})" id="cart-item-size-${item.p_id}"><option value="${item.size}" >${item.size}</option><option value="M">M</option>
                              <option value="XL">XL</option><option value="XXL">XXL</option></select></small></div></div><div class="q-p-container"><div class="quantity-price"><div class="quantity">
                              <select name="cart-quantity" id="cart-item-quantity-${item.p_id}" onchange="change_quantity(${item.p_id})"><option value="${item.quantity}">${item.quantity}</option>
                              <option value="1">1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option><option value="6">6</option>
                              <option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option><option value="11">11</option><option value="12">12</option>
                              <option value="13">13</option><option value="14">14</option><option value="15">15</option><option value="16">16</option><option value="17">17</option><option value="18">18</option>
                              <option value="19">19</option></select></div><div class="price"><p class="price">$<span class="price-total-per-item" id="cart-item-total-price-${item.p_id}">${Number(item.p_price) * Number(item.quantity)}</span></p>
                              <p class="price-per-pc">${item.p_price}$/ per item</p></div></div><div class="like-and-remove-btn"><button class="remove" onclick="remove_cart_item(${item.p_id})">Remove</button>
                              </div></div>
                               `

            // Setting Item innerHTML
            ele.innerHTML = template

            // Appending the cart item and a line after it for separation
            item_container.appendChild(ele)
            var line = document.createElement('div')
            line.classList.add('line')
            line.setAttribute('id', 'line-'+item.p_id)
            item_container.appendChild(line)

        })

        // Calculating total prices of the items with tax
        calculate_total_price()


        // If there is not cart Item in localStorage -> Disable checkout button for good.
        if (cart_items_ids == 0){
            var ele_btn = document.getElementById('checkout_btn')

            ele_btn.children[0].disabled = true
            ele_btn.children[0].style.background = 'gray'
            ele_btn.children[0].style.opacity = '.6'
            ele_btn.children[0].style.cursor = 'not-allowed'


        }
    }catch{
        // If no cart item exists show this message in item container
        document.getElementById('item-container-item').innerHTML = 'Cart is empty !'
    }


}

// Calling once when the page is loaded / reloaded
load_cart_items()


// Remove cart item
function remove_cart_item(id){

    // Parsing cart items and their IDS from localstorage
    var cart_items = JSON.parse(ls.cart)
    var cart_items_ids = JSON.parse(ls.cart_items)

    // Looping through them to find out the target item
    cart_items.forEach( (item) => {

        // If found, remove it from localstorage along with Html page too.
        if (Number(item.p_id) === Number(id)){
            var idx = cart_items.indexOf(item)
            cart_items.splice(idx, 1)
            cart_items_ids.splice(cart_items_ids.indexOf(id), 1)
            $('#cart_item-'+id).remove()
            $('#line-'+id).remove()
        }
    })

    // Updating cart items, and IDS after deletion.
    ls.setItem('cart', JSON.stringify(cart_items))
    ls.setItem('cart_items', JSON.stringify(cart_items_ids))

    // Updating cart item count
    set_cart_item_count()

    // Updating total price
    calculate_total_price()

}


// Change cart item quantity -> tity ->
function change_quantity(id){

    // Getting cart IDS from local storage
    var cart_items = JSON.parse(ls.cart)

    // Looping through each of them
    cart_items.forEach( (item) => {

        // If a match found
        if (item.p_id == id){

            // Update its quantity and price according to quantity -> tity ->
            item.quantity = $('#cart-item-quantity-'+id).val()
            item.p_total_price = Number($('#cart-item-quantity-'+id).val()) * Number(item.p_price)
            update_price(id, item)
        }
    });

    // Updating cart items
    ls.setItem('cart', JSON.stringify(cart_items))

    // Updating total price of the items in cart
    calculate_total_price()
}


// Change size
function change_size(id){

    // Parsing data from localstorage
    var cart_items = JSON.parse(ls.cart)


    // Looping through each of them
    cart_items.forEach( (item) => {

        // If match found
        if (item.p_id == id){

            // Change it's size
            item.size = $('#cart-item-size-'+id).val()
        }
    });

    // Updating cart item size
    ls.setItem('cart', JSON.stringify(cart_items))

}

// Update price according to quantity

function update_price(id, item){
    $('#cart-item-total-price-'+id).text( Number(item.p_price)*Number(item.quantity))

    calculate_total_price()

}

// Calculate total prices

function calculate_total_price(){

    var total = 0
    var prices = document.querySelectorAll('.price-total-per-item')
    prices.forEach((p)=>{
        total += Number(p.innerHTML)
    })

    // Calculating tax and discount -> All though this are constant now, but who cares
    var cal_tax = tax_percentage/100*total
    var cal_discount = discount_amount/100*total

    // Prices includes tax , discount and all items prices
    $('#unit-price').text(total)
    $('#dicount-amount').text(discount_amount)
    $('#tax-amount').text(cal_tax)
    $('#items_total_amount').text(total + cal_tax - cal_discount)
}