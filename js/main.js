//Fix for security error with jquery mobile: http://stackoverflow.com/questions/32453806/uncaught-securityerror-failed-to-execute-replacestate-on-history-cannot-be
$(document).bind('mobileinit',function(){
  $.mobile.changePage.defaults.changeHash = false;
  $.mobile.hashListeningEnabled = false;
  $.mobile.pushStateEnabled = false;
});


function displayCalendarWhenInputFieldClicked(){
  $('div#calpicker input').on('click', function(){$('div#calpicker a').click()});
}

$(document).on('pageinit', function() {
  displayCalendarWhenInputFieldClicked();
});


