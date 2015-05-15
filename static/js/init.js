(function($){
  $(function(){

    $('.parallax').parallax();

    $('.datepicker').pickadate({
        format: 'mmmm d, yyyy',  // what the user sees
        formatSubmit: 'yyyy/mm/dd',  // what the server sees
        hiddenName: true,  // only submit the formatSubmit value
        closeOnSelect: true,  // this doesn't work right now...
        close: 'Close',  // label on 'close' button
        min: -3,  // date range min (relative to today)
        max: 3  // date range max (relative to today)
    });

    $('select').material_select();

    $('.button-collapse').sideNav();

    $('.collapsible').collapsible({
      accordion : false 
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space