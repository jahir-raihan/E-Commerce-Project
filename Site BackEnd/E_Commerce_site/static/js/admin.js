$(document).on('submit', '#search_admin_products', function(e){
    e.preventDefault();

    let req = $.ajax({
        type:'post',
        url: '/account/admin/product-list/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query:$('#query').val()
        }
    })
    req.done(function(response){
        $('#admin_products_grid').html(response.template)

        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})


$(document).on('submit', '#admin-transaction-search', function(e){

    e.preventDefault()

    let req = $.ajax({
        type:'post',
        url: '',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query:$('#query').val()
        }
    })
    req.done(function(response){
        $('#transaction-list').html(response.template)

        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})