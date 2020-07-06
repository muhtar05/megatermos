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

$(document).ready(function(){


    (function(){
        //Сохраняем ссылку на стандартный метод jQuery
        var originalAddClassMethod = jQuery.fn.addClass;
        //Переопределяем
        $.fn.addClass = function(){
            var result = originalAddClassMethod.apply(this, arguments);
            //Инициализируем событие смены класса
            $(this).trigger('cssClassChanged');
            return result;
        }
    })();

    var scrolling = 0;
    $(window).scroll(function(){
      scrolling = $(this).scrollTop();
    });

    var wWidth = $(window).width();
    $(window).resize(function(){
      wWidth = $(window).width();
    });

    $('.button, .button-o').each(function(){
    	let texts = $(this).html();
    	$(this).html('');
    	$(this).append('<span class="relative">'+texts+'</span>');
    });

    $('.homeslider').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: true,
        mouseDrag: false,
        autoplay: false,
        autoplayTimeout: 7000,
        autoHeight: false,
        animateOut: 'fadeOut',
        animateIn: 'fadeIn',
        navText: ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
    });

    $('.single_prod_slider').owlCarousel({
        items: 1,
        loop: true,
        nav: true,
        dots: false,
        mouseDrag: false,
        autoplay: false,
        autoplayTimeout: 7000,
        autoHeight: false,
        navText: ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
    });

    var sliderCountSlides = $('.slider').data('slides');
    $('.slider').owlCarousel({
        items: sliderCountSlides,
        loop: true,
        nav: true,
        dots: true,
        mouseDrag: false,
        autoplay: false,
        autoplayTimeout: 7000,
        autoHeight: false,
        margin: 0,
        responsive: {
          0 : {
            items: 1,
            nav: false
          },
          421 : {
            items: 2,
            nav: false
          },
          700 : {
            items: sliderCountSlides,
            nav: true
          }
        },
        navText: ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
    });

    $('.products_carousel').owlCarousel({
        items: 4,
        loop: false,
        nav: true,
        dots: false,
        mouseDrag: false,
        autoplay: false,
        autoplayTimeout: 7000,
        autoHeight: true,
        margin: 0,
        responsive: {
          0 : {
            items: 1,
            margin: 10,
            center: true
          },
          500 : {
            items: 2,
            margin: 10
          },
          800 : {
            items: 3,
            margin: 20
          },
          1024 : {
          	items: 4,
            margin: 20
          },
          1300 : {
            items: 4
          }
        },
        navText: ['<i class="fa fa-angle-left"></i>','<i class="fa fa-angle-right"></i>']
    });


    // SUBMENU ARROW
    $('.tm_submenu, .sidebar_submenu, .sidebar_subblock, .catalog_submenu').parent('li').addClass('submenu_arrow');
    $('.sidebar_submenu > li.current').parent().closest('li').addClass('opened');

    // SCROLL TO TOP
    $('.backtop').click(function(e) {
        e.preventDefault();
        $('body, html').animate({
            scrollTop : 0
        }, 1200);
    });


    // ПРИКЛЕЙКА МЕНЮ К ВЕРХУ ПРИ СКРОЛЛЕ
    if ( $('.topnav_sec').length ) {
     var stickyNavTop = $('.topnav_sec').offset().top;

     var stickyNav = function(){
          let scrollTop = $(window).scrollTop();
                
          if (scrollTop > stickyNavTop ) { 
              $('.topnav_sec').addClass('fixed'); 
          } else {
              $('.topnav_sec').removeClass('fixed'); 
          }
      };
       
      stickyNav();
       
      $(window).scroll(function() {
          stickyNav();
      });
    }

    // Replace all SVG images with inline SVG
    $('img.svg').each(function(){
      var $img = $(this);
      var imgID = $img.attr('id');
      var imgClass = $img.attr('class');
      var imgURL = $img.attr('src');

      $.get(imgURL, function(data) {
          // Get the SVG tag, ignore the rest
          var $svg = $(data).find('svg');

          // Add replaced image's ID to the new SVG
          if(typeof imgID !== 'undefined') {
              $svg = $svg.attr('id', imgID);
          }
          // Add replaced image's classes to the new SVG
          if(typeof imgClass !== 'undefined') {
              $svg = $svg.attr('class', imgClass+' replaced-svg');
          }

          // Remove any invalid XML tags as per http://validator.w3.org
          $svg = $svg.removeAttr('xmlns:a');

          // Check if the viewport is set, if the viewport is not set the SVG wont't scale.
          if(!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
              $svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'))
          }

          // Replace image with new SVG
          $img.replaceWith($svg);

      }, 'xml');

    });


    // CHECKBOXES / RADIO
    $(document).on('click', '.rd + label, .button_filter + label, .product_option_rd + label', function(){
        $(this).prev('input').click();
    });

    $(document).on('click', '.ch + label',function(){
        var prevInput = $(this).prev('input');
        prevInput.click();
        getProductShowCount();
    });

    $(".clear_filters").on('click', function(e){
        var currentPathName = document.location.pathname;
        document.location.href = currentPathName;
    })

    function getProductShowCountTest(){
        var checkedElements = $('.sidebar_menu').find('.filter_checkbox:checked');
        var parametersUrl = "";
        $.each(checkedElements, function (i, v) {
            parametersUrl += $(this).data('name') + "=" + $(this).val() + "&";
        });
        var filterFormData = $("#filter-form").serialize();
        // var hashes = filterFormData.split('&');
        // for (var i in hashes) {
        //     var hash = hashes[i].split('=');
        //     if ((hash[0].indexOf("slider")) == -1) {
        //         if (hash[0] in options) {
        //             options[hash[0]] = options[hash[0]] + ',' + hash[1];
        //         } else {
        //             options[hash[0]] = hash[1];
        //         }
        //     }
        // }
        $.ajax({
            url: '/catalog/get_filter/',
            cache: 'false',
            data: filterFormData,
        }).done(function (data) {

            $("#product-count").html(data.num_count);
            $('.filter_results_tag').show();
        }).fail(function () {
            alert('Error');
        });
    }

    function getProductShowCount(){
        var filterFormData = $("#filter-form").serialize();
        $.ajax({
            url: '/catalog/get_filter/',
            cache: 'false',
            data: filterFormData,
        }).done(function (data) {
            $("#product-count").html(data.num_count);
            $('.filter_results_tag').show();
        }).fail(function () {
            alert('Error');
        });
    }

    $(".sort_products").on("change", function(e){
        var currentSort = $(this).val();
        window.location.href = document.location.pathname + "?order=" + currentSort;
    });

    $('.filter_results_tag').on('click', function (e) {
        e.preventDefault();
        var checkedElements = $('.sidebar_menu').find('.filter_checkbox:checked');
        console.log(checkedElements);
        var parametersUrl = "";
        var paremeterResult = {};
        $.each(checkedElements, function (i, v) {
            var attrName = $(this).data('name');
            var optionCode = $(this).data('code');
            if (paremeterResult.hasOwnProperty(attrName)) {
                var currentOptions = paremeterResult[attrName];
                paremeterResult[attrName].push(optionCode);
            } else {
                paremeterResult[attrName] = [optionCode];
            }
            parametersUrl += $(this).data('name') + "=" + $(this).val() + "&";
        });

        var priceFromValue = parseInt($("input[name=price-min]").val());
        var priceFromMinValue = parseInt($("input[name=price-min]").data('minvalue'));
        if(priceFromValue > priceFromMinValue){
            paremeterResult['price_from'] = priceFromValue;
        }

        var priceToValue = parseInt($("input[name=price-max]").val());
        var priceToMaxValue = parseInt($("input[name=price-max]").data('maxvalue'));

        if(priceToValue < priceToMaxValue){
            paremeterResult['price_to'] = priceToValue;
        }

        parametersUrl += "price-min=" + $("input[name=price-min]").val() + "&";
        parametersUrl += "price-max=" + $("input[name=price-max]").val();
        var fullUrl = "/";

        $.each(paremeterResult, function (i, v) {
            if (i == 'price_to' || i == 'price_from'){
                fullUrl += i + "_" + v + "/";
            } else {
                var sortElements = v.sort();
                fullUrl += i + "_" + sortElements.join("_") + "/";
            }
        });

        console.log(paremeterResult);

        var currentPathList = document.location.pathname.split("/");
        var currentPathUrl = "/" + currentPathList[1] + "/" + currentPathList[2]  + fullUrl;

        window.location.href = currentPathUrl;
    });


    // TABS
    $('.tabs_container div.tab:not(:first)').hide();
    $('.tabs_nav:not(.links) li').click(function(event) {
        event.preventDefault();
        $('.tabs_container div.tab').hide();
        $('.tabs_nav .current').removeClass("current");
        $(this).addClass('current');

        var clicked = $(this).find('a:first').attr('href');
        $('.tabs_container ' + clicked).fadeIn('fast');
    }).eq(0).addClass('current');

    
    // МАСКА ТЕЛЕФОНА
    jQuery(function($){
        $('input[type=tel]').mask('+7 (999) 999-99-99');
    });

    // ACCORDIONS
    $('.accordion_item.active').children('.ac_content').show();
    $('.accordion_item h4').click(function(){
        var display = $(this).parent().children('.ac_content').css('display');
        if ( display == 'none' ) {
            $('.accordion_item').removeClass('active');
            $('.accordion_item').children('.ac_content').slideUp(300);
            
            $(this).parent().addClass('active');
            $(this).parent().children('.ac_content').slideDown(300);
            
            // SCROLL TO BEGINING OF ACCORDION CLICKED
            if ( $(window).width() <= 800) {
                var that = $(this);
                setTimeout(function() {
                  var offset = that.offset().top;
                  $('html,body').animate({ scrollTop: offset-110 }, 700);
                }, 300);
            }
        } else {
            $('.accordion_item').removeClass('active');
            $('.accordion_item').children('div').slideUp(300);
        }
        
    });


    $('.sidebar_menu > li.submenu_arrow > a[href="#"]').click(function(){
        var display = $(this).parent().children('.sidebar_submenu, .sidebar_subblock').css('display');
        if ( display == 'none' ) {
            // $('.sidebar_menu > li').removeClass('opened');
            // $('.sidebar_menu > li').children('.sidebar_submenu, .sidebar_subblock').hide();
            
            $(this).parent().addClass('opened');
            $(this).parent().children('.sidebar_submenu, .sidebar_subblock').show();
        } else {
            $(this).parent().removeClass('opened');
            // $('.sidebar_menu > li').removeClass('active');
            // $('.sidebar_menu > li').children('.sidebar_submenu, .sidebar_subblock').hide();
        }
        return false;        
    });

  // ONLY NUMBERS
  $('.numbersOnly, .counter_input, .counter_big_input, .range_input').bind("change keyup input click", function() {
      if (this.value.match(/[^0-9]/g)) {
          this.value = this.value.replace(/[^0-9]/g, '');
      }
  });

	// MODAL
	$('.modal_overlay, .modal_close, .close_modal').click(function(){
	  $(this).closest('.sidebar, .modal').removeClass('visible');
	  $('.minicart_open').removeClass('active');
	  return false;
	});

    
    // DATE CALENDAR
    $('.date').keypress(function(e) {
        var verified = (e.which == 8 || e.which == undefined || e.which == 0) ? null : String.fromCharCode(e.which).match();
        if (verified) {
        e.preventDefault();
        }
    });

    $('.date').datepicker({
        keyboardNavigation: false,
        autoclose: true,
        todayHighlight: true,
        startDate: new Date(),
        weekStart: 1,
        format: {
          toDisplay: function(date, format, language) {
            moment.locale('ru');
            let toDisp = moment(date).format('DD MMM YYYY');
            return toDisp;
          },
          toValue: function(date, format, language) {
            moment.locale('ru');
            let toVal = moment(date).format('L');
          }
        },
        orientation: 'bottom',
        language: 'ru'
    });




    $(document).on('click', '.counter_ctrl.minus, .counter_big_ctrl.minus', function () {
        let $input = $(this).parent().find('.counter_input, .counter_big_input');
        let min = $input.data('min');
        let count = parseInt($input.val()) - 1;
        count = count < min ? min : count;
        $input.val(count);
        $input.change();
        return false;
    });

    $(document).on('click', '.counter_ctrl.plus, .counter_big_ctrl.plus', function () {
        let $input = $(this).parent().find('.counter_input, .counter_big_input');
        let max = $input.data('max');
        let count = parseInt($input.val()) + 1;
        count = count > max ? max : count;
        $input.val(count);
        $input.change();
        return false;
    });

    $('.cart_table .counter_big_input').on('change', function(){
        let clos = $(this).closest('tr');
    	if ( $(this).val() < $(this).data('min') ) {
    		$(this).val( $(this).data('min') );
    	}
    	if ( $(this).val() > $(this).data('max') ) {
    		$(this).val( $(this).data('max') );
    	}

    	var currentValue = $(this).val();
    	var productId = $(this).data('product');

    	$.ajax({
            method: "POST",
            url: "/basket/changequantity/",
            data: {
                value: currentValue,
                product_id: productId,
            },
            beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
    	}).done(function(data){
    	    console.log(data);
    	    if (data.status == 'ok'){
                $('.header_cart .header_count').html(data.num_items);
                $('#total_no_spec').html(data.total_sum + " ₽");
                $('#total_price').html(data.total_sum + " ₽");
                clos.find('.cart_prod_final_price b').text(data.line_sum + " ₽");
            }
        }).fail(function (errors) {
            console.log(errors);
        });
    });

    $(".ip_city input[name=city]").change(function(e){
        $("#city-choice-form").submit();
    });

    $('.counter_input').on('change', function(){
    	if ( $(this).val() < $(this).data('min') ) {
    		$(this).val( $(this).data('min') );
    	}
    	if ( $(this).val() > $(this).data('max') ) {
    		$(this).val( $(this).data('max') );
    	}

    	var currentValue = $(this).val();
    	var productId = $(this).data('product');

    	$.ajax({
            method: "POST",
            url: "/basket/changequantity/",
            data: {
                value: currentValue,
                product_id: productId,
            },
            beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
    	}).done(function(data){
    	    console.log(data);
    	    if (data.status == 'ok'){
                $('.header_cart .header_count').html(data.num_items);

            }
        }).fail(function (errors) {
            console.log(errors);
        });

    });

    // $('.counter_input, .counter_big_input').on('change', function(){
    // 	if ( $(this).val() < $(this).data('min') ) {
    // 		$(this).val( $(this).data('min') );
    // 	}
    // 	if ( $(this).val() > $(this).data('max') ) {
    // 		$(this).val( $(this).data('max') );
    // 	}
    // });

    // CART COUNT CHANGE & FINAL PRICE
	(function() {
		var currencySymbol = $('.cart_table').data('currency');
	    // $('.cart_table .counter_big_input').on('change', function(){
	    // 	let clos = $(this).closest('tr');
	    // 	let count = parseInt( $(this).val() );
	    // 	let price, oldPrice;
	    // 	if ( $('.cart_specprice_th').length ) {
	    // 		price = clos.find('.cart_specprice').text();
	    // 		price = parseInt(price);
	    // 		clos.find('.cart_prod_final_price b').text(price*count + currencySymbol);
	    // 	} else {
	    // 		price = clos.find('.cart_price_old').text();
	    // 		price = parseInt(price);
	    // 		clos.find('.cart_prod_final_price b').text(price*count + currencySymbol);
	    // 	}
	    // 	// calculateFinalPrice();
	    // });

	    function calculateFinalPrice() {
	        alert("calculate Price");
	    	let delivery = $('#delivery_val').text();
	    		delivery = parseInt(delivery);
			let specTotal = 0;
			let noSpec = 0;
			let count = 0;

	    	if (isNaN(delivery)) { delivery = 0; }

	    	if ( $('.cart_specprice_th').length ) { // если есть спеццена

	    		$('.cart_table .cart_prod_final_price b').each(function(){
	    			specTotal = specTotal + parseInt( $(this).text() );
	    		});

	    		$('.cart_table .cart_price_old').each(function(){
	    			let count = $(this).closest('tr').find('.counter_big_input').val();
	    			let that = parseInt( $(this).text() ) * count;
	    			noSpec = noSpec + that;
	    		});

	    		$('#total_no_spec').text(noSpec + currencySymbol);
	    		$('#total_price').text(specTotal + delivery + currencySymbol);
	    	
	    	} else { // если нет колонки спеццены
	    		$('.cart_table .cart_prod_final_price b').each(function(){
	    			specTotal = specTotal + parseInt( $(this).text() );
	    		});
	    		$('#total_no_spec').text(specTotal + currencySymbol);
	    		$('#total_price').text(specTotal + delivery + currencySymbol);
	    	}

	    }
	})();


    /* MINI CART FADE OUT */

    $(document).mouseup(function (e){
        var div = $('.catalog_menu_box, .catalog_open');
        if (!div.is(e.target) && div.has(e.target).length === 0) {
            $('.catalog_menu_box, .catalog_open').removeClass('opened');
        }
    });

    $('.open_modal').click(function(){
      var ident = $(this).attr('href');
      var content = $(ident);
      var height = content.find('.modal_content').outerHeight();
      var viewport = $(window).height();
      var center = (viewport / 2) - (height / 2);

      content.css('top', scrolling);
      if ( height >= viewport ) {
        content.find('.modal_content').css('top', '2vh');
      } else {
        content.find('.modal_content').css('top', center);        
      }

      $(ident).addClass('visible');
      return false;
    });

    $('.fancy').fancybox({
      loop: true
    });



    // Isotope filter
    $(window).on('load', function(){
      var $container = $('#filterable').isotope({
          // options
      });
      // filter items on button click
      $('#filters').on( 'click', 'button', function() {
          var filterValue = $(this).attr('data-filter');
          $container.isotope({ filter: filterValue });
          
          // fancybox albums for visible items
          if ( $('.gallery_item').length ) {
            if (filterValue) {
              $('.gallery_item').attr('data-fancybox', 'none');
              $(filterValue).attr('data-fancybox', 'gallery');
            } else {
              $('.gallery_item').attr('data-fancybox', 'gallery');
            }
          }

          // Reviews zebra stripes
          if ( $('.review_row').length ) {
            if (filterValue) {
              $('.review_row'+filterValue).each(function(index){
                let num = index + 1;
                if ( num % 2 == 0 ) {
                  $(this).addClass('stripe');
                }
              });
            } else {
              $('.review_row').removeClass('stripe');
            }
          }


      });
      // change is-checked class on buttons
      $('#filters').each( function( i, buttonGroup ) {
          var $buttonGroup = $( buttonGroup );
          $buttonGroup.on( 'click', 'button', function() {
            $buttonGroup.find('.current').removeClass('current');
            $(this).addClass('current');
          });
      });      
    });


    // OPEN-CLOSE CHANGE PASSORD ROW
    $('.change_password_link').click(function(){
    	$(this).hide();
    	$('.change_password_row').css('display', 'flex');
    	$('.cancel_change_password_link').show();
    	$('.change_password_row .ip_cell:first-child input.input_text').focus();
    	return false;
    });
    $('.cancel_change_password_link').click(function(){
    	$(this).hide();
    	$('.change_password_row').hide();
    	$('.change_password_row .input_text').val('');
    	$('.change_password_link').show();
    	return false;
    });



    // EDIT PERSONAL INFO
    $('.edit_personal_info').click(function(){
    	$(this).hide();
    	$('.save_personal_info').show();
    	$('.personal_info .input_text').removeAttr('disabled');
    	$('.personal_info .ip_cell:first-child input.input_text').focus();
    	return false;
    });

    // TAKEOF or DELIVERY
    $('.rd').change(function(){
    	if ( $(this).attr('id') == 'takeof' ) {
    		$('.delivery_fields').slideUp(400);
    	}
    	if ( $(this).attr('id') == 'delivery' ) {
    		$('.delivery_fields').slideDown(400);
    	}
    });

    // PRICE SLIDER
    (function () {
      var range = $('.range_slider_box');
      var minVal = range.data('min');
      var maxVal = range.data('max');
      var stepVal = range.data('max');
      range.ionRangeSlider({
          type: 'double',
          grid: true,
          min: minVal,
          max: maxVal,
          step: stepVal,
          prefix: "",
          drag_interval: true
      });

      range.on('change', function () {
        rangeValueFrom = $(this).data('from');
        rangeValueTo = $(this).data('to');
        $('.range_input.from').val(rangeValueFrom).attr('data-value', rangeValueFrom);
        $('.range_input.to').val(rangeValueTo).attr('data-value', rangeValueTo);
        getProductShowCount();
      });

      var range_instance = range.data("ionRangeSlider");

      $('.range_input.from').on('change', function(){
      	let fromVal = parseInt($(this).val());
      	if( fromVal < minVal ) {
      		$(this).val(minVal + ' ₽' );
      	} else {
      		$(this).val( $(this).val() + ' ₽' );
      	}
        range_instance.update({
          from: fromVal
        });
      });

      $('.range_input.to').on('change', function(){
      	let toVal = parseInt($(this).val());
      	if( toVal > maxVal ) {
      		$(this).val(maxVal + ' ₽' );
      	} else {
      		$(this).val( $(this).val() + ' ₽' );
      	}
        range_instance.update({
          to: toVal
        });
      });


    })();

    $("#write_review_form_modal").submit(function (e) {
        e.preventDefault();
        var _this = $(this);
        $.ajax({
            method: "POST",
            url: $(this).attr('action'),
            data: $(this).serialize(),
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }).done(function (data) {
            alert(data.status);
            if(data['status'] == 'fail'){
                var errors_data =  $.parseJSON(data['errors']);
                for(var name in errors_data) {
                    for(var i in errors_data[name]) {
                        $("input[name='" + name + "']").after("<p style='color:#ff0000;'>" + errors_data[name][i].message + "</p>");
                        $("textarea[name='" + name + "']").after("<p style='color:#ff0000;'>" + errors_data[name][i].message + "</p>");
                    }
                }
            } else {
                _this.parent().html('<div class="alert alert-success text-center"><h5>Ваш отзыв добавлен</h5></div>');
            }
        }).fail(function (errors) {
            alert("Error");
            console.log(errors);
        });

    });


    $('.add_to_wishlist').click(function(){
        var _this = $(this);
        var productId = $(this).data('product');
        if (_this.hasClass("liked")){
            $.ajax({
                method: "POST",
                url: "/wishlists/deleteproduct/",
                data: {
                    'product_id': productId,
                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }).done(function (data) {
                $(".header_wishlist .header_count").html(data.num_items);
                _this.removeClass('liked');
                console.log(data);
            }).fail(function (errors) {
                alert("Error");
                console.log(errors);
            });
        } else {
            $.ajax({
                method: "POST",
                url: "/wishlists/addproduct/",
                data: {
                    'product_id': productId,
                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }).done(function (data) {
                $(".header_wishlist .header_count").html(data.num_items);
                _this.addClass('liked');
                console.log(data);
            }).fail(function (errors) {
                alert("Error");
                console.log(errors);
            });
        }
        return false;
    });


    $('.product-buy').click(function(e){
        e.preventDefault();
        var _this = $(this);
        var currentValue = $('.counter_big_input').val();
    	$(this).parent().find('.counter_big_box').hide();
    	var productId = $(this).data('product');

    	$.ajax({
            method: "POST",
            url: "/basket/add/" + productId +"/",
            data: {
                'product_id': productId,
                'quantity': currentValue,
            },
            beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
    	}).done(function(data){
    	    if (data.status == 'ok') {
                _this.hide();
                $('.to-basket').show();
                $('.header_cart .header_count').html(data.num_items);
            }

    	    console.log(data);
        }).fail(function (errors) {
            alert("Error");
            console.log(errors);
        });
    });

    // ADD TO CART - SHOW COUNTER BOX
    $('.product_item-buy').click(function(){
        var _this = $(this);
    	$(this).hide();
    	$(this).parent().find('.product_item-counter_box').show();
    	var productId = $(this).data('product');

    	$.ajax({
            method: "POST",
            url: "/basket/add/" + productId +"/",
            data: {
                'product_id': productId,
            },
            beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
    	}).done(function(data){
    	    if (data.status == 'ok') {
                _this.parent().find('.product_added').addClass('visible');
                $('.header_cart .header_count').html(data.num_items);

            }

    	    console.log(data);
        }).fail(function (errors) {
            alert("Error");
            console.log(errors);
        });

    	return false;
    });

    $('.close_add_to_cart').click(function(){
        var _this = $(this);
        var productId = _this.data('product');

    	$.ajax({
            method: "POST",
            url: "/basket/delete/" + productId +"/",
            data: {
                'product_id': productId,
            },
            beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
    	}).done(function(data){
    	    _this.closest('.product_item-counter_box').hide();
    	    _this.closest('.product_item-buttons').find('.product_item-buy').show();
    	    _this.parent().parent().find('.product_added').removeClass('visible');
    	    $('.header_cart .header_count').html(data.num_items);
    	    console.log(data);
        }).fail(function (errors) {
            alert("Error");
            console.log(errors);
        });
    	return false;
    });


    $('.history_arrow').click(function(){
    	$(this).closest('table').toggleClass('opened ');
    	return false;
    });

    $('.attach_file_simulate').click(function(){
    	$('#attach_file').click();
    	return false;
    });

    // PRODUCTS IMAGES SWITCH
    $('.product_thumb').click(function(){
    	let href = $(this).attr('href');
    	$('.product_main_image').attr('href', href);
    	$('.product_main_image img').attr('src', href);
    	$('.product_thumb').removeClass('active');
    	$(this).addClass('active');
    	return false;
    });

    $('.product_main_image').click(function(){
      let fancy = $(this).attr('data-fancybox');
      $('.product_thumb').removeClass('fancy');
      $('.product_thumb:not(.active)').addClass('fancy');
    });

    $('.product_anchor').click(function(){
    	let href = $(this).attr('href');
    	let where = $(href).offset().top;
    	$('body, html').animate({scrollTop: where}, 1000);
    	return false;
    });

    function minicartScrollHeight() {
    	var minicartHeader = $('.minicart_content header').outerHeight();
    	var minicartFooter = $('.minicart_footer').outerHeight();
    	var total = $(window).height() - minicartHeader - minicartFooter;
    	$('.minicart_list').css('max-height', total);
    }

    $(window).on('load', function(){
    	minicartScrollHeight()
    });
    
    $(window).resize(function(){
    	minicartScrollHeight()
    });

    $('.minicart_open, .open_mobile_cart').click(function(){
    	$(this).addClass('active');
    	$('#modal_minicart').addClass('visible ');
    	return false;
    });

    $('.popup_close, .close_popup').click(function(){
    	$(this).closest('.popup').hide();
    	return false;
    });


    $('.topnav_search_input').on('keyup', function(){
        var _this = $(this);
        var parentSearchDiv = $('.search_dropdown_product').parent();
        var productHtml;
    	if ( $(this).val() != '' ) {
    	    $.ajax({
                method: "POST",
                url: "/catalog/search/",
                data: {
                    search_term: _this.val()
                },
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
    	    }).done(function(data){
    	        $(".search_dropdown_product").remove();
    	        $(".search_see_all").remove();
    	        $.each(data.products, function(i,v){
    	            console.log(v);
    	            console.log(v['name']);
    	            productHtml = '<div class="search_dropdown_product">'
                            + '<a href="' + v["url"] +'" class="sdp_image"><img src="'+ v["img"] +'" alt=""></a>'
                            + '<div class="sdp_info_box"><a href="' + v["url"] +'">' + v["name"] + ' </a>'
                            + '<div class="sdp_artnum">Артикул: ' + v["artikul"] + '</div> <div class="sdp_prices">'
                            + '<span class="sdp_price">' + v["price"] + ' ₽</span><span class="instock">В наличии</span></div></div></div>';

    	            parentSearchDiv.append(productHtml);
                });
    	        parentSearchDiv.append('<a href="/catalog/search/?search_term=' + _this.val() +'" class="button search_see_all">Показать все</a>');
                $('.search_dropdown').show();

            }).fail(function (errors) {
                alert("Error");
                console.log(errors);
            });

    	} else {
    		$('.search_dropdown').hide();
    	}
    });

    var menuHeight = $('.catalog_menu').height();
    $('.catalog_menu .submenu_arrow').mouseover(function(){
    	let submenu = $(this).find('.catalog_submenu').height();
    	if ( submenu > menuHeight ) {
    		$('.catalog_menu').height(submenu);
    	}
    });

    $('.catalog_menu .submenu_arrow').mouseleave(function(){
    	$('.catalog_menu').height(menuHeight);
    });

    $('.catalog_open').click(function(){
    	if ( !$(this).hasClass('opened') ) {
    		$(this).addClass('opened');
    		$('.catalog_menu_box').addClass('opened');
    	} else {
    		$(this).removeClass('opened');
    		$('.catalog_menu_box').removeClass('opened');
    	}
    	return false;
    });

    $('.close_menu, .close_modal').click(function(){
    	$('.catalog_open').removeClass('opened');
    	$('.catalog_menu_box').removeClass('opened');
    	return false;
    });


    (function(){
		let cur = $('.paginate li.current');
		cur.prev('li').addClass('show');
		cur.prev('li').prev('li').addClass('show');
		cur.prev('li').prev('li').prev('li').addClass('show');

		cur.next('li').addClass('show');
		cur.next('li').next('li').addClass('show');
		cur.next('li').next('li').next('li').addClass('show');    	
    })();
    
    $('.sidebar_filters_box').each(function(){
    	let count = $(this).find('.ip_checkbox').length;
    	if ( count > 5 ) {
    		let toShow = count - 5;
    		$(this).find('.show_ch_filters').show();
    		$(this).find('.show_ch_filters span').text(toShow);
    	}
    });

    $('.show_ch_filters').click(function(){
    	$(this).hide();
    	$(this).closest('.sidebar_filters_box').find('.ip_checkbox').show();
    	return false;
    });

    $('.mobile_filters_button').click(function(){
    	$('.sidebar_filters').addClass('visible');
    	return false;
    });

    $('.open_mobile_search, .close_search_mobile').click(function(){
    	if ( $('.topnav_search_form').css('display') == 'none' ) {
    		$('.topnav_search_form').css('display', 'flex');
    	} else {
    		$('.topnav_search_form').hide();
        $('input.topnav_search_input').val('');
    	}
    	return false;
    });

    $('.close_search_mobile').click(function(){
    	$('.search_dropdown').hide();
    	return false;
    });

    $('.preview_close').click(function(){
      $('.preview').hide();
      return false;
    });

    $('.pageSelect').change(function(){
      let baseurl = $(this).data('url');
      let page = $(this).val();
      let url = baseurl + page;
      window.location.href = url;
    });

});


