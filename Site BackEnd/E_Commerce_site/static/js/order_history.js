// Search query request

$(document).on('submit', '#order_history_search', function(e){

    e.preventDefault()
    let req = $.ajax({
        type:'post',
        url: '/account/query-order-history/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query: $('#search_query').val()
        }
    });
    req.done(function(response){
        $('#order-history-container').html(response.template)
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})