$(".mail-btn").on("click touchstart", function (e) {
    $(this).addClass("fly")
    that = this
    e.preventDefault();
    setTimeout(function() {
        $(that).removeClass("fly");
    }, 5400)
});