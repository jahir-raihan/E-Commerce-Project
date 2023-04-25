// Constant discount, tax_percentage and shipping fee variables
var discount_amount = 0;
var tax_percentage = 10;
var shipping_fee = 150;


// Search suggestion and selection

//
var s_list = document.getElementById('s-list')

// all_keywords variable is defined inside index.html template in head section , I was unable to find a way out to
// Load keywords data while loading the page inside js , that's why with the help of jinga I've initialized a runtime
// and load time variable inside index.html for keywords

all_keywords.forEach((item) => {
    var ele = document.createElement('small')
    try{
        ele.innerHTML = item
        s_list.appendChild(ele)
    }catch{}
});


// Search inputs suggestions . -> Using try and catch block to avoid undefined error , because there's other
// Pages without search facility on them.
try{
    const searchInput = document.querySelector("#nav-search");
    const listItems = document.querySelectorAll("#s-list small");
    var s_r_s = document.getElementById('s-r-s')
    searchInput.addEventListener("input", function() {
        s_r_s.classList.remove('d-none')
        const searchTerm = searchInput.value.toLowerCase().trim();

        // This block for product page, -> Im overloaded person you know, I love to use a function for multipurpose
        try{
            search_query = searchTerm
            trigger()
        }catch{}

        var cnt = 0;

        // Looping through keywords and appending them to the suggestion list
        listItems.forEach(function(item) {
            if (item.textContent.toLowerCase().includes(searchTerm) & cnt < 10) {
            item.style.display = "block";
            cnt += 1
            } else {
            item.style.display = "none";
            }
        });
    });


    // If the user takes is cursor from the input we just remove the suggestion list.
    searchInput.addEventListener("blur", function() {
        setTimeout(function() {
          s_r_s.classList.add('d-none')
        }, 100);

    });

    // Set input value on item click event
    listItems.forEach(function(item) {
        item.addEventListener("click", function() {
            searchInput.value = item.textContent;
            window.location.href = 'http://127.0.0.1:8000/products/' + '?s=' + item.textContent

        });
    });
}catch{}

// End Search suggestion and selection


// Toggle Nav menu


// A Naive thing
function toggle_nav_menu(){
    var obj = document.getElementById('nav-ham-menu');
    var obj2 = document.getElementById('cross-icon-nav-ham')
    var obj3 = document.getElementById('container')
    var toggle_nav = document.getElementById('toggle-nav')
    if (obj.contains(obj2)){
        obj.innerHTML = '<i class="fa fa-bars" aria-hidden="true"></i>'
        toggle_nav.style.display = 'none'
        try{
            obj3.classList.remove('fade-out')
        }catch{}
    }else{
        obj.innerHTML = '<i id="cross-icon-nav-ham" class="fa fa-times"></i>'
        toggle_nav.style.display = 'block'
        try{
            obj3.classList.add('fade-out')
        }catch{}
    }
}

// End Toggle Nav menu


// Change Background colors -> only for fun nothing else

// array of background colors to cycle through
var bgColors = ['pink', '#E5E0FF', 'pink', '#F8CBA6', '#AACB73'];

// get reference to the body element
const body = document.getElementById('hero');

// initialize color index
let colorIndex = 0;

// set interval to change background color every 1 minute
setInterval(() => {
   // change background color to next color in array
   try{
    body.style.backgroundColor = bgColors[colorIndex];
   }catch{}
   

   // increment color index, reset to 0 if end of array is reached
   colorIndex = (colorIndex + 1) % bgColors.length;
}, 5000);
// End change color hero



// Set current cart items count
function set_cart_item_count(){

    // Getting local storage instance
    var keys = Object.keys(localStorage)

    // Try catch block to avoid undefined error, it is possible to not have cart_items declared.
    try{
        if (keys.includes('cart_items')){
            var item_count = JSON.parse(localStorage.cart_items).length
            console.log(item_count)
            document.getElementById('cart-item-count').innerHTML = item_count
            document.getElementById('cart-item-count1').innerHTML = item_count
        }
    }catch{}
}

// Setting cart items count on page load
set_cart_item_count()


// Add to cart and add to wishlist feature specification

var ls = localStorage
var keys = Object.keys(ls)

// Add to cart function
function get_size_quantity(value){

    // This function will return Item size and quantity -> tity ->
    if (value){
        var size = $('#p_size').val()
        var quantity = $('#q-count').text()
        return {'size': size, 'quantity': quantity}
    }
    else{
        return {'size': 'M', 'quantity': 1}
    }

}

