function outputUpdate(t) {
    var millis = t*1000 + 1000*60*60*5
    var truemillis = t*1000
    var options = { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }
    var gameTimeFormat = new Intl.DateTimeFormat("en-US", options).format;
    document.querySelector('#time').value = gameTimeFormat(millis);
    $( "li" ).each( function( index, el ) {
        var birth = $(this).data("birth");
        var death = $(this).data("death");
        if (birth > truemillis || death < truemillis) {
            $(this).hide();
        };
        if ((birth < truemillis && death==='None')||(birth < truemillis && death > truemillis)) {
            $(this).show();
        };
    });
}

$(document).ready(function(){
    var truemillis = $("#game_time").val()*1000;
    $( "li" ).each( function( index, el ) {
        var birth = $(this).data("birth");
        var death = $(this).data("death");
        if (birth > truemillis || death < truemillis) {
            $(this).hide();
        };
        if ((birth < truemillis && death==='None')||(birth < truemillis && death > truemillis)) {
            $(this).show();
        };
    });
});