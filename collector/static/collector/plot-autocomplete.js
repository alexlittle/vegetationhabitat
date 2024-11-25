const data = document.currentScript.dataset;
const autoCompleteURL = data.plotacurl;

$(document).ready(function () {
    const $plotField = $('#id_plot-plot');
    const $suggestions = $('#suggestions');
    const $properties = $('#properties');

    // Fetch autocomplete suggestions
    $plotField.on('input', function () {
        const query = $plotField.val().trim();

        if (query.length < 2) {
            $suggestions.hide();
            return;
        }
        if (query.length >= 2) {
            $.ajax({
                url: autoCompleteURL,
                data: { q: query },
                method: 'GET',
                success: function (data) {
                    // Clear previous suggestions
                    $suggestions.empty();
                    $properties.empty();

                    if (data.length > 0) {
                        $suggestions.show();
                        data.forEach(item => {
                            const $li = $('<li></li>')
                                .text(item.code)
                                .css({ cursor: 'pointer', padding: '5px' })
                                .on('click', function () {
                                    // Update plot field with selected code
                                    $plotField.val(item.code);
                                    $suggestions.hide();
                                    showProperties(item.properties);
                                });

                            $suggestions.append($li);
                        });
                    } else {
                        $suggestions.hide();
                    }
                },
                error: function (xhr, status, error) {
                    console.error('Error fetching autocomplete data:', error);
                }
            });
        }
    });

    // Hide suggestions when clicking outside
    $(document).on('click', function (event) {
        if (!$suggestions.is(event.target) && !$suggestions.has(event.target).length && !$plotField.is(event.target)) {
            $suggestions.hide();
        }
    });

    // Show selected item's properties
    function showProperties(properties) {
        $properties.empty();
        //$properties.empty().append('<p>Properties:</p>');
        const $ul = $('<ul></ul>');
        properties.forEach(property => {
            const $li = $('<li></li>').text(`${property.name}: ${property.value}`);
            $ul.append($li);
        });
        $properties.append($ul);
    }
});