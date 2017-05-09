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
    var url = "/get_vk_json";

    function successHandler (data) {
        drawTable(data);
    }

    function errorHandler (xhr) {
        alert(xhr.responseText);
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


function drawTable(data) {
    var hd = $("<h4>News:</h><br>");
    $("#news").empty();
    $("#news").append(hd);

    news = data.data;

    for (var source_idx = 0; source_idx < news.length; source_idx++) {
        title = news[source_idx].source;
        posts = news[source_idx].news;

        for (var post_idx = 0; post_idx < posts.length; post_idx++) {
                post = posts[post_idx];
                drawRow(title, post);
        }
    }
}

function drawRow(title, post) {
    if (post.rate == 1) {
        row=($("<p> <b>" + title + "</b> &emsp; <span class=\"label label-primary\">Good post</span></p>"));
    } else {
        row=($("<p> <b>" + title + "</b> &emsp; <span class=\"label label-danger\">Bad post</span></p>"));
    }
    row.append($("<br>"));

    row.append($("<p>" + post.text + "</p>"));
    row.append($("<hr>"))
    $("#news").append(row);
}
