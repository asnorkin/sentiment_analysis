/**
 * Created by alexander on 04.05.17.
 */
// ignore this first line (its fidle mock) and it will return what ever you pass as json:... parameter... consider to change it to your ajax call
$(function(){
    var url = "/get_vk_json";

    function successHandler (data) {
        drawTable(data);
    }

    function errorHandler (xhr, status) {
        alert("Что-то пошло не так");
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
    var hd = $("<h4>News:</h><br>")
    $("#news").empty();
    $("#news").append(hd);

    news = data.data

    for (var source_idx = 0; source_idx < news.length; source_idx++) {
        title = news[source_idx].source;
        posts = news[source_idx].news;

        for (var post_idx = 0; post_idx < posts.length; post_idx++) {
                post = posts[post_idx]
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
