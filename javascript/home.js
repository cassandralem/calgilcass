var tag = document.createElement('script');

   tag.src = "https://www.youtube.com/iframe_api";
   var firstScriptTag = document.getElementsByTagName('script')[0];
   firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

   var player1;
   var player2;

   function onYouTubeIframeAPIReady() {
       player1 = new YT.Player('player1', {
         height: '500',
         width: '500',
         videoId: 'gtoknSe54gs',
         playerVars: { 'autoplay': 0, 'controls': 0, 'disablekb':1, 'modestbranding':1, 'rel':0 },
         events: {
               'onReady': onPlayerReady
           }
       });

       player2 = new YT.Player('player2', {
         height: '500',
         width: '500',
         videoId: 'fcsDG_jVYbc',
         playerVars: { 'autoplay': 0, 'controls': 0, 'disablekb':1 },
         events: {
               'onReady': stopVideo
           }
       });
   }


   function onPlayerReady(event) {
       event.target.playVideo();
   }

   function stopVideo() {
       player1.stopVideo();
       player2.stopVideo();
   }

   // menu js

   $(document).ready(function(){
	$('#nav-icon1').click(function(){
		$(this).toggleClass('open');
	});
});

function clickLike() {
  // Here, "this" is the button that the user clicked.
  var button = $(this);

  // Move through the DOM tree to find the "likes"
  // element that corresponds to the clicked button.

  // Look through parents of this to find .photo.
  var video = $(this).parents('.video-container');

  // Look inside photo to find .likes.
  var likes = $(video).find('.likes');

  // Get the URLsafe key from the button value.
  var urlsafeKey = $(button).val();

  // Send a POST request and handle the response.
  $.post('/likes', {'videos[0].video_id': urlsafeKey}, function(response) {
    // Update the number in the "like" element.
    $(likes).text(response);

  });
  alert('working');
}

$("form").submit(function(e){
    e.preventDefault();
});

$('.video-container button').click(clickLike);
