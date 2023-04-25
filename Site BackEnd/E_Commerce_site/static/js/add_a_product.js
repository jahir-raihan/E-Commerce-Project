
// Function to preview selected images in Add a product template

function previewImages() {
                                
    var preview = document.querySelector('#image-preview');
    preview.innerHTML = ''
    if (this.files) {
    [].forEach.call(this.files, readAndPreview);
    }

    function readAndPreview(file) {
    // Make sure `file.name` matches our extensions criteria
    if (!/\.(jpe?g|png|gif)$/i.test(file.name)) {
        return alert(file.name + " is not an image");
    } // else...

    var reader = new FileReader();

    reader.addEventListener("load", function() {
        var image = new Image();
        image.height = 80
        image.title = file.name;
        image.src = this.result;
        preview.appendChild(image);
    });

    reader.readAsDataURL(file);
    }
}


// Event Listener for preview image
document.querySelector('#images').addEventListener("change", previewImages);


// Add Or Edit product request


// Discount reason checkbox function

var checkbox = document.querySelector('#on_discount')

checkbox.addEventListener('change', ()=> {
    if (checkbox.checked){
        document.getElementById('discount_percentage').required = true
        document.getElementById('discount_expiry').required = true
    }
    else{
        document.getElementById('discount_percentage').required = false
        document.getElementById('discount_expiry').required = false
    }
})

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
        let url = '/account/add-edit-products/'
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