$(document).ready(function () {
    let $document = $(document);

    $document.on('click', '.bootstrap-select li.no-results', function () {
        let new_option = $(this).text().split('"')[1];
        let $select = $(this).closest('.bootstrap-select');
        $select.append('<option>'+ new_option +'</option>').selectpicker('refresh');
    });

    $document.on('click', '#save_user_book', function () {
        let $button = $(this);
        $button.prop('disabled', true);
        $button.text('Saving...');
        $button.prepend("<span class='spinner-border spinner-border-sm' role='status'></span>   ");

        let json = {
            'books': {},
            'user_books': {}
        };

        let valid = true;

        let modal_type = $("#form-rows").data('modal_type');

        let book_id = $(".modal").data("book_id");
        let user_books_id = $(".modal").data("user_books_id");

        $("#form-rows .form-group .form-control:not(div)").each(function () {
            let $form_input = $(this);
            let form_input_id = $(this).attr('id');
            let $form_group = $form_input.closest('.form-group');
            let parent_table = $form_group.data('parent_table');

            if (!$form_input[0].checkValidity()) {
                $button.empty();
                $button.removeClass('btn-success').addClass('btn-danger').text("Save");
                $button.tooltip({"title": "Please correct invalid inputs."}).tooltip('show');
                valid = false;
            }

            if ($form_input.is(':checkbox')) {
                json[parent_table][form_input_id] = $form_input.is(":checked");
            } else if($form_input.attr('type') !== 'search') {
                json[parent_table][form_input_id] = $form_input.val();
            }
        });

        if (valid) {
            let method = modal_type === 'edit' ? 'PUT' : 'POST';

            $.ajax({
                url: '/books/' + (modal_type === 'edit' ? book_id : ''),
                method: method,
                data: JSON.stringify(json['books']),
                success: function(data){
                    let response = JSON.parse(data);
                    json['user_books']['book_id'] = response['id'];
                    $.ajax({
                        url: '/user_books/' + (modal_type=='edit' ? user_books_id : ''),
                        method: method,
                        data: JSON.stringify(json['user_books']),
                        success: function(data){
                            $button.empty();
                            $button.text("Success");
                            $(".modal").modal('hide');
                            // TODO: Update row if PUT, add row if POST
                        }
                    })
                }
            });
        } else {
            return false;
        }

    });

    $document.on('click', '#delete_user_book', function(){
        let $button = $(this);
        let user_book_id = $('.modal').data('user_books_id');
        $button.prop('disabled', true);
        $button.text('Deleting...');
        $button.prepend("<span class='spinner-border spinner-border-sm' role='status'></span>   ");
        $.ajax({
            url: "/user_books/" + user_book_id,
            method: 'DELETE',
            success: function(data){
                let response = JSON.parse(data);
                if (response['success']){
                    $button.empty();
                    $button.text("Success");
                    $(".modal").modal('hide');
                    // TODO: Remove row from table
                }
            }
        })
    });

    $document.on('change', '#form-rows .form-group .form-control', function () {
        if ($("#save_user_book").hasClass('btn-danger')) {
            $("#save_user_book").removeClass('btn-danger').addClass('btn-success').tooltip('dispose').prop('disabled', false);
        }
    });
});