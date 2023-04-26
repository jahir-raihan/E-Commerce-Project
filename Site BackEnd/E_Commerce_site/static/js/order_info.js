let dc = document;

// Load saved addresses if it is in Localstorage

function load_saved_address(){
    ls = localStorage
    try{
        var ele = dc.getElementById('saved-addresses')
        var addresses = JSON.parse(ls.addresses)

        // Looping through each address
        addresses.forEach( (adrs) => {

            var address = dc.createElement('div')
            address.classList.add('address')
            address.setAttribute('id', adrs.address_id)
            var template = `<div class="address-info"><div class="icon-and-info"><div class="img">
                            <i class="fa fa-map-marker loc-icon" aria-hidden="true"></i></div>
                            <p class="address-details">${adrs.city}, ${adrs.address}, zip: ${adrs.zipcode}
                            </p></div><div class="three-dots"><i class="fa fa-ellipsis-v t-dots" ></i></div>
                            </div>`

            address.innerHTML = template

            // Appending the address
            ele.appendChild(address)
        })

    }catch{

        // Like a maze -> it was causing error , so i've decided to ignore it instead fix it :)
        try{
            dc.getElementById('saved-addresses-container-local').style.display = 'none'
        }catch{}
    }
}

// Loading once when page is loaded
load_saved_address()



// Guest checkout functionalities
// If guest checkout is checked -> Mark all user inputs as required
// Else -> Mark them as not required and disable them

var is_guest_checkout = false
function toggle_g_d(){
    var inputs = dc.querySelectorAll('.a-f-tp input')
    var a_f_tp = dc.querySelectorAll('.a-f-tp')
    var show = false
    var ele = dc.getElementById('guest_checkout')
    if (!ele.checked){
        show = true
    }
    inputs.forEach((inp)=>{
        inp.disabled = show
        if (show){
            inp.required = false
        }
        else{
            inp.required = true
        }
    })
    is_guest_checkout = show
    if (!show){
        a_f_tp.forEach( (a)=>{
            a.style.opacity = '1'
        })
    } else{
        a_f_tp.forEach( (a)=>{
            a.style.opacity = '.6'
        })
    }
    dc.getElementById('phone').disabled = false
    dc.getElementById('phone').required = true

}

// Selected payment method -> It's showed as cards in frontEnd


// We've hided out bkash because we didn't got an approval from bkash as merchant which required to setup a payment
// System using bkash

let payment_method = 'cod'; // Default payment method

let cod = dc.getElementById('cod')

//  let bksh = dc.getElementById('bkash')

let sslcom = dc.getElementById('sslcom')
let choices = dc.querySelectorAll('.choice-card')

choices.forEach ( (choice) => {
    choice.addEventListener( 'click', function(){
        if (choice.id == 'cod'){
            payment_method = 'cod';
            cod.classList.add('choice-selected')
//            bksh.classList.remove('choice-selected')
            sslcom.classList.remove('choice-selected')

        }
//        else if (choice.id == 'bkash'){
//            payment_method = 'bkash';
//            bksh.classList.add('choice-selected')
//            cod.classList.remove('choice-selected')
//            sslcom.classList.remove('choice-selected')
//
//        }
        else if (choice.id == 'sslcom'){
            payment_method = 'sslcom';
            sslcom.classList.add('choice-selected')
//            bksh.classList.remove('choice-selected')
            cod.classList.remove('choice-selected')

        }
    })
})

// End Selected payment method


// Selected Saved address , if saved

// This one selects saved address from localstorage if user is not registered
let saved_address_selected = null
let addresses = dc.querySelectorAll('.address')
let address_info = dc.querySelectorAll('.address-info')

addresses.forEach( (address) => {
    address.addEventListener('click', function(){
        if (saved_address_selected === address.id){
            saved_address_selected = null;
            address_info.forEach((ad_info) => {
                ad_info.classList.remove('address-selected')
            });
            enable_address_input()
        } else {
            saved_address_selected = address.id;
            address_info.forEach((ad_info) => {
                ad_info.classList.remove('address-selected')
            });
            address.children[0].classList.add('address-selected')
            disable_address_input()
        }

    })
})

// Disable / Enable address input if saved address is selected / not selected

// Disable
function disable_address_input(){
    var inputs = dc.querySelectorAll('.a-f-btm input')
    var a_f_btm = dc.querySelectorAll('.a-f-btm')
    inputs.forEach( (inp) => {
        inp.disabled = true
    })

    a_f_btm.forEach((a)=>{
        a.style.opacity = '.6'
    })
}

