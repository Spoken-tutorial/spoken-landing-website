// for smooth scroll effect on nav menu click
var FOSS_RESULT;
function scrollTopAnimated(clicked_link) { 
    elem_class = clicked_link.attr('href');
    scroll_length = $(elem_class).offset().top - document.getElementById("logo").offsetHeight-70;
    $("html, body").animate({ scrollTop: scroll_length },800); 
        }

function setLanguage(){
  foss = $( "#foss_select option:selected" ).text();

  foss_obj = FOSS_RESULT.find(x => x.foss === foss);
  languages = foss_obj["languages"];
  $('#lang_select').html('');
  for (i = 0; i < languages.length; i++) {
  s = "<option value="+languages[i]+">"+languages[i]+"</option>";
  $('#lang_select').append(s);
  }
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
  $('#activities-filter button').click(function(){
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

$.ajax({url: "/spoken/api/tutorial-search/", success: function(result){
    FOSS_RESULT = result["foss_lang_list"];
    for (i = 0; i < FOSS_RESULT.length; i++) {
      f = FOSS_RESULT[i].foss;
      s = '<option value="'+f+'">'+f+'</option>';
      $('#foss_select').append(s);
  }
    setLanguage();

  }});

$( "#foss_select" ).change(function() {
    setLanguage();
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
