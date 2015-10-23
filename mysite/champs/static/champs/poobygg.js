var myStackCounter = {"Health Potion":0, 
                    "Mana Potion":0, 
                    "Elixir of Iron":0,
                    "Elixir of Ruin":0,
                    "Elixir of Sorcery":0,
                    "Elixir of Wrath":0,
                    "Stealth Ward":0, 
                    "Total Biscuit of Rejuvenation":0, 
                    "Vision Ward":0};
                    
var otherStackCounter = {"Health Potion":0, 
                    "Mana Potion":0, 
                    "Elixir of Iron":0,
                    "Elixir of Ruin":0,
                    "Elixir of Sorcery":0,
                    "Elixir of Wrath":0,
                    "Stealth Ward":0, 
                    "Total Biscuit of Rejuvenation":0, 
                    "Vision Ward":0};

var showPlay = function() {
    $("#pause").hide();
    $("#play").show();
};

var showPause = function() {
    $("#play").hide();
    $("#pause").show();
};
 
var updateMyStacks = function() {
    $(".my_build").find(".time_item_slot").each( function() {
        var slot = $(this);
        var itemName = slot.data("name");
        if (itemName in myStackCounter) {
            slot.children(".stack_num").text(myStackCounter[itemName]);
        };
    });
};
  
var updateOtherStacks = function() {  
    $(".other_build").find(".time_item_slot").each( function() {
        var slot = $(this);
        var itemName = slot.data("name");
        if (itemName in otherStackCounter) {
            slot.children(".stack_num").text(otherStackCounter[itemName]);
        };
    });
};
              
var myShowOrHide = function(trueMillis) {
    $(".my_build").find(".time_item_slot").each( function() {
        var slot = $(this);        
        var birth = slot.data("birth");
        var death = slot.data("death");
        var itemName = slot.data("name");
        var stackState = slot.data("stack");

        // If item was born after current time or died before current time,
        // we want to hide it.
        var hideItem = Boolean(birth > trueMillis || death < trueMillis);
       
        if (hideItem) {
            if (itemName in myStackCounter && stackState === "on"){
                myStackCounter[itemName]--;
                slot.data("stack", "off");
                updateMyStacks();
            };
            
            slot.hide();
        }
        
        else {
            if (itemName in myStackCounter){
                if (stackState === "off"){
                    myStackCounter[itemName]++;
                    slot.data("stack", "on");
                    updateMyStacks();
                };
            
                if (myStackCounter[itemName] <= 1){ 
                    slot.show();
                };
            }
                
            else{
                slot.show();
            };
        };
    });
};

var otherShowOrHide = function(trueMillis) {
    $(".other_build").find(".time_item_slot").each( function() {
        var slot = $(this);        
        var birth = slot.data("birth");
        var death = slot.data("death");
        var itemName = slot.data("name");
        var stackState = slot.data("stack");

        // If item was born after current time or died before current time,
        // we want to hide it.
        var hideItem = Boolean(birth > trueMillis || death < trueMillis);
       
        if (hideItem) {
            if (itemName in otherStackCounter && stackState === "on"){
                otherStackCounter[itemName]--;
                slot.data("stack", "off");
                updateOtherStacks();
            };
            
            slot.hide();
        }
        
        else {
            if (itemName in otherStackCounter){
                if (stackState === "off"){
                    otherStackCounter[itemName]++;
                    slot.data("stack", "on");
                    updateOtherStacks();
                };
            
                if (otherStackCounter[itemName] <= 1){ 
                    slot.show();
                };
            }
                
            else{
                slot.show();
            };
        };
    });
};
                    
function outputUpdate(t) {
    var el, slot, millis, trueMillis, shownCount, options, gameTimeFormat, birth, death, itemName
    millis = t*1000 + 1000*60*60*5;
    trueMillis = t*1000;
    shownCount = 0;
    options = { hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false };
    gameTimeFormat = new Intl.DateTimeFormat("en-US", options).format;
    document.querySelector('#time').value = gameTimeFormat(millis);
    
    myShowOrHide(trueMillis);
    otherShowOrHide(trueMillis);
    
    el = $("#game_time");
    el.val(t);
    
    width = el.width();
    newPoint = (el.val() - el.attr("min")) / (el.attr("max") - el.attr("min"))
    
    offset = 3.1;
    
    if (newPoint < 0) { newPlace = 0; }
    else if (newPoint > 1) { newPlace = width; }
    else { 
        newPlace = width * newPoint + offset;
        offset -= newPoint;
    };
    
    el
        .next("output")
        .css({
            left: newPlace,
            marginLeft: offset + "%"
        })
}

$(document).ready(function(){
    var slider = $("#game_time");
    var trueMillis = slider.val()*1000;
    var t, max, interval;
    var play;
    
    myShowOrHide(trueMillis);
    otherShowOrHide(trueMillis);
    
    outputUpdate(30);
    showPlay();
    
    $("#pause").click(function() {
        showPlay();
        runGameTime(false);
    });

    $("#play").click(function() {
        showPause();
        runGameTime(true);
    });    
    
    function runGameTime(play) {
        if (play) {
            console.log("playing!");
            t = parseInt(slider.val());
            max = parseInt(slider.attr("max"));
            
            interval = setInterval(increment(), 100);
            
            function increment() {
                if ((t+10)<max){ t+=10;};
                outputUpdate(t);
            };
        }
        else {
            console.log("pausing!");
            clearInterval(interval);
        }
    };
});