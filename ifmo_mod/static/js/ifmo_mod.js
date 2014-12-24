var Summary =
{

    latest_id: 0,

    render_course_table: function(data)
    {
        if (data.courses && data.courses.length) {
            $('#summary-content').html(_.template($('#summary-template-table').text())(data));
        }
    },

    add_filter_date: function()
    {
        this.latest_id += 1;
        $('.summary-filters-controls').before(
                _.template($('#summary-template-date-field').text())({'id': this.latest_id})
        );
        $('#summary-date-picker-'+this.latest_id)
                .datepicker({"dateFormat": "dd/mm/yy"})
                .mask("99/99/9999")
                .val(this.current_date());
    },

    remove_filter_date: function()
    {
        if (1 == this.latest_id) {
            return;
        }
        $('.summary-filters-item-' + this.latest_id).remove();
        this.latest_id -= 1;
    },

    current_date: function()
    {
        var d = new Date();
        return d.getDate() + '/' + (d.getMonth()+1) + '/' + d.getFullYear();
    },

    reset_view: function()
    {
        $('#summary-content').html(_.template($('#summary-template-loading').text())());
    },

    filter_data: function()
    {
        this.reset_view();
        var dates = [];
        $('.summary-date-picker').each(function(e){
            dates.push(this.value);
        });
        $.ajax({
            url: '/summary_handler',
            dataType: 'json',
            data: {'dates': dates},
            success: function(data) { Summary.render_course_table(data); }
        });
    }

};

$(function() {

    $('#summary-button-add').click(function(e) {Summary.add_filter_date()});
    $('#summary-button-remove').click(function(e) {Summary.remove_filter_date()});
    $('#summary-button-filter').click(function(e) {Summary.filter_data()});

    Summary.add_filter_date();
    Summary.filter_data();
});