// Add scrolled effect for header
const topbar = $("#topbar");
const navbar = $("#navbar");
const scrollChange = 50;
$(window).scroll(function () {
    const scroll = $(window).scrollTop();

    if (scroll >= scrollChange) {
        topbar.addClass('topbar-scrolled');
        navbar.addClass('navbar-scrolled');
    } else {
        topbar.removeClass("topbar-scrolled");
        navbar.removeClass("navbar-scrolled");
    }
});


$(document).ready(function () {
    // Add active link at navbar
    $('.nav-item a').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if (location === link) {
            $(this).addClass('active');
        }
    })

    // Add to cart
    $(document).on('click', '#add-to-cart', function (e) {
        const product_id = $(this).attr('data-index')
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-url'),
            data: {
                product_id: product_id,
                quantity: $('#id_quantity').val(),
                csrfmiddlewaretoken: $('.add-to-cart-form input[name="csrfmiddlewaretoken"]').attr('data-index', product_id).val(),
                action: 'post'
            },
            success: function (json) {
                const cart_total = document.getElementById("cart-total")
                cart_total.innerHTML = json.cart_total
                if (json.cart_total > '0') {
                    cart_total.style.display = 'block'
                    console.log('block')
                } else {
                    cart_total.style.display = 'none'
                    console.log('none')
                }
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })

    // Add to wishlist
    $(document).on('click', '#to-wishlist', function (e) {
        const product_id = $(this).attr('data-index')
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-url'),
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('#to-wishlist-form input[name="csrfmiddlewaretoken"]').attr('data-index', product_id).val(),
                action: 'post'
            },
            success: function (json) {
                const wishlist_total = document.getElementById("wishlist-total")
                wishlist_total.innerHTML = json.wishlist_total

                if (json.wishlist_total > '0') {
                    wishlist_total.style.display = 'block'
                    console.log('block')
                } else {
                    wishlist_total.style.display = 'none'
                    console.log('none')
                }

                if (json.action_result === 'added') {
                    $('#to-wishlist i[data-index="' + product_id + '"]').addClass('fa-solid')
                } else {
                    $('#to-wishlist i[data-index="' + product_id + '"]').removeClass('fa-solid')
                }
            },
            error: function (xhr, errmsg, err) {
            }
        });
    })
});


//Lightbox
document.getElementById('lightbox-links').onclick = function (event) {
    event = event || window.event
    const target = event.target || event.srcElement;
    const link = target.src ? target.parentNode : target;
    const options = {index: link, event: event};
    const links = this.getElementsByTagName('a');
    blueimp.Gallery(links, options)
    const blueimp_gallery = document.getElementById('blueimp-gallery')
    blueimp_gallery.classList.add('blueimp-gallery-controls')
}