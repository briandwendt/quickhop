(function($){
  $(function(){

    // Parallax image behind the search form and page headers
    $('.parallax').parallax();

    // Search form date picker
    //  (min/max date restrictions from FlightStats API)
    $('.datepicker').pickadate({
        format: 'mmmm d, yyyy',  // what the user sees
        formatSubmit: 'yyyy/mm/dd',  // what the server sees
        hiddenName: true,  // only submit the formatSubmit value
        closeOnSelect: true,  // this doesn't work right now...
        today: '', // let's hide this button
        clear: '', // and this one too -- why clear the form?
        close: 'Close',  // label on 'close' button
        min: -7,  // date range min (relative to today)
        max: 3  // date range max (relative to today)
    });

    // Custom styled select fields
    $('select').material_select();

    // Collapsible side nav on mobiles
    $('.button-collapse').sideNav();

    // Flights list display collapsible
    $('.collapsible').collapsible({
      accordion : false 
    });

  }); // end of document ready
})(jQuery); // end of jQuery name space