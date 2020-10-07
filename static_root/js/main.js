// js to toggle-menu
var Items = document.getElementById("menu-items");

Items.style.maxHeight = "0px"
function togglemenu(){
    if(Items.style.maxHeight == "0px"){
        Items.style.maxHeight = "200px";
    }
    else{
        Items.style.maxHeight = "0px";
    }
}

//js for product images
var mainImg = document.getElementById("mainImg");
var smallImg = document.getElementsByClassName("smallImg");

for (let i = 0; i < smallImg.length; i++) {
    
    smallImg[i].onclick = function () {
        temp = mainImg.src
        mainImg.src = smallImg[i].src
        smallImg[i].src = temp
    }    
}
