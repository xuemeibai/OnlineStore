function get_global_new() {
    var isoString = latest_refresh.toISOString();

    $.ajax({
        url: "/refresh-global",
        
        data: {
            'last_refresh' : isoString
        },
        type: "GET",

        dataType : "json",
        
        success: function(info){
            update_posts(info);
            update_comments(info);
            latest_refresh = new Date();//renew our last refresh time
        }

    });
}

function addPost(ItemId){
    var isoString = latest_refresh.toISOString();
    var new_post_text_element = $("#id_post_input_text");
    var new_post_text_value = new_post_text_element.val();
    console.log("new_post_text_value = " + new_post_text_value);
    // Clear input box and old error message (if any)
    new_post_text_element.val('');
    displayPostError('');

    $.ajax({
        url: "/add-post/" + ItemId,
        type: "POST",
        data: {
            'last_refresh' : isoString,
            'new_post_text': new_post_text_value,
            csrfmiddlewaretoken: getCSRFToken(),
        },
        
        dataType : "json",
        success: function(response) {
            if ('error' in response){
                displayPostError(response.error);
            } else {
                update_posts(response);
                update_comments(response);
            }

            latest_refresh = new Date();
            
        }
    });
}


function addComment(PostId){
    var isoString = latest_refresh.toISOString();
    var new_comment_text_element = $("#id_comment_input_text_" + PostId);
    var new_comment_text_value = new_comment_text_element.val();

    // Clear input box and old error message (if any)
    new_comment_text_element.val('');
    displayCommentError('');

    $.ajax({
        url: "/add-comment/" + PostId,
        type: "POST",
        data: {
            'last_refresh': isoString,
            'new_comment_text': new_comment_text_value,
            csrfmiddlewaretoken: getCSRFToken(),
        },

        dataType: "json",
        success: function(response) {
            if ('error' in response){
                displayCommentError(response.error, PostId);
            } else {
                update_posts(response);
                update_comments(response);
            }

            latest_refresh = new Date();
        }
    });

}

function update_posts(info) {
    var new_posts = JSON.parse(info['new_posts']);
    console.log('info = ', info, "new posts = ", new_posts);
    $(new_posts).each(function() {
        my_id = "id_post_text_" + this.pk;
        if (document.getElementById(my_id) == null) {
            var isodate = new Date(this.fields.creation_time);
            var options = { year: 'numeric', month: 'long', day: 'numeric'};
            var format_time = isodate.toLocaleString("en-US", options);
            var format_hm = formatAMPM(isodate);
            // console.log(this);
            $("#global_posts").prepend(
                // First part: post itself
                '<li> <div id = "post_"' + this.pk + 'class="posts">' +
                'Post by <a href="/user_profile/' + this.fields.created_by +
                '" id="id_post_profile_' + this.pk + '">' + 
                sanitize(this.fields.first_name) + ' ' + sanitize(this.fields.last_name) +
                '</a>' + '<span id="id_post_text_' + this.pk + '"> -- ' + sanitize(this.fields.post_input_text) + ' -- </span>' +
                '<span id="id_post_date_time_' + this.pk + '">' + sanitize(format_time) + ', ' + sanitize(format_hm) + '</span> </div>' 
                // Second part: comments for post, just write the skeleton
                + '<div id="comment_in_post_' + this.pk + '" class="comments">' + '</div>'
                // Third part: each post has a place to submit comment. This is the comment submit area
                + '<div id="comment_area_in_post_' + this.pk + '" class="comment_area">'
                + '<table> <tr> <td>Comment:</td> ' + 
                '<td><input type="text" maxlength="140" required id="id_comment_input_text_' + this.pk + '"></td>'
                + '<td> <button type="submit" id="id_comment_button_' + this.pk 
                + '" onclick="addComment(\'' + this.pk + '\')">Submit</button> </td>'
                + '<td class="errorlist" id="new_comment_error_' + this.pk + '"></td> </tr> </table> </div> </li>'
            )
        }
    });
}

function update_comments(info){
    var new_comments = JSON.parse(info['new_comments']);

    $(new_comments).each(function(){
        my_id = "id_comment_text_" + this.pk;
        if (document.getElementById(my_id) == null)
        {
            var isodate = new Date(this.fields.creation_time);
            var options = { year: 'numeric', month: 'long', day: 'numeric'};
            var format_time = isodate.toLocaleString("en-US", options);
            var format_hm = formatAMPM(isodate);
            $("#comment_in_post_" + this.fields.belong_post).append(
            '<div> Comment by <a href="/user_profile/' + this.fields.created_by + '"'
            + ' id="id_comment_profile_' + this.pk + '">' + sanitize(this.fields.first_name) + ' '
            + sanitize(this.fields.last_name) + '</a>'
            + '<span id="id_comment_text_' + this.pk + '"> -- ' + sanitize(this.fields.content) + ' -- </span>'
            + '<span id="id_comment_date_time_' + this.pk + '"> ' + sanitize(format_time) + ', ' + sanitize(format_hm) + '</span>'
            + '</div>'
        )}
    });
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

function displayPostError(message) {
    $("#new_post_error").html(message);
}

function displayCommentError(message, PostId) {
    $("#new_comment_error_" + PostId).html(message);
}


function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        c = cookies[i].trim();
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length);
        }
    }
    return "unknown";
}

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = ('0'+minutes).slice(-2);
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
  }  

var latest_refresh = new Date();

window.onload = function(){
    latest_refresh = new Date();
}

window.setInterval(get_global_new, 5000);