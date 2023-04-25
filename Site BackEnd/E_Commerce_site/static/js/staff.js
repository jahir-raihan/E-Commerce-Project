// JS for staff panels


// Function for order action
function order_action(action, order_id){

    // Sending request
    let req = $.ajax({
        type:'post',
        url:'/account/pending-order-action/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            action:action,
            order_id:order_id
        }
    });

    // On success
    req.done(function(response){

        // Resetting csrf_token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']

        // Changing buttons / Order item appearance according to action response
        var cancelled_btn = document.getElementById('cancelled-btn'+order_id)
        var confirm_btn = document.getElementById('confirm-btn'+order_id)
        var status = document.getElementById('order-status'+order_id)
        if (response['cancelled']){
            confirm_btn.remove()
            cancelled_btn.remove()
            cancelled_btn.disabled = true
            status.innerHTML = 'Cancelled'

        }else{
            confirm_btn.remove()
            cancelled_btn.remove()
            status.innerHTML = 'Confirmed'
            status.classList.remove('status-pending')
        }
    })
}


// Search pending orders

$(document).on('submit', '#search_pending_order', function(e){

    e.preventDefault()
    document.getElementById('search-loader-staff-main').style.display = 'block'

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '/account/pending-orders/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query:$('#query').val()
        }

    })

    // On success
    req.done(function(response){

        // Updating template
        $('#pending-orders-container').html(response.template)

        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']

        // Hiding loader
        document.getElementById('search-loader-staff-main').style.display = 'none'

    })

})