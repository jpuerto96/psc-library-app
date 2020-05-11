$(document).ready(function () {
    let $document = $(document);

    // START ADD LISTENERS REGION
    $document.on('click', 'li.no-results', function () {
        let $this = $(this);
        // Grab parent bootstrap-select container.
        let $bootstrap_select = $this.closest('.bootstrap-select');
        // Get the searchbox value
        let val = $bootstrap_select.find('.bs-searchbox>input').val();
        // Add searchbox value to select and select that updated value
        $bootstrap_select.find('select').append('<option class="new_option" value="' + val + '">' + val + '</option>').selectpicker('refresh').selectpicker('val', val);
    });

    $document.off('click', '#save_user_book').on('click', '#save_user_book', function () {
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

        let user_books_id = $(".modal").data("user_books_id");

        // Iterate over form options and check validity.
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
            } else if ($form_input.attr('type') !== 'search') {
                json[parent_table][form_input_id] = $form_input.val();
            }
        });

        if (valid) {
            // POST a new book. We know that we will get book data in response.
            $.ajax({
                url: '/books/',
                method: "POST",
                data: JSON.stringify(json['books']),
                success: function (data) {
                    let book_response = JSON.parse(data);
                    // Update user_books json with the id from the book POST request.
                    json['user_books']['book_id'] = book_response['id'];
                    let method = modal_type === 'edit' ? 'PUT' : 'POST';
                    $.ajax({
                        url: '/user_books/' + (modal_type == 'edit' ? user_books_id : ''),
                        method: method,
                        data: JSON.stringify(json['user_books']),
                        success: function (data) {
                            let user_books_response = JSON.parse(data);

                            // If something failed, display the failure message
                            if (user_books_response['message'] !== undefined) {
                                $button.prop('disabled', false);
                                $button.empty();
                                $button.removeClass('btn-success').addClass('btn-danger').text("Save");
                                $button.tooltip({"title": user_books_response['message']}).tooltip('show');
                                return;
                            }

                            // Otherwise, set success and hide modal.
                            $button.empty();
                            $button.text("Success");
                            $(".modal").modal('hide');
                            if (method === "PUT") {
                                // Update the row with this user_books_id with the updated book/user_books data
                                update_row($(".user_book_row[data-user_books_id='" + user_books_id + "']"),
                                    user_books_response, book_response);
                            } else {
                                // Add a new row with the book/user_books data
                                add_new_row(user_books_response, book_response);
                            }
                        }
                    })
                }
            });
        } else {
            return false;
        }

    });

    $document.off('click', '#delete_user_book').on('click', '#delete_user_book', function () {
        let $button = $(this);
        let user_book_id = $('.modal').data('user_books_id');
        $button.prop('disabled', true);
        $button.text('Deleting...');
        $button.prepend("<span class='spinner-border spinner-border-sm' role='status'></span>   ");
        $.ajax({
            url: "/user_books/" + user_book_id,
            method: 'DELETE',
            success: function (data) {
                let response = JSON.parse(data);
                if (response['success']) {
                    $button.empty();
                    $button.text("Success");
                    $(".modal").modal('hide');
                    // Delete the row from the list.
                    $(".user_book_row[data-user_books_id='" + user_book_id + "']").fadeOut(300, function () {
                        $(this).remove();
                    })
                }
            }
        })
    });

    $document.on('change', '#form-rows .form-group .form-control', function () {
        // If there were any changes, reset the save button.
        if ($("#save_user_book").hasClass('btn-danger')) {
            $("#save_user_book").removeClass('btn-danger').addClass('btn-success').tooltip('dispose').prop('disabled', false);
        }
    });
    // END ADD LISTENERS REGION
});

// START UTILITY FUNCTION REGION
function add_new_row(user_books_data, books_data) {
    // Get the table and template row
    let $table = $("#user_book_list");
    let $new_tr = $table.find('.template_user_book_row').clone();

    // Remove the template class and add the regular row class so that the listeners can be acknowledged.
    $new_tr.removeClass('template_user_book_row').addClass('user_book_row');

    // Update this row with the appropriate data.
    update_row($new_tr, user_books_data, books_data);

    // Add this row to the list and show it.
    $table.find("tbody").append($new_tr);
    $new_tr.show('slow');
}

function update_row($tr, user_books_data, books_data) {
    // Update the data attributes with updated ids.
    $tr.attr('data-user_books_id', user_books_data['id']).attr('data-book_id', books_data['id']);

    // Iterate over data
    for (let key in user_books_data) {
        // Find table cell with class == to the key
        let $td = $tr.find("." + key);
        if ($td.length > 0) {
            // Special case for the checkbox.
            if (key == 'is_favorite') {
                let $input = $td.find('input');
                $input.prop('checked', user_books_data[key]);
            } else {
                $td.text(user_books_data[key]);
            }
        }
    }
    for (let key in books_data) {
        let $td = $tr.find("." + key);
        if ($td.length > 0)
            $td.text(books_data[key]);
    }

    return $tr;
}
// END UTILITY FUNCTION REGION
