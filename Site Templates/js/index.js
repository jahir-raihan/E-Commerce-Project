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