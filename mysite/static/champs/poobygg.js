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
 
var updateMyGold = function(trueMillis) {
    var myGold = 0;
    var myConsumableGold = 0;
    $(".my_build").find(".time_item_slot").each( function() {
        var slot = $(this);
        var gold = slot.data("gold");
        var itemName = slot.data("name");
        var birth = slot.data("birth");
        
        if (itemName in myStackCounter) {
            if (birth < trueMillis) {
                myConsumableGold += gold;
            };
        }
        else {
            if (slot.is(":visible")) {
                myGold += gold; 
            };
        };
    });;
    buildGold = $(".my_build").find(".build_gold").find(".gold_val");
    if (myGold > 1000) {
        myGold = (myGold/1000).toFixed(2).toString() + "K";
    };
    buildGold.text(myGold);
    
    consumableGold = $(".my_build").find(".consumable_gold").find(".gold_val");
    if (myConsumableGold > 1000) {
        myConsumableGold = (myConsumableGold/1000).toFixed(2).toString() + "K";
    };
    consumableGold.text(myConsumableGold);
}

var updateOtherGold = function(trueMillis) {
    var otherGold = 0;
    var otherConsumableGold = 0;
    $(".other_build").find(".time_item_slot").each( function() {
        var slot = $(this);
        var gold = slot.data("gold");
        var itemName = slot.data("name");
        var birth = slot.data("birth");
        
        if (itemName in otherStackCounter) {
            if (birth < trueMillis) {
                otherConsumableGold += gold;
            };
        }
        else {
            if (slot.is(":visible")) {
                otherGold += gold; 
            };
        };
    });;
    
    buildGold = $(".other_build").find(".build_gold").find(".gold_val");
    if (otherGold > 1000) {
        otherGold = (otherGold/1000).toFixed(2).toString() + "K";
    };
    buildGold.text(otherGold);
    
    consumableGold = $(".other_build").find(".consumable_gold").find(".gold_val");
    if (otherConsumableGold > 1000) {
        otherConsumableGold = (otherConsumableGold/1000).toFixed(2).toString() + "K";
    };
    consumableGold.text(otherConsumableGold);    
}
 
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
        var gold = slot.data("gold");
        

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
    
    updateMyGold(trueMillis);
    updateOtherGold(trueMillis);
    
    el = $("#game_time");
    el.val(t);
    
    width = el.width();
    newPoint = (el.val() - el.attr("min")) / (el.attr("max") - el.attr("min"))
    
    offset = 4.7;
    
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
    var t, max;
    var interval = null;
    
    myShowOrHide(trueMillis);
    otherShowOrHide(trueMillis);
    
    outputUpdate(30);
    showPlay();
    
    $("#pause").click(function() {
        showPlay();
        stopGameTime();
    });

    $("#play").click(function() {
        showPause();
        playGameTime();
    });    
    
    function playGameTime() {
        console.log("playing!");
        t = parseInt(slider.val());
        max = parseInt(slider.attr("max"));
        
        interval = setInterval(increment, 100);
        
        function increment() {
            if ((t+10)<max){ t+=10;};
            outputUpdate(t);
        };
    };
    
    function stopGameTime() {
        console.log("pausing!");
        clearInterval(interval);
    };
});