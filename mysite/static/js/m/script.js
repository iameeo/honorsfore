// Add gallery items
for (let i = 0; i < 30; i++) {
    const imgUrl = `https://picsum.photos/500/500?v=${i}`;
    const galleryItem = `
        <div class="gallery-item" data-imgurl="${imgUrl}" style="background: url('${imgUrl}') center center / 150% no-repeat #fff;"></div>
    `;
    $(".gallery").append(galleryItem);
}

// Modal elements
const modal = document.getElementById("myModal");
const modalImg = document.getElementById("modal-img");
const closeBtn = document.querySelector(".close");

// Open modal when a gallery item is clicked
document.querySelectorAll(".gallery-item").forEach(img => {
    img.addEventListener("click", () => {
        modal.style.display = "flex";
        modalImg.src = img.getAttribute("data-imgurl");
    });
});

// Close modal when the close button is clicked
closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
});