// Root vars 

var  gt = document
// Price Range 


let rangeMin = 100;
const range = document.querySelectorAll(".range-selected");
const rangeInput = document.querySelectorAll(".range-input input");
const rangePrice = document.querySelectorAll(".range-price input");


let current_price_range = [0, 10000]; // For tracking current price range

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

    // for updaing price range in tag
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
    
  });
  
});

// End Price Range


// Hidden filter 

function enable_hidden_filter(action){

  // Was complex enough to think about it.

  var obj = document.getElementById('hidden-filter-mobile') 
  var main_filter_container = gt.getElementById('main-filter-container')
  var filter_contents = gt.getElementById('filter-contents')
  var obj3 = document.getElementById('container')
  var close_filter = gt.getElementById('close-filter')

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
 

}

window.onresize = function(){
  if (screen.width > 775){
    enable_hidden_filter(false)
  }
}

// End Hidden filter



// To update tags and refinements

let refienments = new Set(); // Set for storing tags and tracking tags



// Getting all tags , and initializing their id as 1

let filter_box = document.querySelectorAll('.filter-box');
let counter = 1;

// If any tag checkbox is checked or unchecked , this function will invoke and will add or remove tags

filter_box.forEach((item) => {
  item.addEventListener('click', function(){
    var child = item.children[0].children
    var refinements_list = gt.getElementById('refinements')

    if (child[2].checked && !refienments.has(child[0].innerHTML)){
      
      var new_ref = gt.createElement('div')
      new_ref.classList.add('tag-btn')
      new_ref.classList.add('refinements-p')
      new_ref.setAttribute('id', `ref-${counter}`)
      new_ref.innerHTML = `<p id="${counter}"> ${child[0].innerHTML}
                          </p><div class="cross" onclick="del_refinements(${counter})">&#x2715;</div>`
      refinements_list.appendChild(new_ref)
      refienments.add(child[0].innerHTML)
      counter += 1
    } 
    else if (child[2].checked && refienments.has(child[0].innerHTML)){
      var tmp = gt.querySelectorAll('.refinements-p p')
      var itm_to_remove = '';
      tmp.forEach ((item) => {
        if (item.textContent.trim() === child[0].textContent.trim()){
          itm_to_remove = item.id
        }
      })
      gt.getElementById('ref-'+itm_to_remove).remove()
      refienments.delete(child[0].innerHTML)
      
    }


  })
})


// For deleting tags from the tags list . 

function del_refinements(id){
  var tmp_txt = gt.getElementById('ref-'+id).children[0].textContent.trim()
  gt.getElementById('ref-'+id).remove()
  refienments.delete(tmp_txt)
  var refinements_input_check_box = gt.querySelectorAll('.refinements-input-checkbox')
  refinements_input_check_box.forEach( (item) => {
    if (tmp_txt === item.children[0].textContent.trim()){
      item.children[2].checked = false
    }
   
    // solved

  })

}

function clear_refinements(){

  var refinements = gt.querySelectorAll('.refinements-p')
  refinements.forEach( (item) => {
    del_refinements(item.id.split('-')[1])
  })
}
// End tags and refienments


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
    var ele = gt.createElement('div')
    ele.setAttribute('id', 'cat-tag')
    ele.classList.add('tag-btn')
    current_category = item.textContent.trim()
    ele.innerHTML = `<p> ${current_category} </p>`;
    gt.getElementById('tags').appendChild(ele)
    item.classList.add('selected')
    
    
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
}

// end sort by price

// Offerings
let offerrings_set = new Set();

let offerrings = gt.querySelectorAll('.offerings-checkbox')
var counter_tag = 1;
offerrings.forEach( (item) => {

  item.addEventListener('click', function(){
    var child = item.children
    var tags_list = gt.getElementById('tags')

    if (child[1].checked && !offerrings_set.has(child[0].innerHTML)){
      
      var new_tag = gt.createElement('div')
      new_tag.classList.add('tag-btn')
      new_tag.classList.add('tags-p')
      new_tag.setAttribute('id', `tag-${counter_tag}`)
      new_tag.innerHTML = `<p id="${counter_tag}"> ${child[0].innerHTML}
                          </p><div class="cross" onclick="del_tags(${counter_tag})">&#x2715;</div>`
      tags_list.appendChild(new_tag)
      offerrings_set.add(child[0].innerHTML)
      counter_tag += 1
    } 
    else if (child[1].checked && offerrings_set.has(child[0].innerHTML)){
      var tmp = gt.querySelectorAll('.tags-p p')
      var itm_to_remove = '';
      tmp.forEach ((item) => {
        if (item.textContent.trim() === child[0].textContent.trim()){
          itm_to_remove = item.id
        }
      })
      gt.getElementById('tag-'+itm_to_remove).remove()
      offerrings_set.delete(child[0].innerHTML)
      
    }


  })

})

function del_tags(id){
  var tmp_txt = gt.getElementById('tag-'+id).children[0].textContent.trim()
  gt.getElementById('tag-'+id).remove()
  offerrings_set.delete(tmp_txt)
  var tags_input_check_box = gt.querySelectorAll('.offerings-checkbox')
  tags_input_check_box.forEach( (item) => {
    if (tmp_txt === item.children[0].textContent.trim()){
      item.children[1].checked = false
    }
   
    // solved

  })

}


// End offerings

// Rating 



// End Rating 

// Trigger section, it will be responsible for filtering out the page 

function trigger(){

  // Do anything here.
}

// End Trigger section