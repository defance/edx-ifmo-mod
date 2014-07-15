<section>

## TODO Hide navigation bars somehow else, scoped attribute wont be supported like so
<style type="text/css" scoped="scoped">
section.course-content nav {
  display: none;
}
</style>

<div>
% if description is not None:
    <p>${description}</p>
% endif
    <p>Go to <a href="http://htmlacademy.ru/${course_name}/${course_element}" target="_blank">HTML Academy</a></p>
</div>

<form id="inputtype_${id}" class="capa_inputtype">

<fieldset>
    <input type='hidden' id='input_${id}' name='input_${id}' value=''/>
    <input type='hidden' id='input_${id}_user' name='input_${id}_user' value='${userid}'/>
</fieldset>

</form>

<script>
$(function(){
    if(location.hash === '#problem_check') {
        setTimeout(function(){$('.check').trigger('click');}, 10);
        window.location.hash = '';
    }
});
</script>

</section>