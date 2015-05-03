(function($){
  $(function(){

    $('.button-collapse').sideNav();

    $('select').material_select();

    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 3, // Creates a dropdown to control year
        closeOnSelect: true,
        closeOnClear: true,
        format: 'yyyy-mm-dd'
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space