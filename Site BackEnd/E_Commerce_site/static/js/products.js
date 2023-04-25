// Root vars

var  gt = document


// Price Range
let rangeMin = 100;
const range = document.querySelectorAll(".range-selected");
const rangeInput = document.querySelectorAll(".range-input input");
const rangePrice = document.querySelectorAll(".range-price input");


let current_price_range = [0, 10000]; // For tracking current price range


// If price range input is changed , update current_price_range accordingly
rangeInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minRange1 = parseInt(rangeInput[0].value);
    let maxRange1 = parseInt(rangeInput[1].value);
    if (maxRange1 - minRange1 < rangeMin) {     
      if (e.target.className === "min") {
        rangeInput[0].value = maxRange1 - rangeMin;        
      } else {
        rangeInput[1].value = minRange1 + rangeMin;        
      }
    } else {
      rangePrice[0].value = minRange1;
      rangePrice[1].value = maxRange1;
      range[0].style.left = (minRange1 / rangeInput[0].max) * 100 + "%";
      range[0].style.right = 100 - (maxRange1 / rangeInput[1].max) * 100 + "%";
    }
    current_price_range[0] = rangePrice[0].value
    current_price_range[1] = rangePrice[1].value
    trigger()

    // for updating price range in tag
    try{
      gt.getElementById('price-range-tag').remove()
    }
    catch{} 
    var ele = gt.createElement('div')
    ele.setAttribute('id', 'price-range-tag')
    ele.classList.add('tag-btn')
    ele.innerHTML = `<p> Price:  ${current_price_range[0]}$ - ${current_price_range[1]}$ </p>`
    gt.getElementById('tags').appendChild(ele)
    
  });
  
});


rangePrice.forEach((input) => {
  input.addEventListener("input", (e) => {

    let minPrice1 = rangePrice[0].value;
    let maxPrice1 = rangePrice[1].value;
    if (maxPrice1 - minPrice1 >= rangeMin && maxPrice1 <= rangeInput[1].max) {
      if (e.target.className === "min") {
        rangeInput[0].value = minPrice1;
        range[0].style.left = (minPrice1 / rangeInput[0].max) * 100 + "%";
      } else {
        rangeInput[1].value = maxPrice1;
        range[0].style.right = 100 - (maxPrice1 / rangeInput[1].max) * 100 + "%";
      }
    }
    current_price_range[0] = rangePrice[0].value
    current_price_range[1] = rangePrice[1].value
    trigger()
    
  });
  
});

// End Price Range


// Hidden filter -> Process was simple
// step1 -> If current screen size <= 775px we just cut and paste desktop filter section to mobile filter section
// Again -> If current screen size > 775px we cut mobile filter section and paste it to desktop filter section

// The reason we're cutting because it will cause error if two elements are having save ids

function enable_hidden_filter(action){

  // Was complex enough to think about it.

  var obj = document.getElementById('hidden-filter-mobile') 
  var main_filter_container = gt.getElementById('main-filter-container')
  var filter_contents = gt.getElementById('filter-contents')
  var obj3 = document.getElementById('container')
  var close_filter = gt.getElementById('close-filter')
  try{

      if (action==true){
        obj.style.display = 'block';
        obj.appendChild(filter_contents)
        console.log(main_filter_container.children)
        obj3.classList.add('fade-out')
        close_filter.classList.remove('d-none')
      }
      else{
        main_filter_container.appendChild(filter_contents);

        obj.style.display = 'none'
        obj3.classList.remove('fade-out')

        close_filter.classList.add('d-none')
      }
  }catch{}
 

}

window.onresize = function(){
  if (screen.width > 775){
    enable_hidden_filter(false)
  }
}


// End Hidden filter



// To update tags and refinements

let refinements = new Set(); // Set for storing tags and tracking tags



// Getting all tags , and initializing their id as 1

let filter_box = document.querySelectorAll('.filter-box');
let counter = 1;

// If any tag checkbox is checked or unchecked , this function will invoke and will add or remove tags

filter_box.forEach((item) => {
  item.addEventListener('click', function(){
    var child = item.children[0].children
    var refinements_list = gt.getElementById('refinements')

    if (child[2].checked && !refinements.has(child[0].innerHTML)){
      
      var new_ref = gt.createElement('div')
      new_ref.classList.add('tag-btn')
      new_ref.classList.add('refinements-p')
      new_ref.setAttribute('id', `ref-${counter}`)
      new_ref.innerHTML = `<p id="${counter}"> ${child[0].innerHTML}
                          </p><div class="cross" onclick="del_refinements(${counter})">&#x2715;</div>`
      refinements_list.appendChild(new_ref)
      refinements.add(child[0].innerHTML)
      counter += 1
      trigger()
    } 
    else if (child[2].checked && refinements.has(child[0].innerHTML)){
      var tmp = gt.querySelectorAll('.refinements-p p')
      var itm_to_remove = '';
      tmp.forEach ((item) => {
        if (item.textContent.trim() === child[0].textContent.trim()){
          itm_to_remove = item.id
        }
      })
      gt.getElementById('ref-'+itm_to_remove).remove()
      refinements.delete(child[0].innerHTML)
      trigger()
      
    }


  })
})