// Enable
function enable_address_input(){
    var inputs = dc.querySelectorAll('.a-f-btm input')
    var a_f_btm = dc.querySelectorAll('.a-f-btm')
    inputs.forEach( (inp) => {
        inp.disabled = false
        inp.required = true
    })
    a_f_btm.forEach((a)=>{
        a.style.opacity = '1'
    })
}

// End selected saved address

// load cart items --> Checkout page -> Tiny version with little information

function load_cart_items(){
    var ls = localStorage
    var cart_items = JSON.parse(ls.cart)
    var cart_items_ids = JSON.parse(ls.cart_items)
    var item_container = document.getElementById('items-in-cart')
    cart_items.forEach((item) => {
        var ele = document.createElement('div')
        ele.classList.add('item')
        ele.setAttribute('id', 'check_out_cart_item-'+item.p_id)
        var template = ` <div class="img"><img src="${item.p_img}" alt="${item.p_title}"><div class="cnt"><p>${item.quantity}</p></div></div><div class="info">
                         <p class="title">${item.p_title}</p><small>Total : $ ${item.p_total_price}</small></div>`
        ele.innerHTML = template

        // Appending tiny cart items
        item_container.appendChild(ele)

    })


}

// Loading cart items only once while page is loading
load_cart_items()

// Calculate total prices of cart items
function calculate_total_price(){

    var total = 0
    // Parsing cart items

    var items = JSON.parse(ls.cart)

    // Looping through each of them and calculating total
    items.forEach((p)=>{
        total += Number(p.p_total_price)
    })

    // Adding tax and discount amount
    var cal_tax = tax_percentage/100*total
    var cal_discount = discount_amount/100*total

    // Updating prices in the Html template
    $('#unit-price').text(total)
    $('#dicount-amount').text(discount_amount)
    $('#shipping-amount').text(shipping_fee)
    $('#tax-amount').text(cal_tax)
    $('#items_total_amount').text(total + cal_tax + shipping_fee - cal_discount)
}

// Calling while page is loaded once
calculate_total_price()


// Confirm Checkout request form

$(document).on('submit', '#shipping-and-address-form', function(e){

    e.preventDefault();
    // Getting address

    if (saved_address_selected === null){
        var address = {

            'city': $('#city').val(),
            'address': $('#address').val(),
            'zipcode': $('#zipcode').val(),
            'country': $('#country').val()
        }
        var save_address_check_box = dc.getElementById('save-this-address')
        if (save_address_check_box.checked){

            if ($('#user').val() === 'AnonymousUser'){
                try{
                    var address_list = JSON.parse(ls.addresses)
                    var address_count = JSON.parse(ls.address_count) + 1
                    address.address_id = address_count

                    address_list.push(address)
                }catch{
                    var address_count = 0
                    var address_list = [address]
                    address_list[0].address_id = address_count
                }
                ls.setItem('addresses', JSON.stringify(address_list))
                ls.setItem('address_count', JSON.stringify(address_count))
            }else{
                address.save_it = true
            }


        }else{
            address.save_it = false
        }
    }
    else{
        var address = {
        }

        if ($('#user').val() === 'AnonymousUser'){
            var address_list = JSON.parse(ls.addresses)
            address_list.forEach((adrs) => {
                if (adrs.address_id == saved_address_selected){
                    address = adrs
                }
            });
        }else{
            address = saved_address_selected
        }
    }

    // End Address


    // D-Compressing cart items data for fast run time and  and accessible
    var items_ids = []
    var items_quantities = []
    var items_prices = [];
    var items_sizes = [];

    JSON.parse(ls.cart).forEach( (itm) => {
        items_ids.push(itm.p_id)
        items_quantities.push(itm.quantity)
        items_prices.push(itm.p_total_price)
        items_sizes.push(itm.size)

    })

    // End d-compress cart items

    // Sending request
    let req = $.ajax({
        type:'post',
        url:'/order/checkout/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            address: address,
            items_ids: items_ids,
            items_quantities: items_quantities,
            items_prices: items_prices,
            items_sizes: items_sizes,
            first_name : $('#first_name').val(),
            last_name : $('#last_name').val(),
            phone : $('#phone').val(),
            email : $('#email').val(),
            user : $('#user').val(),
            payment_method: payment_method,
            note_to_seller: $('#note_to_seller').val(),
            total_price: $('#items_total_amount').text(),
            guest_checkout: is_guest_checkout,
            save_address: dc.getElementById('save-this-address').checked
        }
    });

    // On success
    req.done(function(response){
        // Resetting cart items
        ls.setItem('cart', '[]')
        ls.setItem('cart_items', '[]')

        // Redirecting to response url , it can be payment page or order history page , depends on action and payment
        // Type

        window.location.href = response.url
    })


})