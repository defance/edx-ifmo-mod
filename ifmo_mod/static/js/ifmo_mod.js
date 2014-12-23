var Summary = {

    render_course_table: function(data) {
        if (data.courses && data.courses.length) {
            $('#summary-content').html(_.template($('#summary-template-table').text())(data));
        }
    },

    get_data: function() {
        $.ajax({
            url: '/summary_handler',
            success: function(data) { Summary.render_course_table(data); }
        })
    }

};

$(function() {
    // Initialize date fields
    $("#summary-date-picker-from").datepicker({"dateFormat": "dd/mm/yy"}).mask("99/99/9999");
    $("#summary-date-picker-to").datepicker({"dateFormat": "dd/mm/yy"}).mask("99/99/9999");

    // Render template
    Summary.get_data();
});