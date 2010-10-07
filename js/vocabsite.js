$(function() {
   
 });


/**
 * getParameterbyName
 * @param name
 */

function getParameterByName( name )
{
  name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
  var regexS = "[\\?&]"+name+"=([^&#]*)";
  var regex = new RegExp( regexS );
  var results = regex.exec( window.location.href );
  if( results == null )
    return "";
  else
    return decodeURIComponent(results[1].replace(/\+/g, " "));
}


/**
 * populategemt
 * @param id
 */

function populategemet(id) {
   boxelem = $("#box"+id);
   barspin = $("#barspin"+id);
   barspin.attr("src", "/images/spinner4.gif");
   boxelem.load("/services/vservs/gemet?q="+getParameterByName('q'));
   $.ajax({
      url: "/services/vservs/gemet?q="+getParameterByName('q'),
      global: false,
      type: "GET",
      async:false,
      success: function(msg){
         boxelem.html(msg);
         toggle(id);
         barspin.attr("src", "");
      }
   });

   //toggle(id);
   //barspin.attr("src", "");
   
}
 /**
  * toggle
  * @param id
  */
 function toggle(id) {
    boxelem = $("#box"+id);
    linkelem = $("#link"+id)
    linkelem.text('-')
    linkelem.attr("href","javascript:untoggle('"+id+"')");
    boxelem.show('fast');
 }
 /**
  * untoggle
  * @param id
  */
 function untoggle(id) {
    boxelem = $("#box"+id);
    linkelem = $("#link"+id)
    linkelem.text('+')
    linkelem.attr("href","javascript:toggle('"+id+"')");
    boxelem.hide('slow');
 }
