$(document).ready(function () {
    $('#add-form').click(function () {
        // Select the formset container and the management form's TOTAL_FORMS input
        var container = $('#formset-container');
        var totalFormsInput = $('[name$="TOTAL_FORMS"]');
        var totalForms = parseInt(totalFormsInput.val(), 10);

        // Clone the last form
        var newForm = container.find('.formset-form').last().clone();

        // Update input attributes in the cloned form
        newForm.find(':input').each(function () {
            var name = $(this).attr('name');
            var id = $(this).attr('id');

            if (name) {
                $(this).attr('name', name.replace(/\d+/, totalForms));
            }
            if (id) {
                $(this).attr('id', id.replace(/\d+/, totalForms));
            }

            // Clear the value of the cloned input fields
            $(this).val('');
        });

        // Append the new form to the container
        container.append(newForm);

        // Increment the TOTAL_FORMS count
        totalFormsInput.val(totalForms + 1);
    });
});