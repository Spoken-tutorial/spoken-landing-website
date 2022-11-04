
  $( ".student_check" ).click(function() {
    alert( "Handler for .click() called." );
  });

  
  function myFunc(){
    alert('he')
    onchange="this.form.submit()"

  }

  $('#select_test').on('change', function(){
    // alert('c');
    $(this).closest('form').submit();
});