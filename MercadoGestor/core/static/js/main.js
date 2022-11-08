
  
   function next (id,project) {
   var width=document.getElementById(project).offsetWidth;
   width>1000?width/=3:width*=1;
   var container = document.getElementById(id);
   sideScroll(container,'right',18,width,10);
   };
   
   function back(id,project) {
   var width=document.getElementById(project).offsetWidth;
   width>1000?width/=3:width*=1;
   var container = document.getElementById(id);
   sideScroll(container,'left',18,width,10);
   };
   
function sideScroll(element,direction,speed,distance,step){
    scrollAmount = 0;
    var slideTimer = setInterval(function(){
        if(direction == 'left'){
            element.scrollLeft -= step;
        } else {
            element.scrollLeft += step;
        }
        scrollAmount += step;
        if(scrollAmount > distance){
            window.clearInterval(slideTimer);
        }
    }, speed);
}


jQuery(document).ready(function ($) {

var owl = $('.owl-carousel');
owl.owlCarousel({
    autoplayHoverPause:true,
    video:true,
    autoplay:true,
    dotsEach:true,
    navText: [' <img class="d-none d-md-block" src="static/img/assets/icone_seta_esquerda.svg">',' <img class="d-none d-md-block" src="static/img/assets/icone_seta_direita.svg">'],
    nav:true,
    responsive:{
        0:{margin:33.33,
            items:1
        },
        600:{
          margin:33.33,
            items:2
        },
        900:{
          margin:10.33,
            items:4
        },
        1450:{
          margin:33.33,
            items:4
        }
    }
});
owl.on('mousewheel', '.owl-stage', function (e) {
    if (e.deltaY>0) {
        owl.trigger('next.owl');
    } else {
        owl.trigger('prev.owl');
    }
    e.preventDefault();
});


  // $(".tabs-doar" ).tabs();

  //  aguardando pagina de  projeto e entidade 
  // auto complete home page 
  // $("#project-entities-search-input").autocomplete({
  //   delay: 1,
  //   minLength: 2,
  //   source: function(request, response) {
  //     $.ajax({
  //       url: "/ps/core/list/projects/entity/",
  //       dataType: "json",
  //       data: {
  //         'term': request.term
  //       },
  //       success: function(data) {
  //         response($.map(data, function(item) {
  //           console.log(item)
  //           return {
  //             label: item.name,
  //             value: item.name,
  //             id: item.id,
  //             url: 'google.com'
  //           }
  //         }))
  //       }
  //     })
  //   },
  //   select: function(event, ui){
  //     console.log(ui.item)
  //   }
  // });


  //  subscribe form 
  $('#subscribe_form').submit(function(event){
    event.preventDefault()

    var form =  $(this);
    $.ajax({
        url:  form.attr('action'),
        type: form.attr('method'),
        data: form.serialize(),
        dataType: 'json',
        beforeSend:function(){

        },
        success: function(data){

          // if data is valid 
          let header = 'Pontos Solidarios | Subscribe '
          if (data.is_form_valid){
            let message = " Obrigado por se inscrever,"
            $("#result-text").removeClass("text-danger").text(message +" "+ data.result.email)

          } else{
            // add errors to  modal 
            $.each(data.errors, function(key, value){
              $("#result-text").append('span')
                .addClass("text-danger").text(key.toUpperCase() + ":" + " "+ value[0])
            });

          }
          $('#modal-result .modal-title').text(header);
          $('#modal-result').modal('show');

        }
    });

  })
  //  contact form 
    //  contact form 
    $('#contact_form').submit(function(event){
      event.preventDefault()

      var form =  $(this);
      $.ajax({
          url:  form.attr('action'),
          type: form.attr('method'),
          data: form.serialize(),
          dataType: 'json',
          beforeSend:function(){

          },
          success: function(data){

            // if data is valid 
            let header = 'Pontos Solidarios | Contato'
            if (data.is_form_valid){
              let message = "Agradecemos o contato, retornaremos em breve"
              $("#result-text").removeClass("text-danger").text(message)

            } else{
              // add errors to  modal 
              $.each(data.errors, function(key, value){
                $("#result-text").append('span')
                  .addClass("text-danger").text(key.toUpperCase() + ":" + " "+ value[0])
              });

            }
            $('#modal-result .modal-title').text(header);
            $('#modal-result').modal('show');

          }
      });

    })
  

  // Header fixed and Back to top button
  $(window).scroll(function () {
    if ($(this).scrollTop() > 100) {
      $('.back-to-top').fadeIn('slow');
      $('#header').addClass('header-fixed'); 
      $('#header-logo-white').addClass('hide')
      $('#header-logo-principal').removeClass('hide');
      $('.fa-bars').addClass('text-dark');
      $('.fa-bars').removeClass('color-bars');
    } else {
      $('.back-to-top').fadeOut('slow');
 
      $('#header').removeClass('header-fixed');
      $('#header-logo-white').removeClass('hide')
      $('#header-logo-principal').addClass('hide');
      $('.fa-bars').addClass('color-bars');
      $('.fa-bars').removeClass('text-dark');         
    }
  });
  $('.back-to-top').click(function () {
    $('html, body').animate({
      scrollTop: 0
    }, 1500, 'easeInOutExpo');
    return false;
  });

  // Initiate the wowjs
  new WOW().init();

  // Initiate superfish on nav menu
  $('.nav-menu').superfish({
    animation: {
      opacity: 'show'
    },
    speed: 400
  });

  // Mobile Navigation
  if ($('#nav-menu-container').length) {
    var $mobile_nav = $('#nav-menu-container').clone().prop({
      id: 'mobile-nav'
    });
    $mobile_nav.find('> ul').attr({
      'class': '',
      'id': ''
    });
    $('body').append($mobile_nav);
    $('body').prepend('<button type="button" id="mobile-nav-toggle"><i class="fa fa-bars color-bars"></i></button>');
    $('body').append('<div id="mobile-body-overly"></div>');
    $('#mobile-nav').find('.menu-has-children').prepend('<i class="fa fa-chevron-down"></i>');

    $(document).on('click', '.menu-has-children i', function (e) {
      $(this).next().toggleClass('menu-item-active');
      $(this).nextAll('ul').eq(0).slideToggle();
      $(this).toggleClass("fa-chevron-up fa-chevron-down fa-times fa-bars color-bars");
    });

    $(document).on('click', '#mobile-nav-toggle', function (e) {
      $('body').toggleClass('mobile-nav-active');
      $('#mobile-nav-toggle i').toggleClass('fa-times fa-bars color-bars');
      $('#mobile-body-overly').toggle();
    });

    $(document).click(function (e) {
      var container = $("#mobile-nav, #mobile-nav-toggle");
      if (!container.is(e.target) && container.has(e.target).length === 0) {
        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('#mobile-nav-toggle i').toggleClass('fa-times fa-bars color-bars');
          $('#mobile-body-overly').fadeOut();
        }
      }
    });
  } else if ($("#mobile-nav, #mobile-nav-toggle").length) {
    $("#mobile-nav, #mobile-nav-toggle").hide();
  }

  // Smoth scroll on page hash links
  $('a[href*="#"]:not([href="#"])').on('click', function () {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {

      var target = $(this.hash);
      if (target.length) {
        var top_space = 0;

        if ($('#header').length) {
          top_space = $('#header').outerHeight();
          if (!$('#header').hasClass('header-fixed')) {
            top_space = top_space - 20;
          }
        }

        $('html, body').animate({
          scrollTop: target.offset().top - top_space
        }, 1500, 'easeInOutExpo');

        if ($(this).parents('.nav-menu').length) {
          $('.nav-menu .menu-active').removeClass('menu-active');
          $(this).closest('li').addClass('menu-active');
        }

        if ($('body').hasClass('mobile-nav-active')) {
          $('body').removeClass('mobile-nav-active');
          $('#mobile-nav-toggle i').toggleClass('fa-times fa-bars color-bars');
          $('#mobile-body-overly').fadeOut();
        }
        return false;
      }
    }
  });

  // Porfolio filter
  $("#portfolio-flters li").click(function () {
    $("#portfolio-flters li").removeClass('filter-active');
    $(this).addClass('filter-active');

    var selectedFilter = $(this).data("filter");
    $("#portfolio-wrapper").fadeTo(100, 0);

    $(".portfolio-item").fadeOut().css('transform', 'scale(0)');

    setTimeout(function () {
      $(selectedFilter).fadeIn(100).css('transform', 'scale(1)');
      $("#portfolio-wrapper").fadeTo(300, 1);
    }, 300);
  });

  // jQuery counterUp
  $('[data-toggle="counter-up"]').counterUp({
    delay: 10,
    time: 1000
  });

  // custom code

});
