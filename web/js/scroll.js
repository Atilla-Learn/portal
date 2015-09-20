$(document).ready(function(){
  $('#topbutton').click(function(){
    $('html, body').animate({
           scrollTop: 790
       }, 800);
  });
  $('ul.tabs').tabs();
});
