$(window).load(function () {
    window.setTimeout(function () {
        $('object').remove();
    }, 500);

    $("#form-subscriber input[name=email]").focus();
    $("#form-subscriber").submit(function (e) {
        e.preventDefault();
        var email = $(this).find('input[name=email]').val();
        var data = {
            csrfmiddlewaretoken: $(this).find('input[name=csrfmiddlewaretoken]').val(),
            email: email,
            last_name: $(this).find('input[name=last_name]').val(),
            first_name: $(this).find('input[name=first_name]').val(),
        };
        $('#form-subscriber .errorlist').slideUp();
        $('#cover').fadeIn();
        $.ajax({
            type: 'post',
            url: $(this).attr('action'),
            data: data,
            success: function (data) {
                $('#cover').fadeOut(function () {
                    if (!data.success) {
                        $('#form-subscriber').html(data.html);
                        $('#form-subscriber .errorlist').hide().slideDown();
                        $('#form-subscriber .non-field-errors').hide().slideDown();
                        if ($('#form-subscriber .non-field-errors').html()) {
                            window.location = data.redirect_url + '?s=' + data.s;
                        }
                        return;
                    }
                    $("#form-subscriber").html('<h2 style="color: #A50017">Uma mensagem foi enviada para o email ' + email + '.</h2>');
                    $("#form-subscriber").effect('highlight', 2000, function () {
                        $("#form-subscriber").effect('highlight', 2000);
                    });
                });
            }
        });
    });
});