// For deleting tags from the tags list . 

function del_refinements(id){
  var tmp_txt = gt.getElementById('ref-'+id).children[0].textContent.trim()
  gt.getElementById('ref-'+id).remove()
  refinements.delete(tmp_txt)
  var refinements_input_check_box = gt.querySelectorAll('.refinements-input-checkbox')
  refinements_input_check_box.forEach( (item) => {
    if (tmp_txt === item.children[0].textContent.trim()){
      item.children[2].checked = false
    }

  })
  trigger()

}

// Function for clearing refinements
function clear_refinements(){

  var refinements = gt.querySelectorAll('.refinements-p')
  refinements.forEach( (item) => {
    del_refinements(item.id.split('-')[1])
  })
  trigger()
}
// End tags and refinements


// category filter 

var categories = gt.querySelectorAll('.category')
var current_category = ''
categories.forEach( (item) => {

  item.addEventListener('click', function(){

    var sub_itm = gt.querySelectorAll('.category')
    sub_itm.forEach( (sub_item) => {
      sub_item.classList.remove('selected')
    })
    try{
      gt.getElementById('cat-tag').remove()
    }
    catch{}
    if (current_category !== item.getAttribute('cat_id')){
        var ele = gt.createElement('div')
        ele.setAttribute('id', 'cat-tag')
        ele.classList.add('tag-btn')
        current_category = item.getAttribute('cat_id')
        ele.innerHTML = `<p> ${item.innerHTML} </p>`;
        gt.getElementById('tags').appendChild(ele)
        item.classList.add('selected')
    }else{
        try{document.getElementById('cat-tag').remove()}catch{}


        item.classList.remove('selected')
        current_category = ''
    }


    trigger()
    
  })

})

// end category filter

// sort by price 

let sort_by_price = false
function change_sorting(){
  var sort_icon = gt.getElementById('sort-icon')
  if (sort_by_price){
    sort_icon.classList.remove('fa-sort')
    sort_icon.classList.add('fa-sort-up')
    sort_by_price = false

  }
  else{
    sort_icon.classList.remove('fa-sort')
    sort_icon.classList.remove('fa-sort-up')
    sort_icon.classList.add('fa-sort-down')
    sort_by_price = true

  }
  trigger()
}

// end sort by price

// Offerings
let offerings_set = new Set();

let offerings = gt.querySelectorAll('.offerings-checkbox')
var counter_tag = 1;
offerings.forEach( (item) => {

  item.addEventListener('click', function(){
    var child = item.children
    var tags_list = gt.getElementById('tags')

    if (child[1].checked && !offerings_set.has(child[0].innerHTML)){
      
      var new_tag = gt.createElement('div')
      new_tag.classList.add('tag-btn')
      new_tag.classList.add('tags-p')
      new_tag.setAttribute('id', `tag-${counter_tag}`)
      new_tag.innerHTML = `<p id="${counter_tag}"> ${child[0].innerHTML}
                          </p><div class="cross" onclick="del_tags(${counter_tag})">&#x2715;</div>`
      tags_list.appendChild(new_tag)
      offerings_set.add(child[0].innerHTML)
      counter_tag += 1
      trigger()
    } 
    else if (child[1].checked && offerings_set.has(child[0].innerHTML)){
      var tmp = gt.querySelectorAll('.tags-p p')
      var itm_to_remove = '';
      tmp.forEach ((item) => {
        if (item.textContent.trim() === child[0].textContent.trim()){
          itm_to_remove = item.id
        }
      })
      gt.getElementById('tag-'+itm_to_remove).remove()
      offerings_set.delete(child[0].innerHTML)
      trigger()

      
    }


  })

})


// Function to delete tags
function del_tags(id){
  var tmp_txt = gt.getElementById('tag-'+id).children[0].textContent.trim()
  gt.getElementById('tag-'+id).remove()
  offerings_set.delete(tmp_txt)
  var tags_input_check_box = gt.querySelectorAll('.offerings-checkbox')
  tags_input_check_box.forEach( (item) => {
    if (tmp_txt === item.children[0].textContent.trim()){
      item.children[1].checked = false

    }
   


  })
  trigger()

}


// End offerings


// Search query from other pages

var search_query = search_query;
function del_s_q(){
    document.getElementById('search-query-tag').remove()

    window.location.href = 'http://127.0.0.1:8000/products/'
    search_query = '';
    trigger()

}

// End Search query

// Trigger section, it will be responsible for filtering out the page 

function trigger(){
    gt.getElementById('loader-product-page').style.display = 'block'

    // Sending request
    let req = $.ajax({
        type:'post',
        url:'/products/',
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            search_query:search_query,
            offerings: Array.from(offerings_set),
            sort_by_price:sort_by_price,
            current_category:current_category,
            refinements: Array.from(refinements),
            price_range: current_price_range



        }

    })

    // On success
    req.done(function(response){
        // Update product template
        gt.getElementById('loader-product-page').style.display = 'none'
        $('#products-grid').html(response.template)

        // Resetting csrf token
        var token  = document.getElementsByName('csrfmiddlewaretoken')[0]
        token.value = response['token']
    })

}

// End Trigger section