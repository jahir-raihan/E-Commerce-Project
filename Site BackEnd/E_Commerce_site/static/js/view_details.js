let dc = document
// Image gallery 


// Image gallery -> This function is responsible for showing images in products detials page
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

// End Image gallery


// For review stars

// ---- ---- Const ---- ---- //
const stars = document.querySelectorAll('.stars i');
const starsNone = document.querySelector('.rating-box');
let current_stars = 1;
// ---- ---- Stars ---- ---- //
stars.forEach((star, index1) => {
  star.addEventListener('click', () => {
    current_stars = star.getAttribute('val')
    stars.forEach((star, index2) => {
      // ---- ---- Active Star ---- ---- //
      index1 >= index2
        ? star.classList.add('active')
        : star.classList.remove('active');
    });
  });
});

// End review stars


// For updating quantity

let quantity = 1; // Default value is 1
let q_btns = dc.querySelectorAll('.q-input button')
q_btns.forEach( (btn) => {
  btn.addEventListener( 'click', function(){

    if (btn.classList[0] == 'plus' && quantity < 20){
      quantity += 1
    }
    else if (btn.classList[0] == 'minus' && quantity > 1){
      quantity -= 1
    }
    dc.getElementById('q-count').innerHTML = quantity;
  })
})


// Reviews and rating section


// Writing review section
function write_review(value, user, id){

    // Only allow registered users to write review
    if ((user !== 'AnonymousUser') && (!users_reviewed.includes(id))){
        dc.getElementById('w-a-r-p-s').style.display='block'
    }

}


// Reviews request

$(document).on('submit', '#review_form', function(e){
    e.preventDefault();

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '/review/'+$(this).attr('p_id')+'/',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            review_text: $('#review_text').val(),
            rating: current_stars,

        }
    });

    // On success
    req.done(function(response){

        // Updating html
        dc.getElementById('w-a-r-p-s').style.display='none'
        $('#review_section').html(response.template)

        // Resetting token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})

// Reviews Replays

$(document).on('submit', '#write-reply', function(e){
    e.preventDefault();

    // Sending request
    let req = $.ajax({
        type:'post',
        url: '/replay/'+$(this).attr('r_id')+'/',
        data: {
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            replay_text: $('#replay_text').val()

        }
    });

    // On success
    req.done(function(response){

        // Updating template
        dc.getElementById('write-reply').style.display='none'
        $('#review_section').html(response.template)

        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })
})


// Show all reviews

function show_all_reviews(id){
    let req = $.ajax({
        type:'get',
        url:'/get-all-review/'+id+'/',
        data:{
        }
    })

    req.done(function(response){

        // Replacing review section of a products
        $('#review_section').html(response)
    })
}