// Price Range 

let rangeMin = 100;
const range = document.querySelectorAll(".range-selected");
const rangeInput = document.querySelectorAll(".range-input input");
const rangePrice = document.querySelectorAll(".range-price input");


rangeInput.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minRange = parseInt(rangeInput[2].value);
    let maxRange = parseInt(rangeInput[3].value);
    if (maxRange - minRange < rangeMin) {     
      if (e.target.className === "min") {
        rangeInput[2].value = maxRange - rangeMin;        
      } else {
        rangeInput[3].value = minRange + rangeMin;        
      }
    } else {
      rangePrice[2].value = minRange;
      rangePrice[3].value = maxRange;
      range[1].style.left = (minRange / rangeInput[2].max) * 100 + "%";
      range[1].style.right = 100 - (maxRange / rangeInput[3].max) * 100 + "%";
    }

    // Mobile Version

    let minRange1 = parseInt(rangeInput[0].value);
    let maxRange1 = parseInt(rangeInput[1].value);
    if (maxRange1 - minRange1 < rangeMin) {     
      if (e.target.className === "min") {
        rangeInput[0].value = maxRange1 - rangeMin1;        
      } else {
        rangeInput[1].value = minRange1 + rangeMin1;        
      }
    } else {
      rangePrice[0].value = minRange1;
      rangePrice[1].value = maxRange1;
      range[0].style.left = (minRange1 / rangeInput[0].max) * 100 + "%";
      range[0].style.right = 100 - (maxRange1 / rangeInput[1].max) * 100 + "%";
    }
  });
});


rangePrice.forEach((input) => {
  input.addEventListener("input", (e) => {
    let minPrice = rangePrice[2].value;
    let maxPrice = rangePrice[3].value;
    if (maxPrice - minPrice >= rangeMin && maxPrice <= rangeInput[3].max) {
      if (e.target.className === "min") {
        rangeInput[2].value = minPrice;
        range[1].style.left = (minPrice / rangeInput[2].max) * 100 + "%";
      } else {
        rangeInput[3].value = maxPrice;
        range[1].style.right = 100 - (maxPrice / rangeInput[3].max) * 100 + "%";
      }
    }
    
    // Mobile Version
    
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
  });
});

// End Price Range


// Hidden filter 

function enable_hidden_filter(action){
  var obj = document.getElementById('hidden-filter-mobile') 
  var obj3 = document.getElementById('container')
  if (action==true){
    obj.style.display = 'block';
    obj3.classList.add('fade-out')
  }
  else{
    obj.style.display = 'none'
    obj3.classList.remove('fade-out')
  }
 

}

// End Hidden filter