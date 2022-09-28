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

// Add active link at navbar
$(document).ready(function () {
    $('.nav-item a').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        let link = this.href;
        if (location === link) {
            $(this).addClass('active');
        }
    })
});

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