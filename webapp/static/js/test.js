document.addEventListener('DOMContentLoaded', function() {
    console.log("McBuckets");

    var tabHeader = document.getElementsByClassName("tab-header")[0];
    
    tabHeader.addEventListener('click', function() {
      alert("It Works!");  
    }, false);
});
