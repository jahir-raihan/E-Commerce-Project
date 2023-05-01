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


//// Analytics
//
//const ctx = document.getElementById('myChart');
//
//new Chart(ctx, {
//    type: 'bar',
//    data: {
//        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//        datasets: [{
//            label: '# of Votes',
//            data: [12, 19, 3, 5, 2, 3],
//            backgroundColor: [
//              'rgba(255, 99, 132, 0.2)',
//              'rgba(255, 159, 64, 0.2)',
//              'rgba(255, 205, 86, 0.2)',
//              'rgba(75, 192, 192, 0.2)',
//              'rgba(54, 162, 235, 0.2)',
//              'rgba(153, 102, 255, 0.2)',
//              'rgba(201, 203, 207, 0.2)'
//            ],
//            borderColor: [
//              'rgb(255, 99, 132)',
//              'rgb(255, 159, 64)',
//              'rgb(255, 205, 86)',
//              'rgb(75, 192, 192)',
//              'rgb(54, 162, 235)',
//              'rgb(153, 102, 255)',
//              'rgb(201, 203, 207)'
//            ],
//
//            borderWidth: 1
//        }]
//    },
//    options: {
//        scales: {
//            y: {
//              beginAtZero: true
//            }
//        }
//    }
//});
//
//// Polar area chart
//
//const ctx1 = document.getElementById('myChart1');
//
//new Chart(ctx1, {
//    type: 'polarArea',
//    data: {
//        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//        datasets: [{
//            label: '# of Votes',
//            data: [12, 19, 3, 5, 2, 3],
//            backgroundColor: [
//              'rgba(255, 99, 132, 0.2)',
//              'rgba(255, 159, 64, 0.2)',
//              'rgba(255, 205, 86, 0.2)',
//              'rgba(75, 192, 192, 0.2)',
//              'rgba(54, 162, 235, 0.2)',
//              'rgba(153, 102, 255, 0.2)',
//              'rgba(201, 203, 207, 0.2)'
//            ],
//            borderColor: [
//              'rgb(255, 99, 132)',
//              'rgb(255, 159, 64)',
//              'rgb(255, 205, 86)',
//              'rgb(75, 192, 192)',
//              'rgb(54, 162, 235)',
//              'rgb(153, 102, 255)',
//              'rgb(201, 203, 207)'
//            ],
//
//            borderWidth: 1
//        }]
//    },
//    options: {
//        scales: {
//            y: {
//              beginAtZero: true
//            }
//        }
//    }
//});