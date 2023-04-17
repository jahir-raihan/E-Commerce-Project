let dc = document;

// Load saved addresses if in the memory

function load_saved_address(){
    ls = localStorage
    try{
        var ele = dc.getElementById('saved-addresses')
        var addresses = JSON.parse(ls.addresses)
        addresses.forEach( (adrs) => {
            console.log(address)
            var address = dc.createElement('div')
            address.classList.add('address')
            address.setAttribute('id', adrs.address_id)
            var template = `<div class="address-info"><div class="icon-and-info"><div class="img">
                            <i class="fa fa-map-marker loc-icon" aria-hidden="true"></i></div>
                            <p class="address-details">${adrs.city}, ${adrs.address}, zip: ${adrs.zip}
                            </p></div><div class="three-dots"><i class="fa fa-ellipsis-v t-dots" ></i></div>
                            </div>`

            address.innerHTML = template

            ele.appendChild(address)
        })

    }catch{

    // Like a maze

        try{
            dc.getElementById('saved-addresses-container-local').style.display = 'none'
        }catch{}
    }
}
load_saved_address()



// Guest checkout functionalities

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

}

// Selected payment method

let payment_method = 'cod';

let cod = dc.getElementById('cod')
let bksh = dc.getElementById('bkash')
let sslcom = dc.getElementById('sslcom')
let choices = dc.querySelectorAll('.choice-card')
choices.forEach ( (choice) => {
    choice.addEventListener( 'click', function(){

        if (choice.id == 'cod'){
            payment_method = 'cod';
            cod.classList.add('choice-selected')
            bksh.classList.remove('choice-selected')
            sslcom.classList.remove('choice-selected')

        }
        else if (choice.id == 'bkash'){
            payment_method = 'bkash';
            bksh.classList.add('choice-selected')
            cod.classList.remove('choice-selected')
            sslcom.classList.remove('choice-selected')

        }
        else if (choice.id == 'sslcom'){
            payment_method = 'sslcom';
            sslcom.classList.add('choice-selected')
            bksh.classList.remove('choice-selected')
            cod.classList.remove('choice-selected')

        }
    })
})

// End Selected payment method


// Selected Saved address , if saved

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

// Disable / Enable address input if saved address is selected / di-selected

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

// load cart items

function load_cart_items(){
    var ls = localStorage
    var cart_items = JSON.parse(ls.cart)
    var cart_items_ids = JSON.parse(ls.cart_items)
    var item_container = document.getElementById('items-in-cart')
    cart_items.forEach((item) => {
        var ele = document.createElement('div')
        ele.classList.add('item')
        ele.setAttribute('id', 'check_out_cart_item-'+item.p_id)
        var template = ` <div class="img">
                            <img src="${item.p_img}" alt="${item.p_title}">
                            <div class="cnt">
                                <p>${item.quantity}</p>
                            </div>
                         </div>

                         <div class="info">
                            <p class="title">${item.p_title}</p>
                            <small>Total : $ ${item.p_total_price}</small>
                         </div>`
        ele.innerHTML = template
        item_container.appendChild(ele)

    })


}

load_cart_items()

// Calculate total prices

function calculate_total_price(){

    var total = 0
    var items = JSON.parse(ls.cart)
    items.forEach((p)=>{
        total += Number(p.p_total_price)
    })

    var cal_tax = tax_percentage/100*total
    var cal_discount = discount_amount/100*total

    $('#unit-price').text(total)
    $('#dicount-amount').text(discount_amount)
    $('#shipping-amount').text(shipping_fee)
    $('#tax-amount').text(cal_tax)
    $('#items_total_amount').text(total + cal_tax + shipping_fee - cal_discount)
}
calculate_total_price()