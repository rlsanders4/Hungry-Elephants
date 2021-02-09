/* 
 * File: nav.js
 * Created by Luke Evers
 * Sets the active navbar link to the current page.
 * For this to work, the HTML template used to render the page MUST pass a pageurl variable with the URL path of the current page.
 */

 $(document).ready(function() {
    $("a").removeClass("active");
    console.log("On page: " + pageurl);
    if(pageurl == "/admin/"){
        $("#adminlink").addClass("active");
    }
 });
