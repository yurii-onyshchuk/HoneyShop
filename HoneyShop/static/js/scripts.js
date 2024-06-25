$(document).ready(function () {

    // Add active link at navbar
    $('.nav-item a').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if (location === link) {
            $(this).addClass('active');
        }
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

    // Add the product to wishlist
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

    // Add the product to cart
    $(document).on('click', '.add-to-cart button', function (e) {
        const product_id = $(this).parent().attr('data-index')
        e.preventDefault();
        $.ajax({
            type: 'POST', url: $(this).parent().attr('data-url'), data: {
                product_id: product_id,
                csrfmiddlewaretoken: $('form.add-to-cart[data-index="' + product_id + '"] input[name="csrfmiddlewaretoken"]').val(),
                action: 'post'
            }, success: function (json) {
                const add_to_cart_button = $('form.add-to-cart[data-index="' + product_id + '"] button')
                const to_cart_link = $('form.add-to-cart[data-index="' + product_id + '"] a')
                add_to_cart_button.addClass('d-none')
                to_cart_link.removeClass('d-none')

                const cart_total_quantity = document.getElementById("cart-total")
                cart_total_quantity.innerHTML = json.cart_total_quantity
                if (json.cart_total_quantity > '0') {
                    cart_total_quantity.style.display = 'block'
                } else {
                    cart_total_quantity.style.display = 'none'
                }
            }, error: function (xhr, errmsg, err) {
            }
        });
    })

    // Increase the quantity of product in the cart
    $(document).on('click', '.plus', function (e) {
        e.preventDefault();
        if (!($(this).hasClass('no-active'))) {
            const product_id = $(this).parent().parent().attr('data-index')
            const input = $('form.update_quantity[data-index="' + product_id + '"] .quantity input')
            const new_input_quantity = parseInt(input.val() || 0) + 1
            ajax_handler(e, input, product_id, new_input_quantity)
            return false;
        }
    })

    // Reduce the quantity of product in the cart
    $(document).on('click', '.minus', function (e) {
        e.preventDefault();
        if (!($(this).hasClass('no-active'))) {
            const product_id = $(this).parent().parent().attr('data-index')
            const input = $('form.update_quantity[data-index="' + product_id + '"] .quantity input')
            let new_input_quantity = parseInt(input.val() || 2) - 1;
            new_input_quantity = new_input_quantity < 1 ? 1 : new_input_quantity;
            ajax_handler(e, input, product_id, new_input_quantity)
            return false;
        }
    })

    // Change the quantity of product in the cart by "focusout"
    $(document).on('focusout', 'form.update_quantity input', function (e) {
        const product_id = $(this).parent().parent().attr('data-index')
        const input = $('form.update_quantity[data-index="' + product_id + '"] .quantity input')
        let new_input_quantity = parseInt(input.val() || 1)
        ajax_handler(e, input, product_id, new_input_quantity)
        return false;
    })

    // Change the quantity of product in the cart by "Enter" key
    $('form.update_quantity').keydown(function (e) {
        if (e.keyCode === 13) {
            const product_id = $(this).attr('data-index')
            const input = $('form.update_quantity[data-index="' + product_id + '"] .quantity input')
            input.focusout()
            input.blur()
            return false;
        }
    })

    // AJAX handler for changing the quantity of product in the cart
    function ajax_handler(e, input, product_id, new_input_quantity) {
        $.ajax({
            type: 'POST', url: input.parent().parent().attr('data-url'), data: {
                input_quantity: new_input_quantity,
                csrfmiddlewaretoken: $('form.update_quantity[data-index="' + product_id + '"] input[name="csrfmiddlewaretoken"]').val(),
                action: 'post'
            }, success: function (json) {
                const diff = json.available_product_quantity - json.product_quantity
                if (diff >= 0) {
                    input.val(json.product_quantity);
                    change_active_status(input, diff)
                    const product_total_price = $('#product-total-price[data-index="' + product_id + '"]')
                    product_total_price[0].innerHTML = json.product_total_price
                    const cart_total_price = document.getElementById("total-price")
                    cart_total_price.innerHTML = json.cart_total_price
                    const cart_total_quantity = document.getElementById("cart-total")
                    cart_total_quantity.innerHTML = json.cart_total_quantity
                }
            }, error: function (xhr, errmsg, err) {
            }
        });
        return false;
    }

    // Change active status of "+/-" buttons in the cart
    function change_active_status(input, diff) {
        const minus = input.parent().find('button.minus')
        const plus = input.parent().find('button.plus')
        if (diff <= 0) {
            plus.addClass('no-active')
        }
        if (diff > 0) {
            plus.removeClass('no-active')
        }
        if (parseInt(input.val()) === 1) {
            minus.addClass('no-active')
        }
        if (parseInt(input.val()) >= 2) {
            minus.removeClass('no-active')
        }
    }

    // Change delivery options on the Checkout page
    let deliveryOption = $('.checkout #id_delivery_option');
    adjustFieldsVisibility();
    deliveryOption.change(function () {
        adjustFieldsVisibility();
    });

    function adjustFieldsVisibility() {
        let selectedOption = deliveryOption.val();
        $('.checkout #div_id_city, .checkout #div_id_street, .checkout #div_id_house, ' + '.checkout #div_id_flat, .checkout #div_id_delivery_service_department').hide();
        if (selectedOption === '1') {
        } else if (selectedOption === '2' || selectedOption === '3') {
            $('.checkout #div_id_city, .checkout #div_id_delivery_service_department').show();
        } else if (selectedOption === '4') {
            $('.checkout #div_id_city, .checkout #div_id_street, ' + '.checkout #div_id_house, .checkout #div_id_flat').show();
        }
    }
})


