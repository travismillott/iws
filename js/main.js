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
  $("td.turnEpochIntoDate").each(function(i,ele){ele.innerHTML = setDateFromEpoch(parseInt(ele.innerHTML))})
  $('#datatable').DataTable( {
    order: []
  } );
});

var monthNames = [
  "Jan", "Feb", "Mar",
  "Apr", "May", "Jun", "Jul",
  "Aug", "Sep", "Oct",
  "Nov", "Dec"
];

function padZero(i) {
    if (i < 10) {
        i = "0" + i;
    }
    return i;
}

function setDateFromEpoch(epoch){
  var d = new Date(0); 
  d.setUTCSeconds(epoch);
  return monthNames[d.getMonth()] +' ' + d.getDate() + ' ' + d.getFullYear() + ' ' + padZero(d.getHours()) + ':' + padZero(d.getMinutes());
}

