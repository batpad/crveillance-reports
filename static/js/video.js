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
    console.log('video onplay');
    $('#pauseVideo').text('Pause! (space)');
    $('.js-show-on-pause').hide();
  }
  
  videoElem.onloadedmetadata = function() {
    console.log('onloadedmetadata');
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
  
  $('.js-jumpToTimecode').click(function(e) {
    console.log('clicked');
    e.preventDefault();
    var timecode = Number($(this).attr('data-timecode'));
    console.log(timecode);
    videoElem.currentTime = timecode / 1000;
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
    var currentTimeMs = videoElem.currentTime * 1000;
    var nextFrame = currentTimeMs + 40;
    if (nextFrame / 1000 > videoElem.duration) {
      nextFrame = videoElem.duration * 1000;
    }
    videoElem.currentTime = nextFrame / 1000;
  });
  
  $('#markImage').click(function(e) {
    e.preventDefault();
    var imageData = getFrameData();
    var $img = $('<img />').prop('src', imageData);
    $('.js-highlightImage').empty().append($img).removeClass('hide');
    $('<div />')
      .prop('id','markercircle')
      .css('background','url('+ imageData +')')
      .css('clip-path', 'circle(10% at 50% 50%)')
      .appendTo('.js-highlightImage');
    $('.js-highlightImage').click( function(e) {
        var posX = ((e.pageX - $(this).offset().left)/$('#markercircle').width())*100,
            posY = ((e.pageY - $(this).offset().top)/$('#markercircle').height())*100;
        $('#markerleft').val(posX);
        $('#markertop').val(posY);
        $('#markercircle')
          .css('clip-path', 'circle('+$('#markersizer').val()+'% at '+posX+'% '+posY+'%)');
    });
    $('.js-highlightImage').after(
      '<input type="range" id="markersizer" name="markersizer" value="10" min="2" max="50"></input>'+
      '<input id="markerleft" name="markerleft" type="hidden" value="50"></input>'+
      '<input id="markertop" name="markertop" type="hidden" value="50"></input><br />' + 
      'Mark highlighted area in report: <input id="submit_highlight" type="checkbox" checked />')
    $('#markersizer').width('100%').change( function() {
      $('#markercircle').css('clip-path', 'circle('+$(this).val()+'% at '+
        $('#markerleft').val()+'% '+$('#markertop').val()+'%');
    });

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
    var title = $('#report-title').val();
    var reporterName = $('#report-name').val();
    var hasHighlight = $('#submit_highlight').length && $('#submit_highlight').prop('checked');
    var pointX, pointY, pointRadius;
    if (hasHighlight) {
      var pointX = Number($('#markerleft').val());
      var pointY = Number($('#markertop').val());
      var pointRadius = Number($('#markersizer').val());
    }
    var formData = new FormData();
    $('#submit').hide();
    $('.js-submit-div').text('Submitting Report...')
    formData.append('frame_base64', imageData);
    formData.append('description', description);
    formData.append('video', VIDEO_ID);
    formData.append('timecode', Math.floor(videoElem.currentTime * 1000));
    formData.append('title', title);
    formData.append('reporter_name', reporterName);
    if (hasHighlight) {
      formData.append('point_x', pointX);
      formData.append('point_y', pointY);
      formData.append('point_radius', pointRadius);
    }
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
    console.log('keyup');
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