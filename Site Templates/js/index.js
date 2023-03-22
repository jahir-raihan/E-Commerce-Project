// Search suggestion and selection

const searchInput = document.querySelector("#nav-search");
const listItems = document.querySelectorAll("#s-list a");
var s_r_s = document.getElementById('s-r-s')
searchInput.addEventListener("input", function() {
    s_r_s.classList.remove('d-none')
    const searchTerm = searchInput.value.toLowerCase().trim();
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
    
    });
});


// End Search suggestion and selection


// Toggle Nav menu

function toggle_nav_menu(){
    var obj = document.getElementById('nav-ham-menu');
    var obj2 = document.getElementById('cross-icon-nav-ham')
    var toggle_nav = document.getElementById('toggle-nav')
    if (obj.contains(obj2)){
        obj.innerHTML = '<img src="/img/menu.png" alt="">'
        toggle_nav.style.display = 'none'
    }else{
        obj.innerHTML = '<i id="cross-icon-nav-ham" class="fa fa-times"></i>'
        toggle_nav.style.display = 'block'


    }
}

// End Toggle Nav menu

// To change background color of hero



 // array of background colors to cycle through
 const bgColors = ['pink', '#E5E0FF', 'pink', '#F8CBA6', '#AACB73'];

 // get reference to the body element
 const body = document.getElementById('hero');

 // initialize color index
 let colorIndex = 0;

 // set interval to change background color every 1 minute
 setInterval(() => {
   // change background color to next color in array
   body.style.backgroundColor = bgColors[colorIndex];

   // increment color index, reset to 0 if end of array is reached
   colorIndex = (colorIndex + 1) % bgColors.length;
 }, 5000);
// End change color hero