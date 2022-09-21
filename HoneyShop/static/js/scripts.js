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