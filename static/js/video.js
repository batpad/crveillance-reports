function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

$(function() {
  var videoElem = $('#video').get(0);
  var isFocussed = false;
  function getFrameData() {
    var canvas = document.createElement('canvas');
    canvas.height = videoElem.videoHeight;
    canvas.width = videoElem.videoWidth;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(videoElem, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL();
  }

  $('input, textarea').focus(function() {
    isFocussed = true;
  });

  $('input, textarea').blur(function() {
    isFocussed = false;
  });

  videoElem.onpause = function () {
    $('#pauseVideo').text('Play! (space)');
    $('.js-show-on-pause').show();
  }
  
  videoElem.onplay = function () {
    $('#pauseVideo').text('Pause! (space)');
    $('.js-show-on-pause').hide();
  }
  
  videoElem.onloadedmetadata = function() {
    if (window.location.hash !== '#') {
      var hash = window.location.hash.replace('#', '');
      var newTime = parseFloat(Number(hash) / 1000).toFixed(3);
      videoElem.currentTime = newTime;
    }
  }

  $('#pauseVideo').click(function() {
    if(!videoElem.paused) {
      videoElem.pause();
    } else {
      videoElem.play();
    }
  });
  
  $('#goBack').click(function() {
    var currentTimeMs= videoElem.currentTime * 1000;
    var prevFrame = currentTimeMs - 40;
    if (prevFrame < 0) { 
      prevFrame = 0;
    }
    videoElem.currentTime = prevFrame / 1000;
  });
  
  $('#goForward').click(function() {
    var currentTimeMs= videoElem.currentTime * 1000;
    var nextFrame = currentTimeMs + 40;
    if (nextFrame / 1000 > videoElem.duration) {
      nextFrame = videoElem.duration * 1000;
    }
    videoElem.currentTime = nextFrame / 1000;
  });
  
  $('#slowdown').click(function() {
    var currentRate = videoElem.playbackRate;
    if (currentRate <= 0.1) {
      return;
    } else if (currentRate <= 1) {
      videoElem.playbackRate = currentRate - 0.1;
    } else {
      videoElem.playbackRate = currentRate - 0.5;
    }
  })
  
  $('#speedUp').click(function() {
    var currentRate = videoElem.playbackRate;
    videoElem.playbackRate = currentRate + 0.5;
  });
  
  $('#resetSpeed').click(function() {
    videoElem.playbackRate = 1;
  });
  
  $('#submit').click(function(e) {
    e.preventDefault();
    var csrftoken = getCookie('csrftoken');
    var imageData = getFrameData();
    var description = $('#report-description').val();
    var formData = new FormData();
    $('#submit').hide();
    $('.js-submit-div').text('Submitting Report...')
    formData.append('frame_base64', imageData);
    formData.append('description', description);
    formData.append('video', VIDEO_ID);
    formData.append('timecode', Math.floor(videoElem.currentTime * 1000))
    fetch('/add_report', {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrftoken
      },
      body: formData
    })
    .then(response => response.json())
    .then(data => {
      const reportId = data.report_id;
      const $a = $('<a />').prop('href', '/report/video/' + reportId).text('Report Submitted');
      $('.js-submit-div').empty().append($a);
    })
    .catch(e => console.log('error', e))
  });

  $(document).keyup(function(e) {
    e.preventDefault();
    if (isFocussed) {
      return;
    }
    switch (e.keyCode) {
      case 37: // left arrow
        $('#goBack').click();
        break;
      case 39: // right arrow
        $('#goForward').click();
        break;
      case 83: // s
        $('#slowdown').click();
        break;
      case 70: // f
        $('#speedUp').click();
        break;
      case 32: // space
        $('#pauseVideo').click();
        break;
      case 82: // r
        $('#resetSpeed').click();
        break;
      default:
        return;
    }
  });
});