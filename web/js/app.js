document.querySelector('.share-twitter').addEventListener('click', function(e){
  e.preventDefault();
  var url = this.getAttribute('data-url');
  var shareurl = "https://twitter.com/intent/tweet?text=" +
    encodeURIComponent(document.title) + "&via=CY106" +
    "&url=" + encodeURIComponent(url);
  window.open(shareurl, "Partage", 'scrollbar=yes, width=640, height=340, top=0, left=0');
})

document.querySelector('.share-fb').addEventListener('click', function(e){
  e.preventDefault();
  var url = this.getAttribute('data-url');
  var shareurl = "https://facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url);
  window.open(shareurl, "Partage", 'scrollbar=yes, width=640, height=340, top=0, left=0');
})

document.querySelector('.share-gp').addEventListener('click', function(e){
  e.preventDefault();
  var url = this.getAttribute('data-url');
  var shareurl = "https://plus.google.com/share?url=" + encodeURIComponent(url);
  window.open(shareurl, "Partage", 'scrollbar=yes, width=640, height=340, top=0, left=0');
})

document.querySelector('.share-linkedin').addEventListener('click', function(e){
  e.preventDefault();
  var url = this.getAttribute('data-url');
  var shareurl = "https://linkedin.com/shareArticle?url=" + encodeURIComponent(url);
  window.open(shareurl, "Partage", 'scrollbar=yes, width=640, height=340, top=0, left=0');
})
