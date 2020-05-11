$(document).ready(function () {
    let $document = $(document);
    feather.replace();

    //START ADD LISTENERS REGION
    $document.on('hide.bs.modal', function () {
        $(".modal").remove();
    });

    $document.on("click", '.user_book_row', function () {
        let $row = $(this);
        let $table = $(this).closest('table');
        let user_books_id = $row.data('user_books_id');
        let book_id = $row.data('book_id');

        if (!$table.hasClass('loading')) {
            $table.addClass('loading').removeClass('table-hover');
            // Grab the modal
            $.get("/modal/user_books/edit/" + user_books_id, function (data) {
                $('body').append(data);

                // For each of the selects, we need to initialize them as selectpickers and then reset the value that existed before we did the reset
                $(".modal select").each(function (i) {
                    let $select = $(this);
                    let select_val = $select.val();c
                    $select.selectpicker({
                        noneResultsText: 'Click here to add!'
                    });
                    $select.val(select_val);
                });

                $(".modal").modal('show');

                // Set data attr on the modal.
                $(".modal").data('user_books_id', user_books_id);
                $(".modal").data('book_id', book_id);

                feather.replace();
                $table.removeClass('loading').addClass('table-hover');
            });
        }
    });

    $document.on('click', '#add_user_book', function () {
        // Load modal
        $.get("/modal/user_books/create/", function (data) {
            $('body').append(data);

            //for each of the selects, we need to initialize them as selectpickers.
            $(".modal select").each(function (i) {
                $(this).val('').selectpicker({
                    // Change text to be more descriptive for what we need.
                    noneResultsText: 'Click here to add!'
                });
            });

            $(".modal").modal('show');

            feather.replace();
        });
    });

    $document.on('click', '#share_email', function () {
        let email_to_send = $("#share_email_input").val();
        // Send e-mail
        $.get("/user_books/share_user_books/" + email_to_send, function (data) {

        });
    });
    //END ADD LISTENERS REGION
});