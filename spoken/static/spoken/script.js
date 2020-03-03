function scrollTopAnimated(clicked_link) { 
    // elem_class = clicked_link.attr('href').replace('#','.');
    elem_class = clicked_link.attr('href');
    console.log(elem_class);
    console.log($(elem_class).offset().top);
    console.log($('nav').outerHeight());
    scroll_length = $(elem_class).offset().top - $('nav').outerHeight();
    console.log(scroll_length);
            $("html, body").animate({ scrollTop: scroll_length },800); 
        } 



$(document).ready(function(){
  console.log('js working ....');
  
  // console.log(slider);
  var $container = $('.activities-container');

  window.sr = ScrollReveal();
  console.log('start');
  console.log(sr);
// intial show only jobfairs
  $container.isotope({ filter: '.filter-workshop' });
  $('#filter-workshop').css('background-color','#ed125b');

  $('.scroll_link').on('click',function(e){
    console.log($('nav').outerHeight());
    scrollTopAnimated($(this));
  });

  
  $('#activities-filter a').click(function(){
    console.log('clicked');
  var selector = $(this).attr('data-filter');
  var id_div = $(this).attr('data-filter').replace('.','#');
  $('.filter_div').css('background-color','#02073F');
  $(id_div).css('background-color','#ed125b');
  $container.isotope({ filter: selector });

  console.log($container);
  console.log(selector);


  return false;

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
