var veryFast=50

$(document).ready(function() {
    var original = {"width":"82px", "height":"82px", "margin":"15px"};
    var originalImg = {"width":"90px", "height":"90px", "margin":"-7px"};
    
    var large = {"width":"92px", "height":"92px", "margin":"10px"};
    var largeImg = {"height":"100px", "width":"100px", "margin":"-7px"};

    var myName = $('#my_name').text();
    
    $('.player').each(function() {
        player = $(this);
        player_name = player.find('.player_name');
        var name = $.trim(player_name.text());
        console.log(name);
        if(name===myName){
            player.addClass('bold');
        };
    });
    
    $('.match_time')
    
    $('.champ_pic').hover(function() {
        $(this).animate(large, veryFast);
        $(this).children('img').animate(largeImg, veryFast);
    }, function() {
        $(this).animate(original, veryFast);
        $(this).children('img').animate(originalImg, veryFast);
    });
    
    // $('.collapse').hide();
    // $('.match_details').hide();
    
    
    $('.match').mouseenter(function() {
        var match = $(this);
        var expand = match.find('.expand');
        var collapse = match.find('.collapse');
        var matchDetails = match.find('.match_details');
        
        expand.click(function(){
            matchDetails.show();
            expand.hide();
            collapse.show();
            match.animate({"width":"700px"}, veryFast);
        });

        collapse.click(function(){
            matchDetails.hide();
            expand.show();
            collapse.hide();
            match.animate({"width":"330px"}, veryFast);
        });
    });
    

    
    // $('.match').hover(function() {
        // var match = $(this);
        // expandMatch(match);
    // }, function() {
        // var match = $(this);
        // normalizeMatch(match);
    // });
});

function expandMatch(match) {
    var blue = match.find('.blue_team');
    var vs = match.find('.vs');
    var red = match.find('.red_team');
    var players = match.find('.player');
    var playerPics = match.find('.player_pic');
    var playerPicImgs = playerPics.find('img');
    var playerNames = match.find('.player_name');
    
    match.animate({"height":"240px"}, veryFast);
    vs.animate({"height":"240px", "line-height":"240px"}, veryFast);
    blue.animate({"height":"240px"}, veryFast);
    players.animate({"height":"30px"}, veryFast);
    playerPics.animate({"height":"30px"}, veryFast);
    playerPicImgs.animate({"height":"30px", "width":"30px", "margin":"0 5px"}, veryFast);
    playerNames.animate({"font-size":"14px", "line-height":"30px"}, veryFast);
};

function normalizeMatch(match) {
    var blue = match.find('.blue_team');
    var vs = match.find('.vs');
    var red = match.find('.red_team');
    var players = match.find('.player');
    var playerPics = match.find('.player_pic');
    var playerPicImgs = playerPics.find('img');
    var playerNames = match.find('.player_name');
    
    match.animate({"height":"120px"}, veryFast);
    vs.animate({"height":"120px", "line-height":"120px"}, veryFast);
    blue.animate({"height":"120px"}, veryFast);
    players.animate({"height":"20px"}, veryFast);
    playerPics.animate({"height":"20px"}, veryFast);
    playerPicImgs.animate({"height":"20px", "width":"20px", "margin":"0 10px"}, veryFast);
    playerNames.animate({"font-size":"12px", "line-height":"20px"}, veryFast);
};