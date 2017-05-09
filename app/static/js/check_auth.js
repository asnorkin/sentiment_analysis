// setup csrf token for all ajax calls
// var csrftoken = $('meta[name=csrf-token]').attr('content');
// $.ajaxSetup({
//     beforeSend: function(xhr, settings) {
//         if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
//          xhr.setRequestHeader("X-CSRFToken", csrftoken);
//       }
//     }
// });

$(document).ready(function(){
   // initial check to see if user is logged in or not
   updateAuthStatus();
});

// helpers
function updateAuthStatus() {
   verifyAuth()
      .done(function(response){
         showLoggedIn(response.data.user_name)
      }).fail(function(response){
         showLoggedout()
      });
}

function showLoggedIn(username) {
   // May do something
}

function showLoggedout() {
   // show logged out view
   document.body.innerHTML = '';
   var url = '/';
   alert("\t You are not autorized yet! Log In please! \t");
   window.location.href = url;
}

// API calls
function verifyAuth(callback) {
   var url = '/api/auth/verify_auth';
   return $.get(url);
}
