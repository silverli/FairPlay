$( document ).ready(function() {
    console.log('working');
    
    //adds functionality from jquery ui for tabs on school view page
    $( function() {
        $( "#tabs" ).tabs();
    });
    
    //adds functionality for accordions on take action page
    $(".accordion-header h2").on('click', function() {
        console.log('did it');
        $(this).siblings('p').toggleClass('accordion-showing');
    });     
    
});
