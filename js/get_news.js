/**
 * Created by alexander on 04.05.17.
 */
// ignore this first line (its fidle mock) and it will return what ever you pass as json:... parameter... consider to change it to your ajax call
$(function(){
    var url = "/get_vk_json";

    function successHandler (response) {
        var form = response.form;  // эквивалент response["form"]
        alert("Отлично");
    }

    function errorHandler (xhr, status) {
        alert("Что-то пошло не так");
    }

    function formHandler(event) {
        event.preventDefault();
        $.ajax({
            url: url,
            type: "POST",
            crossDomain: false,
            data: $(this).serialize(),
            dataType: "json",
            success: successHandler,
            error: errorHandler
        })
    }

    $("#nkvd_form").submit(formHandler);
})

// $.ajax({
//     url: '/get_vk_json/',
//     type: "POST",
//     data: ,
//     success: function(data, textStatus, jqXHR) {
//         // since we are using jQuery, you don't need to parse response
//         drawTable(data);
//     }
// });

function drawTable(data) {
    for (var source_idx = 0; source_idx < data.length; source_idx++) {
    		title = data[source_idx].source;
        posts = data[source_idx].news;
        for (var post_idx = 0; post_idx < posts.length; post_idx++) {
        		post = posts[post_idx]
        		drawRow(title, post);
        }
    }
}

function drawRow(title, post) {
		var row = $("<tr />")
    if (post.rate == 1) {
    	row = $("<tr bgcolor=\"#FA8075\">")
    } else {
    	row = $("<tr bgcolor=\"#0F00FF\">")
    }
    $("#personDataTable").append(row); //this will append tr element to table... keep its reference for a while since we will add cels into it

    row.append($("<td>" + title + "</td>"));
    row.append($("<td>" + post.text + "</td>"));
    row.append($("</tr>"))
}