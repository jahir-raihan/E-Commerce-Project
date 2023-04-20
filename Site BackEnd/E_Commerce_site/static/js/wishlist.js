// Constantly update is stock status of a wishlist product
var dc = document


function check_availability_wishlist(){
    var items = dc.querySelectorAll('.status')
    items.forEach( (item) => {
        let req = $.ajax({
            type:'get',
            url: '/account/check-wishlist-item-availability/',
            data:{
                p_id:item.getAttribute('id')
            }
        });

        req.done(function(response){
            if (response.status){
                var btn = dc.getElementById('wishlist-cart-btn-'+item.getAttribute('id'))
                btn.disabled = false
                item.innerHTML = 'In Stock'
                item.style.color = 'green'
                btn.style.backgroundColor='#0D6EFD'
                btn.style.cursor = 'pointer'
                btn.style.opacity = '1'
            }else{
                var btn = dc.getElementById('wishlist-cart-btn-'+item.getAttribute('id'))
                btn.disabled = true
                btn.style.backgroundColor='gray'
                btn.style.cursor = 'not-allowed'
                btn.style.opacity = '.6'
                item.innerHTML = 'Out of stock'
                item.style.color = 'red'

            }
        })

    })


}

setInterval(() => {
    try{
        check_availability_wishlist()
    }catch{}
}, 5000)



// Load wishlist items local users

function load_wishlist_items(){
    try{
        var ls = localStorage
        var items = JSON.parse(ls.wishlist)
        items.forEach( (item) => {
            var ele = document.createElement('div')
            ele.classList.add('item')
            var wishlist_container = dc.getElementById('load-wishlist-items')
            ele.setAttribute('id', 'wish-list-item-'+item.p_id)
            var template = `<div class="trash">

                                <i class="fas fa-trash" onclick="remove_wishlist_item_local(${item.p_id})"></i>

                            </div>

                            <div class="img-and-details">
                                <img id="p_img-${item.p_id}" src="${item.p_img}" alt="${item.p_title}">

                                <div>
                                     <p class="wish-item-title" id="p_title-${item.p_id}">${item.p_title}</p>
                                    <small>$ <span id="p_price-${item.id}">${item.p_price}</span></small>
                                </div>

                                <div class="trash-right">

                                    <i class="fas fa-trash" onclick="remove_wishlist_item_local(${item.p_id})"></i>

                                </div>

                            </div>


                            <p class="status" style="color:red;" id="${item.p_id}">Out of stock</p>
                            <div class="add-to-cart-and-datetime">
                                <div class="date"></div>

                                <button class="add-to-cart" style="background-color:gray; opacity:.6;cursor:not-allowed;" disabled id="wishlist-cart-btn-${item.p_id}" onclick="add_to_cart( ${item.p_id}, 'AnnymousUser', get_size_quantity(false) )">
                                    Add to cart
                                </button>
                            </div>
                            `
            ele.innerHTML = template
            wishlist_container.appendChild(ele)
        })

        if (JSON.parse(ls.wishlist_items).length === 0){
            dc.getElementById('load-wishlist-items').innerHTML = '<p class="title" style="text-align:center;"> Wishlist is empty ! </p>'
        }
    }catch{}
}
load_wishlist_items()

// Remove wishlist items

// For registered users

function remove_wishlist_item(id){
    let req = $.ajax({
        type:'get',
        url:'/account/remove-wishlist-item/',
        data:{
            product_id:id
        }
    });
    req.done(function(response){
        $('#wish-list-item-'+id).remove()

        if (response.items_count == 0){
            $('#wishlist-item-title').text('Wishlist is empty !')
            dc.getElementById('wishlist-item-title').style.textAlign = 'center'
        }
        console.log(response.items_count)
    })
}

// For local users

function remove_wishlist_item_local(id){
    var wish_items = JSON.parse(ls.wishlist)
    var wish_items_ids = JSON.parse(ls.wishlist_items)
    wish_items.forEach( (item) => {
        if (Number(item.p_id) === Number(id)){
            var idx = wish_items.indexOf(item)
            wish_items.splice(idx, 1)
            wish_items_ids.splice(wish_items_ids.indexOf(id), 1)
            $('#wish-list-item-'+id).remove()
            $('#line-'+id).remove()

        }
    })
    ls.setItem('wishlist', JSON.stringify(wish_items))
    ls.setItem('wishlist_items', JSON.stringify(wish_items_ids))

    if (wish_items_ids.length === 0){
        dc.getElementById('load-wishlist-items').innerHTML = '<p class="title" style="text-align:center;"> Wishlist is empty ! </p>'
    }
    
}