// Function to Add a item to cart
function add_to_cart(product_id, user, s_q){

    // Getting product id
    var p_id = product_id

    // If local storage already have a cart instance
    if (keys.includes('cart')){

        // Parse if
        var cart_items = JSON.parse(ls.cart_items)

        // Check if cart items includes current item -> If not then add it
        if ( !cart_items.includes(p_id)){
            var items = JSON.parse(ls.cart)

            // Retrieving product data as a JS object
            var data = {'p_id':p_id, 'p_title': $('#p_title-'+p_id).text(), 'p_price': $('#p_price-'+p_id).text(),
                        'p_img': $('#p_img-'+p_id).attr('src'), 'size': s_q.size, 'quantity': s_q.quantity,
                        'in_stock': $('#p_status-'+p_id).val(), 'p_total_price': Number($('#p_price-'+p_id).text()) * Number(s_q.quantity)}
            items.push(data)

            // Compressing items as string to store them
            ls.setItem('cart', JSON.stringify(items))
            let cart_items = JSON.parse(ls.cart_items)
            cart_items.push(p_id)
            ls.setItem('cart_items', JSON.stringify(cart_items))

            // Finally updating the cart count
            set_cart_item_count()
        }

    }

    // If local storage doesn't have any cart instance
    else{

        // Add cart instance to local storage
        var data = {'p_id':p_id, 'p_title': $('#p_title-'+p_id).text(), 'p_price': $('#p_price-'+p_id).text(),
                    'p_img': $('#p_img-'+p_id).attr('src'),  'size': s_q.size, 'quantity': s_q.quantity,
                    'in_stock': $('#p_status-'+p_id).val(), 'p_total_price': Number($('#p_price-'+p_id).text()) * Number(s_q.quantity)}

        // Set compressed data
        ls.setItem('cart', JSON.stringify([data]))
        ls.setItem('cart_items', JSON.stringify([p_id]))

        // Update keys and cart item counts
        keys = Object.keys(ls)
        set_cart_item_count()
    }



}

// Add to wishlist --> Same Explanation as Cart but one difference
// Difference -> If user is registered , then push the wished item directly to backend and update the template after
// Successful operation , otherwise do it with localstorage

function add_to_wishlist(product_id, user, user_id=null){
    var p_id = product_id

    // If user is not authenticated

    if (user  === 'AnonymousUser'){

        if (keys.includes('wishlist')){

            var wishlist_items = JSON.parse(ls.wishlist_items)

            if ( !wishlist_items.includes(p_id)){
                var items = JSON.parse(ls.wishlist)
                console.log(items)
                var data = {'p_id':p_id, 'p_title': $('#p_title-'+p_id).text(), 'p_price': $('#p_price-'+p_id).text(),
                            'p_img': $('#p_img-'+p_id).attr('src')}
                items.push(data)
                console.log(items)
                ls.setItem('wishlist', JSON.stringify(items))


                let wishlist_items = JSON.parse(ls.wishlist_items)
                wishlist_items.push(p_id)
                ls.setItem('wishlist_items', JSON.stringify(wishlist_items))
            }
        }
        else{


            var data = {'p_id':p_id, 'p_title': $('#p_title-'+p_id).text(), 'p_price': $('#p_price-'+p_id).text(),
                        'p_img': $('#p_img-'+p_id).attr('src')}

            ls.setItem('wishlist', JSON.stringify([data]))
            ls.setItem('wishlist_items', JSON.stringify([p_id]))
            keys = Object.keys(ls)
        }
    }

    // If user is authenticated

    else{

        // Sending request to backend
       let req = $.ajax({
            type:'post',
            url:'/account/save-wishlist-item/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                product_id: product_id,
                user_id: user_id
            }
       })

       // On success
       req.done(function(response){

            // Just update the token
            var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
            token.value = response['token']
       })
    }
}



// Load locally saved addresses
// If user is not registered or logged in and there's addresses in local storage -> load them up and show them in
// Checkout page or Local Account page

function load_saved_address_local(){
    ls = localStorage

    // Try catch block to avoid undefined error, It is possible that address can be undefined
    try{
        var ele = document.getElementById('locally_saved_addresses_user')

        // parsing address data
        var addresses = JSON.parse(ls.addresses)

        // Looping through each address object
        addresses.forEach( (adrs) => {
            console.log(address)
            var address = document.createElement('div')
            address.classList.add('address')
            address.setAttribute('id', adrs.address_id)
            var template = `<div class="address-info"><div class="icon-and-info"><div class="img">
                            <i class="fa fa-map-marker loc-icon" aria-hidden="true"></i></div>
                            <p class="address-details">${adrs.city}, ${adrs.address}, zip: ${adrs.zipcode}
                            </p></div><div class="three-dots"><i class="fa fa-ellipsis-v t-dots" ></i></div>
                            </div>`

            address.innerHTML = template

            // Appending each address data
            ele.appendChild(address)
        })
    }catch{}

}

// Calling function for once while loading
load_saved_address_local()


// Login - Register Redirect

// This one is a interesting feature , when a user clicks login button from checkout or cart or any page , -> After
// Successful Registration or Login , the user will be redirected to where he came from

function login(url){
    ls.setItem('redirect_url', url)
    window.location.href = '/account/login/'
}
function register(url){
    ls.setItem('redirect_url', url)
    window.location.href = '/account/register/'
}