// Add replay at comment
function addReply(user, comment_id) {
    document.getElementById("contactparent").value = comment_id;
    const comment_form = document.getElementById("contactcomment")
    comment_form.innerText = `${user}, `;
    const end = comment_form.value.length;
    comment_form.setSelectionRange(end, end);
    comment_form.focus()
}

$(document).ready(function () {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    // City choose
    $('#id_city').on('input', function () {
        let query = $(this).val();
        if (query.length >= 2) {
            $.ajax({
                url: '/checkout/city_autocomplete/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({query: query}),
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (data) {
                    $('#city-results').empty().show();
                    if (data.success) {
                        $.each(data.data[0].Addresses, function (index, address) {
                            $('#city-results').append(`<li class="dropdown-item" data-city-ref="${address.DeliveryCity}">${address.Present}</li>`);
                        });
                    }
                }
            });
        }
    });
    $('#city-results').on('click', 'li', function () {
        $('#id_city').val($(this).text())
            .attr('value', $(this).text())
            .attr('data-city-ref', $(this).attr('data-city-ref'));
        $('#city-results').hide();
    });

    $(document).click(function (event) {
        if (!$(event.target).closest('#id_city, #city-results').length) {
            $('#city-results').hide();
        }
    });


    // Delivery service department choose
    $('#id_delivery_service_department').on('input', function () {
        let query = $(this).val();
        let city_id = $('#id_city').attr('data-city-ref');
        if (query.length >= 1) {
            $.ajax({
                url: '/checkout/department_autocomplete/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({query: query, city_id: city_id}),
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function (data) {
                    $('#department-results').empty().show();
                    if (data.success) {
                        $.each(data.data, function (index, warehouse) {
                            $('#department-results').append(`<li class="dropdown-item">${warehouse.Description}</li>`);
                        });
                    }
                }
            });
        }
    });
    $('#department-results').on('click', 'li', function () {
        $('#id_delivery_service_department').val($(this).text());
        $('#department-results').hide();
    });

    $(document).click(function (event) {
        if (!$(event.target).closest('#id_delivery_service_department, #department-results').length) {
            $('#department-results').hide();
        }
    });
});