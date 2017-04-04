document.addEventListener('DOMContentLoaded', function() {
    console.log("McBuckets");

    var tabHeader = document.getElementsByClassName("tab-header")[0],
        listItem = document.getElementsByClassName("2012")[0];
    
    listItem.addEventListener('click', function() {
      alert("It Works!");  
    }, false);
    
});
