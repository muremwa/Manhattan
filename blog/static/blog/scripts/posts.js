var inputs = document.getElementsByTagName("input");

for (input in inputs) {
    if (inputs[input].type == "text") {
        inputs[input].classList.add("form-control");
        inputs[input].style.width = "100%";
        inputs[input].placeholder = "Say something about this post";
    }
}

$(document).on('submit', '#comment-form', function(e){
    e.preventDefault();
    console.log(pk);

    $.ajax({
        type: 'POST',
        url: commentUrl,
        // dataType: 'json',
        data: {
            comment:$("#id_comment_text").val(),
            id: pk,
            csrfmiddlewaretoken:$("input[name=csrfmiddlewaretoken]").val()
        },
        success: function(){
            fetchComments();
        },
        error: function(){
            commentError("Could not comment. Refresh the page and try again")
        }
    })
});


// new comment is fetched!
function fetchComments(){
    // give post id, 
    $.ajax({
        type:"GET",
        url: allCommentsUrl,
        dataType:'json',
        data:{
            id: pk,
            csrfmiddlewaretoken:token
        },
        success: function (json) {
            newCommentRegion(json.results[0]['comment_text']);
        },
        error: function (json) {
            commentError("Could not load new comments, please refresh the page")
        }
    })
}

// new comment appears on the page!
function newCommentRegion (commText, date) {
    var commentText = document.getElementById("new-comment-text");
    var datePosted = document.getElementById("new-comment-posted");

    commentText.innerHTML = commText;
    datePosted.innerHTML = "Just now";
    $("#new-comment").show(200);
    document.getElementById("id_comment_text").placeholder = "Say something about this post";
    // If no comments existed
    try {
        document.getElementById("no-comments").style.display = "none";
    }
    catch (err) {
        console.log("other comments exist!");
    }
}

function commentError (message) {
    var errorDiv = document.getElementById("comment-error");
    errorDiv.innerHTML = message;
    $(errorDiv).show(100);
}
