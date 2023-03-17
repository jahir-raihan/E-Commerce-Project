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

document.querySelector('input[type="file"]').addEventListener("change", previewImages);
