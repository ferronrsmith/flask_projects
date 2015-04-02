//retrieve short url from shortener service

// dev mode - { false diables browser logging }
// dev mode prints allow console output to the browseer console using console.log
var debugMode = true;

/**
 * The following function calls the url shortener service to shorten the supplied url
 * @param longurl - url to be shortened  - i.e - longurl
 */
function get_shorturl(longurl){
    $.getJSON('/create/'+longurl, function(obj) {

        // http status code
        var status = obj.status_code;
        var href, url;
        
        // testing
        console.log(obj);

        //check the status codes of request
        if(status == 200) {
            url = obj.data.url;
            href = url;
	          $('#urlid').val('');

            // avoid appending to table if it already exists
            if(obj.data.exists == false) {
    	        append_to_table(obj);
            }
            else {
              alert('Already in your item list');
            }
        }
        else if (status == 404) {
            url = 'PAGE NOT FOUND';
            href = '#';
        }

        $('#result').text(url);
        $('#result').attr('href',href);
    });
}

/**
 * The following function gets the current href and appends the shorturl
 * @param shorturl - hash - i.e shorturl
 * @return {String := current href with hash appended }
 */
function format_shorturl(shorturl) {
    return document.location.href + shorturl;
}

/**
 * The following function formats a long url {appened protocol/limit length}
 * @param longurl - site url
 * @param protocol - http/https
 * @param limit - boolean to determine if url should be limited if too long
 * @return {*}
 */
function format_longurl(longurl, protocol, limit) {
    var result = longurl;
    if(result.indexOf('http://') < 0) {
        result = protocol + longurl;
    }
    if(limit) {
        result = txtlimiter(result)
    }
    return result;
}

$(function(){
    //format the shorturl so that it is clickable
    var shorturl = $('#shorturl').text();
    $('#shorturl').attr('href',format_shorturl(shorturl));
    
    // check debugging value
    if(!debugMode) {
        console.log = function(){return {}};
    }
});

// calls shortner service and retrieve url
function submit_request(){
    var input = $.trim($('#urlid').val());
    if (input.length === 0)
        alert('No input was entered!!!');
    else {
        // check if url is valid
        if(validurl(input)){
           get_shorturl(input);
        }
        else {
         alert('Invalid URL!!!!');
        }
    }
}

/**
 * The following function limits the length of a string to predefined limit value.
 * If the entered value exceeds this value it will be shortened and (...) appended
 * @param url - url to be limited
 * @return {String := limited url}
 */
function txtlimiter(url){
  var limit = 50;
  if (url.length > limit){
    return url.substring(0,limit-3) + '...';
  }
  else{
    return url;
  }
}

/**
 * The following function checks if a url is valid
 * @param url - url to be validated
 * @return {Boolean := returns true if url is valid}
 */
function validurl (url){
    var expression = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
    return expression.test(url);
}

/**
 * The following function appends a row dynamically to the shorten url table
 * @param obj - json object returned from url shortener service
 */
function append_to_table(obj){
  $('#tid tr:first').after(
      "<tr><td><a id=longurl href=" + format_longurl(obj.data.long_url,obj.proto,false) + '">' +
          format_longurl(obj.data.long_url,obj.proto,true) + "</a></td><td>" +
          '<a id=shorturl href="' + obj.data.url +'">' + obj.data.hash+'</a>' +
          '</td>' +
      '</tr>');
}