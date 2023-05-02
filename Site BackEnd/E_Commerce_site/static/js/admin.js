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

// Admin edit products


try{
    var product_id = $('#product_id').val()
}catch{
    var product_id = ''
}

// This function is a overloaded function which works on two different criteria if -> Add a product it's sends a add
// request , if -> Edit a product , it sends a edit product request to the backend.

$(document).on('submit', '#add-a-product'+product_id, function(e){

    // Preventing from  loading  the page on submit
    e.preventDefault();

    // Getting form data
    var formData = new FormData($('#add-a-product'+product_id).get(0))

    // Some functional checking ->
        // If Edit product -> and no category is chosen pop up a required message
        // If On discount is checked -> Mark all discount inputs as required

    var category = $('#category')
    var category_new = $('#category_new')
    var discount = document.getElementById('on_discount')
    var discount_reason = $('#discount_reason')
    var discount_reason_new = $('#discount_reason_new')
    if (category.val() === '' && category_new.val() === ''){
        alert('Category cannot be empty !')
    } else if (discount.checked && discount_reason.val() === '' && discount_reason_new.val() === ''){
        alert('Discount reason cannot be empty !')
    } else {
        var btn = document.getElementById('product_save_btn')
        btn.innerHTML = 'Saving <i id="l-i" class="fa fa-spinner fa-spin"></i>'

        // Determining URL by Edit or Add product behavior
        let url = '/account/admin/add-edit-product/'
        if (product_id !== ''){
            url += product_id+'/'
        }

        // Sending request
        let req = $.ajax({
            type:'post',
            url: url,
            data: formData,
            cache: false,
            processData: false,
            contentType: false,

        });

        // On request success
        req.done(function(response){

            // Resetting form
            try{
                if ('success' in response &&  response['edit'] == false){
                    $( '#add-a-product' ).each(function(){
                        this.reset();
                    });

                    // Resetting image preview
                    var preview = document.querySelector('#image-preview')
                    preview.innerHTML = ''

                } else if ('success' in response && response['edit'] == true){
                    document.getElementById('success-msg-p').innerHTML = 'Updated successfully'
                }
            }catch{ location.reload()}

            // Showing message and resetting csrf token
            btn.innerHTML = 'Save'
            var msg = document.getElementById('success-msg')
            msg.style.display = 'block'

            var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
            token.value = response['token']
            setTimeout(() => {msg.style.display='none'}, 4000);

        });
        return
    }

})

