var discount_amount = 0;
var tax_percentage = 10;
var shipping_fee = 150;
// Search suggestion and selection

var s_list = document.getElementById('s-list')
all_keywords.forEach((item) => {
    var ele = document.createElement('small')
    ele.innerHTML = item
    s_list.appendChild(ele)
});


try{
const searchInput = document.querySelector("#nav-search");
const listItems = document.querySelectorAll("#s-list small");
var s_r_s = document.getElementById('s-r-s')
searchInput.addEventListener("input", function() {
    s_r_s.classList.remove('d-none')
    const searchTerm = searchInput.value.toLowerCase().trim();

    try{
        // for products page

        search_query = searchTerm
        trigger()
    }catch{}

    var cnt = 0;
    listItems.forEach(function(item) {
        if (item.textContent.toLowerCase().includes(searchTerm) & cnt < 10) {
        item.style.display = "block";
        cnt += 1
        } else {
        item.style.display = "none";
        }
    });
});

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

// To change background color of hero



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
    var keys = Object.keys(localStorage)
    try{
    if (keys.includes('cart_items')){
        var item_count = JSON.parse(localStorage.cart_items).length
        console.log(item_count)
        document.getElementById('cart-item-count').innerHTML = item_count
        document.getElementById('cart-item-count1').innerHTML = item_count

    }}catch{}
}
set_cart_item_count()

// Add to cart and add to wishlist feature specification

let ls = localStorage
var keys = Object.keys(ls)


// Add to cart

function get_size_quantity(value){

    if (value){
        var size = $('#p_size').val()
        var quantity = $('#q-count').text()
        return {'size': size, 'quantity': quantity}
    }
    else{
        return {'size': 'M', 'quantity': 1}
    }

}


function add_to_cart(product_id, user, s_q){

    var p_id = product_id


    if (keys.includes('cart')){

        var cart_items = JSON.parse(ls.cart_items)

        if ( !cart_items.includes(p_id)){
            var items = JSON.parse(ls.cart)

            var data = {'p_id':p_id, 'p_title': $('#p_title-'+p_id).text(), 'p_price': $('#p_price-'+p_id).text(),
                        'p_img': $('#p_img-'+p_id).attr('src'), 'size': s_q.size, 'quantity': s_q.quantity,
                        'in_stock': $('#p_status-'+p_id).val(), 'p_total_price': Number($('#p_price-'+p_id).text()) * Number(s_q.quantity)}
            items.push(data)

            ls.setItem('cart', JSON.stringify(items))

            let cart_items = JSON.parse(ls.cart_items)
            cart_items.push(p_id)
            ls.setItem('cart_items', JSON.stringify(cart_items))
            set_cart_item_count()
        }

    }
    else{


        var data = {'p_id':p_id, 'p_title': $('#p_title-'+p_id).text(), 'p_price': $('#p_price-'+p_id).text(),
                    'p_img': $('#p_img-'+p_id).attr('src'),  'size': s_q.size, 'quantity': s_q.quantity,
                    'in_stock': $('#p_status-'+p_id).val(), 'p_total_price': Number($('#p_price-'+p_id).text()) * Number(s_q.quantity)}

        ls.setItem('cart', JSON.stringify([data]))
        ls.setItem('cart_items', JSON.stringify([p_id]))
        keys = Object.keys(ls)
        set_cart_item_count()
    }



}

// Add to wishlist

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
       let req = $.ajax({
            type:'post',
            url:'/account/save-wishlist-item/',
            data:{
                csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
                product_id: product_id,
                user_id: user_id
            }
       })
       req.done(function(response){

            var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
            token.value = response['token']
       })
    }
}
