(function($){
  $(function(){

    $('.parallax').parallax();

    $('select').material_select();

    $('.button-collapse').sideNav();

    $('.collapsible').collapsible({
      accordion : false 
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space