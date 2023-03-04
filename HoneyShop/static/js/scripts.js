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
    $(document).on('click', '.add-to-cart button', function (e) {
        const product_id = $(this).parent().attr('data-index')
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).parent().attr('data-url'),
            data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('form.add-to-cart[data-index="' + product_id + '"] input[name="csrfmiddlewaretoken"]').val(),
                action: 'post'
            },
            success: function (json) {
                const add_to_cart_button = $('form.add-to-cart[data-index="' + product_id + '"] button')
                const to_cart_link = $('form.add-to-cart[data-index="' + product_id + '"] a')
                add_to_cart_button.addClass('d-none')
                to_cart_link.removeClass('d-none')

                const cart_total = document.getElementById("cart-total")
                cart_total.innerHTML = json.cart_total
                if (json.cart_total > '0') {
                    cart_total.style.display = 'block'
                } else {
                    cart_total.style.display = 'none'
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
            type: 'POST', url: $(this).attr('data-url'), data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('#to-wishlist-form input[name="csrfmiddlewaretoken"]').attr('data-index', product_id).val(),
                action: 'post'
            }, success: function (json) {
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
            }, error: function (xhr, errmsg, err) {
            }
        });
    })

    // Click like at post comment
    $(document).on('click', '#like', function (e) {
        const comment_id = $(this).attr('data-index')
        e.preventDefault();
        $.ajax({
            type: 'POST', url: $(this).attr('data-url'), data: {
                comment_id: comment_id,
                csrfmiddlewaretoken: $('#like-form input[name="csrfmiddlewaretoken"]').attr('data-index', comment_id).val(),
                action: 'post'
            }, success: function (json) {
                const like_total = document.getElementById("like-total-" + comment_id)
                like_total.innerText = json.like_total

                if (json.like_total > '0') {
                    like_total.style.display = 'inline-block'
                } else {
                    like_total.style.display = 'none'
                }

                if (json.action_result === 'added') {
                    $('#like i[data-index="' + comment_id + '"]').addClass('fa-solid')
                } else {
                    $('#like i[data-index="' + comment_id + '"]').removeClass('fa-solid')
                }
            }, error: function (xhr, errmsg, err) {
            }
        });
    })

    // Increase the quantity of product in the cart
    $(document).on('click', '.plus', function (e) {
        const minus = $(this).parent().find('button.minus')
        const plus = $(this)
        const product_id = plus.parent().parent().attr('data-index')
        const input = $('form.update_quantity[data-index="' + product_id + '"] .quantity input')
        const new_quantuty = parseInt(input.val()) + 1
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).parent().parent().attr('data-url'),
            data: {
                quantity: new_quantuty,
                csrfmiddlewaretoken: $('form.update_quantity[data-index="' + product_id + '"] input[name="csrfmiddlewaretoken"]').val(),
                action: 'post'
            },
            success: function (json) {
                const diff = json.available_quantity - new_quantuty
                if (diff >= 0) {
                    input.val(new_quantuty);
                    input.change();
                    const product_total_price = $('#product-total-price[data-index="' + product_id + '"]')
                    product_total_price[0].innerHTML = json.product_total_price
                    const total_price = document.getElementById("total-price")
                    total_price.innerHTML = json.total_price
                    const cart_total = document.getElementById("cart-total")
                    cart_total.innerHTML = json.cart_total
                }
                if (diff <= 0) {
                    plus.addClass('no-active')
                }
                if (diff > 0) {
                    plus.removeClass('no-active')
                }
                if (new_quantuty >= 2) {
                    minus.removeClass('no-active')
                }
            },
            error: function (xhr, errmsg, err) {
            }
        });
        return false;
    })

    // Reduce the quantity of product in the cart
    $(document).on('click', '.minus', function (e) {
        const minus = $(this)
        const plus = $(this).parent().find('button.plus')
        const product_id = $(this).parent().parent().attr('data-index')
        const input = $('form.update_quantity[data-index="' + product_id + '"] .quantity input')

        let new_quantuty = parseInt(input.val()) - 1;
        new_quantuty = new_quantuty < 1 ? 1 : new_quantuty;

        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: $(this).parent().parent().attr('data-url'),
            data: {
                quantity: new_quantuty,
                csrfmiddlewaretoken: $('form.update_quantity[data-index="' + product_id + '"] input[name="csrfmiddlewaretoken"]').val(),
                action: 'post'
            },
            success: function (json) {
                const diff = json.available_quantity - new_quantuty
                if (diff > 0) {
                    input.val(new_quantuty);
                    input.change();
                    plus.removeClass('no-active')
                    const product_total_price = $('#product-total-price[data-index="' + product_id + '"]')
                    product_total_price[0].innerHTML = json.product_total_price
                    const total_price = document.getElementById("total-price")
                    total_price.innerHTML = json.total_price
                    const cart_total = document.getElementById("cart-total")
                    cart_total.innerHTML = json.cart_total
                }
                if (new_quantuty === 1) {
                    minus.addClass('no-active')
                }
            },
            error: function (xhr, errmsg, err) {
            }
        });
        return false;
    })
})

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
})

function addReply(user, comment_id) {
    document.getElementById("contactparent").value = comment_id;
    const comment_form = document.getElementById("contactcomment")
    comment_form.innerText = `${user}, `;
    const end = comment_form.value.length;
    comment_form.setSelectionRange(end, end);
    comment_form.focus()
}

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