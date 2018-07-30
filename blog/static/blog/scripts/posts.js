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
    document.querySelector("#spin").classList.add("spinner");

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
            document.querySelector("#spin").classList.remove("spinner");
            fetchLatestComment();
        },
        error: function(){
            document.querySelector("#spin").classList.remove("spinner");
            commentError("Could not comment. Refresh the page and try again")
        }
    })
});


// new comment is fetched!
function fetchLatestComment(){
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
            newComment(currentUserName, json.results[0]['comment_text'], json.results[0]['time']);
        },
        error: function (json) {
            commentError("Could not load new comments, please refresh the page")
        }
    })
}


var count = 0;

function newComment (user, text, time) {
    // section to add new section
    var newCommentSection = document.getElementById("new-comments");

    // new comment section
    var commentDiv = document.createElement("div");
    commentDiv.className = "row comment";        // add a class name
    commentDiv.id = count;            // add an id
    commentDiv.style.display = "none"; // for animation
    
    // image section
    var imageDiv = document.createElement("div");
    imageDiv.className = "col-sm-1";       // size
    imageDiv.id = "user-img";
    var imgSection = document.createElement("img");
    imgSection.src = userImageAddress; // add a source
    imgSection.alt = "image of " + user;  // adds an alternative to the image
    imageDiv.appendChild(imgSection);
    commentDiv.appendChild(imageDiv);

    // top section
    var commentZone = document.createElement("p");
    commentZone.className = "col-sm-11"; // size
    var userPlace = document.createElement("strong");   // bold divs
    var timePlace = document.createElement("strong");   // bold divs
    var topText = document.createTextNode(" Posted ");  // static section
    var userName = document.createTextNode(user);       // username
    userPlace.appendChild(userName);
    var timeValue = document.createTextNode(time);      // time
    timePlace.appendChild(timeValue);
    var lineBreak = document.createElement("br");       // linebreak
    var commentText = document.createTextNode(text);     // the content
    commentZone.appendChild(userPlace);
    commentZone.appendChild(topText);
    commentZone.appendChild(timePlace);
    commentZone.appendChild(lineBreak);
    commentZone.appendChild(commentText);
    commentDiv.appendChild(commentZone);

    // add sec to page
    if (count == 0) {
        // the very first one
        newCommentSection.appendChild(commentDiv);
    } else {
        // other comments that follow
        var b4 = document.getElementById(count-1);
        newCommentSection.insertBefore(commentDiv, b4);
    }
    
    $("#"+count).show(200);

    // Increment count
    count++;
    
    // If no comments existed
    try {
        document.getElementById("no-comments").style.display = "none";
    }
    catch (err) {
        console.log("You are not the first to comment");
    }
}


// error message when ajax comment fails
function commentError (message) {
    var errorDiv = document.getElementById("comment-error");
    errorDiv.innerHTML = message;
    $(errorDiv).show(100);
}
