var tag = document.createElement('script');

   tag.src = "https://www.youtube.com/iframe_api";
   var firstScriptTag = document.getElementsByTagName('script')[0];
   firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

   var player1;
   var player2;
   var player1_url = "boot"
   var player2_url = ""


   function get_and_delete(){
    //  var player1El = $('#player1');
    //  var videoUrl = player1El.attr('value');
    //  console.log('VIDEO1 = ' + videoUrl);
     $.post('/getdeletevideo', function(response) {
       $(player1).get(response);
       player1_url = response
       alert(player1_url);
     $('#player1_iframe').attr("src", "https://www.youtube.com/embed/" + player1_url)

       // TODO: Use jQuery to select the correct iframe
       // TODO: Update the src attribute of the iframe with the video id, also set autoplay=1

      // onYouTubeIframeAPIReady(player1_url)
    });

   }

   $('#test').click(get_and_delete);

   function onYouTubeIframeAPIReady(player1_url) {
      // console.log(player1_url)
      //  player1 = new YT.Player('player1', {
      //    height: '500',
      //    width: '500',
      //    videoId: player1_url,
      //    playerVars: { 'autoplay': 1, 'controls': 0, 'disablekb':1, 'modestbranding':0, 'rel':0 },
      //
      //  });

       player2 = new YT.Player('player2', {
         height: '500',
         width: '500',
         videoId: 'vQdG3ks8-qY',
         playerVars: { 'autoplay': 1, 'controls': 0, 'disablekb':1, 'modestbranding':0, 'rel':0  },

       });
   };


//setInterval(function(onYouTubeIframeAPIReady){console.log("Hello")},10000);
/*
1 minute is up
decide if player1 or player2 win

loser = player2
new_url = response.newVideo
new YT.Player(loser, {
  height: '500',
  width: '500',
  videoId: new_url,
  playerVars: { 'autoplay': 1, 'controls': 0, 'disablekb':1, 'modestbranding':0, 'rel':0  },

});


*/


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
  $.post('/likes', {'video_key': urlsafeKey}, function(response) {
    // Update the number in the "like" element.
    $(likes).text(response);

  });
}

$("form").submit(function(e){
    e.preventDefault();
});

$('.video-container button').click(clickLike);

// menu section allows for section navigation

///Starting to linking database with videokeys in players








var menu = document.querySelector('.nav__list');
var burger = document.querySelector('.burger');
var doc = $(document);
var l = $('.scrolly');
var panel = $('.panel');
var vh = $(window).height();

var openMenu = function() {
  burger.classList.toggle('burger--active');
  menu.classList.toggle('nav__list--active');
};

// reveal content of first panel by default
panel.eq(0).find('.panel__content').addClass('panel__content--active');

var scrollFx = function() {
  var ds = doc.scrollTop();
  var of = vh / 4;

  // if the panel is in the viewport, reveal the content, if not, hide it.
  for (var i = 0; i < panel.length; i++) {
    if (panel.eq(i).offset().top < ds+of) {
     panel
       .eq(i)
       .find('.panel__content')
       .addClass('panel__content--active');
    } else {
      panel
        .eq(i)
        .find('.panel__content')
        .removeClass('panel__content--active')
    }
  }
};

var scrolly = function(e) {
  e.preventDefault();
  var target = this.hash;
  var $target = $(target);

  $('html, body').stop().animate({
      'scrollTop': $target.offset().top
  }, 300, 'swing', function () {
      window.location.hash = target;
  });
}

var init = function() {
  burger.addEventListener('click', openMenu, false);
  window.addEventListener('scroll', scrollFx, false);
  window.addEventListener('load', scrollFx, false);
  $('a[href^="#"]').on('click',scrolly);
};

doc.on('ready', init);
