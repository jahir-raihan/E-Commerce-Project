// Order history Search query request

$(document).on('submit', '#order_history_search', function(e){

    e.preventDefault()

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '/account/query-order-history/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            query: $('#search_query').val()
        }
    });

    // On success
    req.done(function(response){
        // Updating template
        $('#order-history-container').html(response.template)

        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})