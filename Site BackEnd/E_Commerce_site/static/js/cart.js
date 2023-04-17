
function load_cart_items(){
    var ls = localStorage
    try{
        var cart_items = JSON.parse(ls.cart)
        var cart_items_ids = JSON.parse(ls.cart_items)
        var item_container = document.getElementById('item-container-item')
        cart_items.forEach((item) => {
            var ele = document.createElement('div')
            ele.classList.add('item')
            ele.setAttribute('id', 'cart_item-'+item.p_id)
            var template = `    <div class="img-title-details">
                                    <div class="left">
                                        <img src="${item.p_img}" alt="${item.p_title}">
                                    </div>
                                    <div class="right">
                                        <p class="title">${item.p_title}</p>
                                        <small>Size: ${item.size}</small>
                                    </div>
                                </div>
                                <div class="q-p-container">
                                    <div class="quantity-price">
                                        <div class="quantity">
                                            <select name="cart-quantity" id="cart-item-quantity-${item.p_id}" onchange="change_quantity(${item.p_id})">
                                                <option value="${item.quantity}">${item.quantity}</option>
                                                <option value="1">1</option>
                                                <option value="2">2</option>
                                                <option value="3">3</option>
                                                <option value="4">4</option>
                                                <option value="5">5</option>
                                                <option value="6">6</option>
                                                <option value="7">7</option>
                                                <option value="8">8</option>
                                                <option value="9">9</option>
                                                <option value="10">10</option>
                                                <option value="11">11</option>
                                                <option value="12">12</option>
                                                <option value="13">13</option>
                                                <option value="14">14</option>
                                                <option value="15">15</option>
                                                <option value="16">16</option>
                                                <option value="17">17</option>
                                                <option value="18">18</option>
                                                <option value="19">19</option>
                                            </select>
                                        </div>
                                        <div class="price">
                                            <p class="price">$<span class="price-total-per-item" id="cart-item-total-price-${item.p_id}">${Number(item.p_price) * Number(item.quantity)}</span></p>

                                            <p class="price-per-pc">${item.p_price}$/ per item</p>
                                        </div>
                                    </div>
                                    <div class="like-and-remove-btn">
                                        <button class="remove" onclick="remove_cart_item(${item.p_id})">Remove</button>
                                    </div>
                                </div>`
            ele.innerHTML = template
            item_container.appendChild(ele)
            var line = document.createElement('div')
            line.classList.add('line')
            line.setAttribute('id', 'line-'+item.p_id)
            item_container.appendChild(line)

        })
        calculate_total_price()
    }catch{
        document.getElementById('item-container-item').innerHTML = 'Cart is empty !'
    }

}
load_cart_items()

// Remove cart item

function remove_cart_item(id){
    var cart_items = JSON.parse(ls.cart)
    var cart_items_ids = JSON.parse(ls.cart_items)
    cart_items.forEach( (item) => {
        if (item.p_id == id){
            var idx = cart_items.indexOf(item)
            cart_items.splice(idx)
            cart_items_ids.splice(cart_items_ids.indexOf(id))
            $('#cart_item-'+id).remove()
            $('#line-'+id).remove()
        }
    })
    ls.setItem('cart', JSON.stringify(cart_items))
    ls.setItem('cart_items', JSON.stringify(cart_items_ids))
    set_cart_item_count()
    calculate_total_price()

}

// Change cart item quantity

function change_quantity(id){
    var cart_items = JSON.parse(ls.cart)

    cart_items.forEach( (item) => {
        if (item.p_id == id){
            item.quantity = $('#cart-item-quantity-'+id).val()
            item.p_total_price = Number($('#cart-item-quantity-'+id).val()) * Number(item.p_price)
            update_price(id, item)
        }
    });
    ls.setItem('cart', JSON.stringify(cart_items))
    calculate_total_price()
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

    var cal_tax = tax_percentage/100*total
    var cal_discount = discount_amount/100*total

    $('#unit-price').text(total)
    $('#dicount-amount').text(discount_amount)
    $('#tax-amount').text(cal_tax)
    $('#items_total_amount').text(total + cal_tax - cal_discount)
}