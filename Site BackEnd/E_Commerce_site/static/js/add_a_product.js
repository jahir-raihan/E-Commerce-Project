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

document.querySelector('#images').addEventListener("change", previewImages);

var data = null;

// Add a product form request

$(document).on('submit', '#add-a-product', function(e){

    e.preventDefault();
    var formData = new FormData($('#add-a-product').get(0))
    data = formData
    console.log(formData)

    var btn = document.getElementById('product_save_btn')
    btn.innerHTML = 'Saving <i id="l-i" class="fa fa-spinner fa-spin"></i>'
    let req = $.ajax({
        type:'post',
        url: '/account/add-products/',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,

    });
    req.done(function(response){

        if ('success' in response &&  response['edit'] == false){
            $( '#add-a-product' ).each(function(){
                this.reset();
            });
            btn.innerHTML = 'Save'
            var msg = document.getElementById('success-msg')
            msg.style.display = 'block'
            var preview = document.querySelector('#image-preview')
            preview.innerHTML = ''



            // Reset CSRF token

            var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
            token.value = response['token']


            setTimeout(() => {msg.style.display='none'}, 3000);


        }


    })



})