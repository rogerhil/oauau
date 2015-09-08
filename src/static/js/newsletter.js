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
                    return;
                }
                var msg;
                if (data.s) {
                    var url = data.success_url + '?s=' + data.s;
                    if (data.subs) {
                        url += "&subs=1";
                    }
                    window.location = url;
                    msg = 'Redirecionando';
                } else {
                    msg = 'Uma mensagem foi enviada para o email ' + email;
                }
                $("#form-subscriber").html('<h2 style="color: #A50017">' + msg + '.</h2>').css('padding', '5px');
                $("#form-subscriber").effect('highlight', 2000, function () {
                    $("#form-subscriber").effect('highlight', 2000);
                });
            });
        }
    });
});
