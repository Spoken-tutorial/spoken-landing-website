// for smooth scroll effect on nav menu click
function scrollTopAnimated(clicked_link) { 
    elem_class = clicked_link.attr('href');
    scroll_length = $(elem_class).offset().top - $('nav').outerHeight();
            $("html, body").animate({ scrollTop: scroll_length },800); 
        } 

$(document).ready(function(){
  var $container = $('.activities-container');
  window.sr = ScrollReveal();
  // default view - workshops
  $container.isotope({ filter: '.filter-workshop' });
  $('#filter-workshop').css('background-color','#EC6C06');

  // for smooth scroll
  $('.scroll_link').on('click',function(e){
  scrollTopAnimated($(this));
  });

  // filter jobfairs, workshop and internships
  $('#activities-filter a').click(function(){
  var selector = $(this).attr('data-filter');
  var id_div = $(this).attr('data-filter').replace('.','#');
  $('.filter_div').css('background-color','#02073F');
  $(id_div).css('background-color','#EC6C06');
  $container.isotope({ filter: selector });
  return false;

});


$('.navbar-nav>li>a').on('click', function(){
    $('.navbar-collapse').collapse('hide');
});

// scroll effects
  sr.reveal('.navbar', {
          duration: 2000,
          origin:'bottom'
        });

  sr.reveal('.quote .content', {
          duration: 1200,
          origin:'left',
          distance:'200px'
        });

  sr.reveal('.about .content', {
      delay:400,
          duration: 2000,
          origin:'bottom',
          distance:'300px',
          viewFactor: 0.2
        });
   sr.reveal('.applications-grid .box', {
          duration: 500,
          delay: 500,
          origin:'bottom',
          distance:'300px',
          viewFactor: 0.2
        });
    sr.reveal('.activities .h-image', {
          duration: 600,
          delay: 500,
          origin:'left',
          distance:'300px',
          viewFactor: 0.2
        });
     sr.reveal('.activities .a-content', {
          duration: 1000,
          delay: 500,
          origin:'bottom',
          distance:'300px',
          viewFactor: 0.2
        });
     sr.reveal('.collab .content', {
          duration: 700,
          delay: 500,
          origin:'bottom',
          distance:'500px',
          viewFactor: 0.2
        });
     sr.reveal('.contact-wrapper', {
          duration: 700,
          delay: 700,
          origin:'bottom',
          distance:'300px',
          viewFactor: 0.2
        });
   
});
