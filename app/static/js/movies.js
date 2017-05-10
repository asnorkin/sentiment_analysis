// setup csrf token for all ajax calls
var csrftoken = $('meta[name=csrf-token]').attr('content');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
         xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
    }
});

$(function(){
    var url = "/api/analysis/movies_analyzer";

    function successHandler (data) {
        $("#response_text").val(data.text);
        $("#prediction").text(data.pred_msg);
    }

    function errorHandler (xhr) {
        alert('Error occured: ' + xhr.responseText);
    }

    function formHandler(event) {
        event.preventDefault();
        $.ajax({
            url: url,
            type: "POST",
            data: $(this).serialize(),
            dataType: "json",
            success: successHandler,
            error: errorHandler
        });
    }

    $("#request_form").submit(formHandler);
})
