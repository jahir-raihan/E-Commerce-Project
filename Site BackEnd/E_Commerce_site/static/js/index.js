// Search suggestion and selection

var s_list = document.getElementById('s-list')
all_keywords.forEach((item) => {
    var ele = document.createElement('small')
    ele.innerHTML = item
    s_list.appendChild(ele)
});


try{
const searchInput = document.querySelector("#nav-search");
const listItems = document.querySelectorAll("#s-list small");
var s_r_s = document.getElementById('s-r-s')
searchInput.addEventListener("input", function() {
    s_r_s.classList.remove('d-none')
    const searchTerm = searchInput.value.toLowerCase().trim();

    try{
        // for products page

        search_query = searchTerm
        trigger()
    }catch{}

    var cnt = 0;
    listItems.forEach(function(item) {
        if (item.textContent.toLowerCase().includes(searchTerm) & cnt < 10) {
        item.style.display = "block";
        cnt += 1
        } else {
        item.style.display = "none";
        }
    });
});

searchInput.addEventListener("blur", function() {
    setTimeout(function() {
      s_r_s.classList.add('d-none')
    }, 100);
    
});
  
// Set input value on item click event
listItems.forEach(function(item) {
    item.addEventListener("click", function() {
        searchInput.value = item.textContent;
        window.location.href = 'http://127.0.0.1:8000/products/' + '?s=' + item.textContent
    
    });
});
}catch{}


// End Search suggestion and selection


// Toggle Nav menu

function toggle_nav_menu(){
    var obj = document.getElementById('nav-ham-menu');
    var obj2 = document.getElementById('cross-icon-nav-ham')
    var obj3 = document.getElementById('container')
    var toggle_nav = document.getElementById('toggle-nav')
    if (obj.contains(obj2)){
        obj.innerHTML = '<i class="fa fa-bars" aria-hidden="true"></i>'
        toggle_nav.style.display = 'none'
        try{
            obj3.classList.remove('fade-out')
        }catch{}
    }else{
        obj.innerHTML = '<i id="cross-icon-nav-ham" class="fa fa-times"></i>'
        toggle_nav.style.display = 'block'
        try{
            obj3.classList.add('fade-out')
        }catch{}
        


    }
}

// End Toggle Nav menu

// To change background color of hero



 // array of background colors to cycle through
 var bgColors = ['pink', '#E5E0FF', 'pink', '#F8CBA6', '#AACB73'];

 // get reference to the body element
 const body = document.getElementById('hero');

 // initialize color index
 let colorIndex = 0;

 // set interval to change background color every 1 minute
 setInterval(() => {
   // change background color to next color in array
   try{
    body.style.backgroundColor = bgColors[colorIndex];
   }catch{}
   

   // increment color index, reset to 0 if end of array is reached
   colorIndex = (colorIndex + 1) % bgColors.length;
 }, 5000);
// End change color hero