// BONUS TRACK
$(window).on('load', function(){
  if ( $('.bonus_item').length ) {
    if ( $(window).width() <= 568 ) {
      $('.bonus_item.active:last').show();
    }

  let item = $('.bonus_item:first').width();
  let offsetItem = $('.bonus_item.active:last').position().left;
  $('.bonus_past').width( offsetItem + (item/2) );

    $('.bonus_item').each(function(){
    let offsetItem = $(this).position().left;
    if ( $(this).is(':last-child')) {
      $(this).find('.bonus_item-price, .bonus_item_circle').css('background-position', -offsetItem + (item*2));
    } else {
      $(this).find('.bonus_item-price, .bonus_item_circle').css('background-position', -offsetItem);
    }
  });       
  }



  $('.sidebar_block').mousemove(function(evt){
    if ( evt.target.closest('.sidebar_block') ){
      let sidebar = $('.sidebar_block ').height();
      let target = evt.target.closest('.sidebar_block');
      let targetCoords = target.getBoundingClientRect();
      let yCoord = evt.clientY - targetCoords.top;
      if ( yCoord >= 25 && yCoord <= sidebar - 25 ) {
        $('.filter_results_tag').css('top', yCoord);
      }
    }
  });

  $('.sort_view_link').click(function(){
    let view = $(this).attr('href');
    $('.sort_view_link').removeClass('current');
    $(this).addClass('current');
    console.log(view);

    if ( view == '#view-row' ) {
      $('.catalog_box').addClass('catalog_view-row');
    } else {
      $('.catalog_box').removeClass('catalog_view-row');
    }
    return false;
  });

  $(function () {
    var parent = $('.product_box');
    if (parent.find('.product_thumbs_box').length == 1) {
      parent.find('.product_thumbs_box').css('display', 'none');
    }
  });

});