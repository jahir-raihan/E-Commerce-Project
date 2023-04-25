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