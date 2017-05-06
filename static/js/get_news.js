/**
 * Created by alexander on 04.05.17.
 */
// ignore this first line (its fidle mock) and it will return what ever you pass as json:... parameter... consider to change it to your ajax call
$(function(){
    var url = "/get_vk_json";

    function successHandler (data) {
        drawTable(data)
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
    var hd = $("<thead>")
    hd.append($("<tr>"));
    hd.append($("<th>" + "Паблик" + "</th>"));
    hd.append($("<th> " + "Публикация" + "</th>"));
    hd.append($("</tr>"));
    hd.append($("</thead>"));
    $("#personDataTable").append(hd);

    var row = $("<tbody>")
    $("#personDataTable").append(row);
    for (var source_idx = 0; source_idx < data.length; source_idx++) {
    		title = data[source_idx].source;
        posts = data[source_idx].news;
        for (var post_idx = 0; post_idx < posts.length; post_idx++) {
        		post = posts[post_idx]
        		drawRow(title, post);
        }
    }
    row = $("</tbody>")
    $("#personDataTable").append(row);
}

function drawRow(title, post) {
	var row = $("<tr />")
    if (post.rate == 1) {
    	row = $("<tr class=\"good\">")
    } else {
    	row = $("<tr class=\"bad\">")
    }
    $("#personDataTable").append(row); //this will append tr element to table... keep its reference for a while since we will add cels into it

    row.append($("<td>" + title + "</td>"));
    row.append($("<td>" + post.text + "</td>"));
    row.append($("</tr>"))
}