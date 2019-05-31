$(document).ready(function () {

        function get_result(q) {
            $.getJSON(location.origin + '/api/v1/products/?search=' + q)
                .done(function (data) {
                    $('#search-result').empty();
                    $.each(data.results, function (i, item) {
                        $('#search-result').append('<a href="' + item.url.replace('/api/v1/', '/') + '">' + item.name_product + '</a>');
                        // Количество элементов в выдаче -1
                        if (i === 1) {
                            return false;
                        }
                    });
                });
        }

        $('#search-input').on('keyup',function () {
            if ($(this).val().length > 2) {
                get_result($(this).val());
            }
        });
    }
);