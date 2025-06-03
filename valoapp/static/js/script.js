(function ($) {

  "use strict";

function updateTimers() {
  const currentTime = Math.floor(Date.now() / 1000);

  document.querySelectorAll("[id^=timer-]").forEach(timer => {
    const endTime = parseInt(timer.dataset.endtime);
    if (isNaN(endTime)) {
      console.error("Invalid end time for", timer.id);
      return;
    }

    let timeLeft = endTime - currentTime;

    if (timeLeft > 0) {
      let days = Math.floor(timeLeft / (60 * 60 * 24));
      let hours = Math.floor((timeLeft % (60 * 60 * 24)) / 3600);
      let minutes = Math.floor((timeLeft % 3600) / 60);
      let seconds = timeLeft % 60;

      timer.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;

    } 
    else {
      timer.innerHTML = "Bidding Closed";
      let row = timer.closest("tr");
      if (row) {
        let button = row.querySelector("button");
        if (button) button.disabled = true;
      }
    }
  });
}

setInterval(updateTimers, 1000);
updateTimers();


  // init jarallax parallax
  var initJarallax = function () {
    jarallax(document.querySelectorAll(".jarallax"));

    jarallax(document.querySelectorAll(".jarallax-img"), {
      keepImg: true,
    });
  }

  // input spinner
  var initProductQty = function(){

    $('.product-qty').each(function(){

      var $el_product = $(this);
      var quantity = 0;

      $el_product.find('.quantity-right-plus').click(function(e){
          e.preventDefault();
          var quantity = parseInt($el_product.find('.quantity').val());
          $el_product.find('.quantity').val(quantity + 1);
      });

      $el_product.find('.quantity-left-minus').click(function(e){
          e.preventDefault();
          var quantity = parseInt($el_product.find('.quantity').val());
          if(quantity>0){
            $el_product.find('.quantity').val(quantity - 1);
          }
      });

    });

  }

  // init Chocolat light box
	var initChocolat = function () {
		Chocolat(document.querySelectorAll('.image-link'), {
			imageSize: 'contain',
			loop: true,
		})
	}

  // Animate Texts
  var initTextFx = function () {
    $('.txt-fx').each(function () {
      var newstr = '';
      var count = 0;
      var delay = 0;
      var stagger = 10;
      var words = this.textContent.split(/\s/);
      
      $.each( words, function( key, value ) {
        newstr += '<span class="word">';

        for ( var i = 0, l = value.length; i < l; i++ ) {
          newstr += "<span class='letter' style='transition-delay:"+ ( delay + stagger * count ) +"ms;'>"+ value[ i ] +"</span>";
          count++;
        }
        newstr += '</span>';
        newstr += "<span class='letter' style='transition-delay:"+ delay +"ms;'>&nbsp;</span>";
        count++;
      });

      this.innerHTML = newstr;
    });
  }

  $(document).ready(function () {

    initProductQty();
    initJarallax();
    initChocolat();
    initTextFx();

    $(".user-items .search-item").click(function () {
      $(".search-box").toggleClass('active');
      $(".search-box .search-input").focus();
    });
    $(".close-button").click(function () {
      $(".search-box").toggleClass('active');
    });

    var breakpoint = window.matchMedia('(max-width:61.93rem)');

    if (breakpoint.matches === false) {
      
      var swiper = new Swiper(".main-swiper", {
        slidesPerView: 1,
        spaceBetween: 48,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        autoplay: {
          delay: 3000, // Adjust the delay (in milliseconds) as needed
          disableOnInteraction: false, 
        },
        breakpoints: {
          800: {
            slidesPerView: 2,
            spaceBetween: 48,
          },
        },
      });

      // homepage 2 slider
      var swiper = new Swiper(".thumb-swiper", {
        direction: 'horizontal',
        slidesPerView: 6,
        spaceBetween: 6,
        breakpoints: {
          900: {
            direction: 'vertical',
            spaceBetween: 6,
          },
        },
      });
      var swiper2 = new Swiper(".large-swiper", {
        spaceBetween: 48,
        effect: 'fade',
        slidesPerView: 1,
        pagination: {
          el: ".swiper-pagination",
          clickable: true,
        },
        thumbs: {
          swiper: swiper,
        },
      });

    }

    // product single page
    var thumb_slider = new Swiper(".product-thumbnail-slider", {
      slidesPerView: 5,
      spaceBetween: 10,
      // autoplay: true,
      direction: "vertical",
      breakpoints: {
        0: {
          direction: "horizontal"
        },
        992: {
          direction: "vertical"
        },
      },
    });

    // product large
    var large_slider = new Swiper(".product-large-slider", {
      slidesPerView: 1,
      // autoplay: true,
      spaceBetween: 0,
      effect: 'fade',
      thumbs: {
        swiper: thumb_slider,
      },
      pagination: {
        el: ".swiper-pagination",
        clickable: true,
      },
    });

    

  }); // End of a document

  $(window).load(function(){
    $('.preloader').fadeOut();
  });

})(jQuery);