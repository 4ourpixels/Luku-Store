function storeParalax() {
  window.addEventListener("scroll", function () {
    var parallaxImage = document.getElementById("parallax-image");
    var scrollPosition = window.pageYOffset;
    var imagePosition = parallaxImage.offsetTop;

    if (scrollPosition > imagePosition - window.innerHeight) {
      var distance = scrollPosition - imagePosition;
      parallaxImage.style.opacity = 1 - distance / (window.innerHeight * 0.8);
    } else {
      parallaxImage.style.opacity = 1;
    }
  });
}
storeParalax();

export default storeParalax;
