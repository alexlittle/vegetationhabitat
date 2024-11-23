const data = document.currentScript.dataset;
const autoCompleteURL = data.speciesacurl;



$(document).ready(function () {
    // Select all input fields ending with '-species'
    const $inputs = $('input[name$="-species"]');

    $inputs.each(function () {
        const $input = $(this); // Current input field
        const $resultsContainer = $('<div class="autocomplete-results"></div>'); // Create a results container dynamically
        $input.after($resultsContainer); // Place it after the input field

        $input.on('input', function () {
            const query = $input.val();

            if (query.length >= 3) {
                console.log(autoCompleteURL); // For debugging: log the URL

                // Send AJAX request
                $.ajax({
                    url: autoCompleteURL,
                    data: { q: query },
                    success: function (data) {

                        console.log(data);
                        if (Array.isArray(data) && data.length > 0) {
                            $resultsContainer.empty().show();
                            data.forEach(function(item) {
                                $resultsContainer.append('<div class="autocomplete-suggestion">' + item + '</div>');
                            });
                            $('.autocomplete-suggestion').on('click', function() {
                                $input.val($(this).text());
                                $resultsContainer.empty().hide();
                            });
                        } else {
                            $resultsContainer.empty().hide();
                        }

                    },
                    error: function () {
                        console.error('Error fetching autocomplete data');
                    }
                });
            } else {
                // Clear results if query is too short
                $resultsContainer.empty();
            }
        });

        // Hide results when clicking outside
        $(document).on('click', function (e) {
            if (!$input.is(e.target) && !$resultsContainer.is(e.target) && $resultsContainer.has(e.target).length === 0) {
                $resultsContainer.empty();
            }
        });
    });
});