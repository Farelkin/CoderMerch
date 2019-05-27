let g_urls = {
    'login': location.origin + '/api/v1/login/',
    'logout': location.origin + '/api/v1/logout/',
};
let g_auth = localStorage.getItem("auth");
if (g_auth == null) {
    g_auth = sessionStorage.getItem("auth");
}

if (g_auth) {
    try {
        g_auth = JSON.parse(g_auth);
    } catch (error) {
        g_auth = null;
    }
}
let getCookie = function (name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
let g_csrftoken = getCookie('csrftoken');
let initLogin = function () {
    if (g_auth) {
        $('#non-logged-in').hide();
        $('#logged-in').show();
        if (g_auth.remember_me) {
            localStorage.setItem("auth", JSON.stringify(g_auth));
        } else {
            sessionStorage.setItem("auth", JSON.stringify(g_auth));
        }
    } else {
        $('#non-logged-in').show();
        $('#logged-in').hide();
        localStorage.removeItem("auth");
        sessionStorage.removeItem("auth");
    }
};
$(function () {
    initLogin();

    $('#loginOkButton').click(function () {
        let email = $('#defaultForm-email').val();
        let password = $('#defaultForm-pass').val();
        let remember_me = $('#input-local-storage').prop('checked');
        if (email && password) {
            $('#modal-error').addClass('invisible');
            $.ajax({
                url: g_urls.login,
                method: "POST",
                data: {
                    email: email,
                    password: password,
                    csrfmiddlewaretoken: g_csrftoken
                }
            }).done(function (data) {
                g_auth = {
                    email: email,
                    key: data.key,
                    remember_me: remember_me
                };
                $('.close').click();
                initLogin();
                g_csrftoken = getCookie('csrftoken');
            }).fail(function () {
                $('#modal-error').removeClass('invisible');
            });
        } else {
            $('#modal-error').removeClass('invisible');
        }
    });
    $('#logged-in').click(function () {
        $.ajax({
            url: g_urls.logout,
            method: "POST",
            beforeSend: function (request) {
                request.setRequestHeader("Authorization", "Token " + g_auth.key);
            },
            data: {
                csrfmiddlewaretoken: g_csrftoken
            }
        }).done(function () {
            g_auth = null;
            initLogin();
        }).fail(function () {
            console.log("FAIL");
        });
    });

});