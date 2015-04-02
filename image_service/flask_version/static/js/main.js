// dev mode - { false diables browser logging }
// dev mode prints allow console output to the browseer console using console.log
var debugMode = true;
var maxFileSize = 1.0;
var megabytes = 1024 * 1024;

$(function(){
   if(!debugMode) {
       // turn off console logging if not in debug mode
       console.log= {};
   }
});

/**
 *
 * @param files
 */
function upload(files) {

    for (var i = 0; i < files.length; i++) {
        var file = files[i];

        var currentSize = file.size / megabytes;

        if(currentSize>maxFileSize) {
            alert("File size cannot be greater than 1 MB!!! File size : " + currentSize.toFixed(2) + " MB");
            return;
        }
    }

    $("#imageupload").submit();
}

function editMode() {
    $('#filename').removeAttr("disabled");
    $('#edit').hide();
    $('#save').show();
}

function updateTitle() {

    var title = $('#filename').val();
    var shorturl = $('#shorturl').val();

    $.post('/update', { title: title, shorturl: shorturl }, function(data) {
        if(data.success) {
            console.log('title was successfully updated ');
        }
        else {
            console.log('error : title not updated');
        }
    });

    // final state
    // set back to default value
    $('#filename').attr("disabled", "disabled");
    $('#edit').show();
    $('#save').hide();

}

function deleteImg() {
    var shorturl = $('#shorturl').val();
    $.get("/delete/" + shorturl, function(data){

        if(data.success) {
            document.location = document.location.origin;
        }
        else {
            console.log('error : image could not be deleted');
        }
    });
}