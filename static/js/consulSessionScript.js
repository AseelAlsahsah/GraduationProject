//function checkSessionTimes() {
//    // Get the current time
//    var currentTime = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
//    var end_time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
//
//    // Loop through all the buttons and update their styles
//    var buttons = document.querySelectorAll(".session-button");
//    buttons.forEach(function(button) {
//        var sessionTime = button.getAttribute("data-session-time");
//        if (currentTime >= end_time and current_time <= end_time) {
//            button.classList.add("accept");
//            button.classList.remove("disabled");
//            button.disabled = false;
//        } else {
//            button.classList.add("disabled");
//            button.classList.remove("accept");
//            button.disabled = true;
//        }
//    });
//}
//
//window.onload = function() {
//    // Call the checkSessionTimes function when the page is loaded
//    checkSessionTimes();
//};
//
//window.addEventListener("focus", function() {
//    // Call the checkSessionTimes function when the page gains focus
//    checkSessionTimes();
//});