// Search request for admin panel -> Products
$(document).on('submit', '#search_admin_products', function(e){
    e.preventDefault();

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '/account/admin/product-list/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query:$('#query').val()
        }
    })

    // On success
    req.done(function(response){

        // Updating products template
        $('#admin_products_grid').html(response.template)


        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})


// Search request for admin panel -> Transactions
$(document).on('submit', '#admin-transaction-search', function(e){

    e.preventDefault()

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query:$('#query').val()
        }
    })

    // On success
    req.done(function(response){

        // Updating transaction list template
        $('#transaction-list').html(response.template)

        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})

// Admin search pending orders


$(document).on('submit', '#admin_search_pending_order', function(e){

    e.preventDefault()
    document.getElementById('search-loader-staff-main').style.display = 'block'

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '/account/admin/orders/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query:$('#query').val()
        }

    })

    // On success
    req.done(function(response){

        // Updating template
        $('#pending-orders-container-admin').html(response.template)

        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']

        // Hiding loader
        document.getElementById('search-loader-staff-main').style.display = 'none'

    })

})