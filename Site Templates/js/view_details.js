function showImage(imageId) {
    // Get all the images in the gallery
    var images = document.getElementsByClassName("img-gallery-img");

    // Remove the "selected" class from all the images
    for (var i = 0; i < images.length; i++) {
        images[i].classList.remove("selected");
    }

    // Add the "selected" class to the clicked image
    var selectedImage = document.getElementById(imageId);
    var add_border = document.getElementById("img-gallery-img"+imageId)
    add_border.classList.add("selected");

    // Update the full-size image with the clicked image
    var fullSizeImage = document.getElementById("selected-image");
    fullSizeImage.src = selectedImage.src;
    fullSizeImage.alt = selectedImage.alt;
}


// ---- ---- Const ---- ---- //
const stars = document.querySelectorAll('.stars i');
const starsNone = document.querySelector('.rating-box');

// ---- ---- Stars ---- ---- //
stars.forEach((star, index1) => {
  star.addEventListener('click', () => {
    stars.forEach((star, index2) => {
      // ---- ---- Active Star ---- ---- //
      index1 >= index2
        ? star.classList.add('active')
        : star.classList.remove('active');
    });
  });
});