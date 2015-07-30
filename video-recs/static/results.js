
$(function(){
  $('.youTubeVideo').click(function(){
 		var vidtitle = $(this).parents('.videoThum').next('.videoInfo').find('h2').text();
		$('.video-container .iframe h2').text(vidtitle);
		var winWidth = $(window).width();
        var winHeight = $(window).height();
        var centerDiv = $('.popup');
        var left = winWidth / 2 - ((parseInt(centerDiv.css("width"))) / 2);
        var top = winHeight / 2 - ((parseInt(centerDiv.css("height"))) / 2);
        centerDiv.css({'left': left,'top': '15%'});
    		$('.youtube').show();
		  $('.popup.youtube, .overlaybg').show();
		 $("html,body").animate({scrollTop: 0}, 800);
 		var ind = $(this).parents('.videoThum').addClass('aaa').parents('.guideBox').siblings().find('.videoThum').removeClass('aaa');
		var linkSrc = $(this).parents('.videoThum').find('a').attr('rel');
		 $('.youtube .video-container').find('iframe').attr('src', linkSrc);
	});

	$('.close, .overlaybg').click(function(){
		$('.youtube .video-container').find('iframe').attr('src', '');
		$('.popup.youtube, .overlaybg').hide();
	});
	});	
