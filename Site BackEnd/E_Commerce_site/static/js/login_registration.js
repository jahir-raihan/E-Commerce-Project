let ls = localStorage
let dc = document
$(document).on('submit', '#login-form', function(e){

    e.preventDefault();

    let redirect_url, cart_items, wishlist_items;
    let login_btn = dc.querySelector('.login-btn')

    // Login btn React on submit

    login_btn.disabled =  true
    login_btn.style.cursor = 'progress'
    login_btn.style.opacity = '.8'
    let l_t = dc.getElementById('l-t')
    l_t.innerHTML = 'Memorising'
    dc.getElementById('l-i').classList.remove('d-none')



    // Checking for local storage data

    const keys = Object.keys(ls);
    if (keys.includes('cart_items')){
        cart_items = Json.parse(ls.getItem('cart_items'));
    }
    if (keys.includes('wishlist_items')){
        wishlist_items = Json.parse(ls.getItem('wishlist_items'))
    }
    if (keys.includes('redirect_url')){
        redirect_url = ls.getItem('redirect_url')
    }


    // Request

    let req = $.ajax({
        type:'post',
        url:'/account/login/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email:$('#email').val(),
            password:$('#password-input').val(),
            cart_items:cart_items,
            wishlist_items:wishlist_items,
            redirect_url:redirect_url

        }
    });
    setTimeout(() => {l_t.innerHTML = 'Logging in . .' }, 300);



    req.done(function(data){
        if ('success' in data){
            // reinitializing login button

            setTimeout(() => {l_t.innerHTML = 'Redirecting' }, 200);
            l_t.innerHTML = 'Login'
            dc.getElementById('l-i').classList.add('d-none')

            // Redirecting

            window.location.href = data['redirect']

        }
        else if ('error' in data) {

            // If Account not found , show some alert on the window and reset the buttons

            l_t.innerHTML = 'Login'
            dc.getElementById('l-i').classList.add('d-none')
            login_btn.disabled = false
            login_btn.style.cursor = 'pointer'
            alert('Account Not Found!') ? "" : location.reload();
        }

    })


})


