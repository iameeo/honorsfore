for(let i=0; i<30; i++){
    $(".gallery").append("<div class=\"gallery-item\" data-imgurl=\"https://picsum.photos/500/500?v="+i+"\" style=\"background: url('https://picsum.photos/500/500?v="+i+"') center center / 150% no-repeat #fff;\"></div>");
}

const modal = document.getElementById("myModal");
const modalImg = document.getElementById("modal-img");

const images = document.querySelectorAll(".gallery-item");
images.forEach(function(img) {
    img.onclick = function() {
        modal.style.display = "flex";
        modalImg.src = this.getAttribute("data-imgurl");
    }
});

const span = document.getElementsByClassName("close")[0];
span.onclick = function() { 
    modal.style.display = "none";
}