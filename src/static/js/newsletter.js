

$(window).ready(function () {
    $("#form-subscriber").submit(function (e) {
        newsletterSubmit(this, e);
    });
    $("#form-subscriber button").removeAttr('disabled');
});


function newsletterSubmit(o, e) {
    e.preventDefault();
    var email = $(o).find('input[name=email]').val();
    var data = {
        csrfmiddlewaretoken: $(o).find('input[name=csrfmiddlewaretoken]').val(),
        email: email,
        last_name: $(o).find('input[name=last_name]').val(),
        first_name: $(o).find('input[name=first_name]').val(),
    };
    $('#form-subscriber .errorlist').slideUp();
    $('#cover').fadeIn();
    $.ajax({
        type: 'post',
        url: $(o).attr('action'),
        data: data,
        success: function (data) {
            $('#cover').fadeOut(function () {
                if (!data.success) {
                    $('#form-subscriber').html(data.html);
                    $('#form-subscriber .errorlist').hide().slideDown();
                    $('#form-subscriber .non-field-errors').hide().slideDown();
                    $("#form-subscriber button").removeAttr('disabled');
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
                    msg = 'Tá quase lá! Uma mensagem foi enviada para o email ' + email + '. Clique nela para ter acesso ao livro do au au.<br><br> Caso não tenha recebido, verifique sua pasta spam ou sua pasta de promoções (do gmail) - emails podem ir para lugares estranhos...';
                }
                $("#content").html('<h2 style="color: #A50017">' + msg + '.</h2>').css('padding', '5px');
                $("#content").effect('highlight', 2000, function () {
                    $("#content").effect('highlight', 2000);
                });
            });
        }
    });
}