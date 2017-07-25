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
