<section>

## TODO Hide navigation bars somehow else, scoped attribute wont be supported like so
<style type="text/css" scoped="scoped">
section.course-content nav {
  display: none;
}
</style>

% if description is not None:
<p>${description}</p>
% endif

<applet name="vlapplet" archive="${archive}" code="${code}" height="${height}" width="${width}">
</applet>

<form id="inputtype_${id}" class="capa_inputtype">

<fieldset>
    <input type='hidden' id='input_${id}' name='input_${id}' value=''/>
## TODO Protect score field in vlab applet
    <input type='hidden' id='input_${id}_score' name='input_${id}_score' value=''/>
</fieldset>

</form>

<script>
$(function(){
    $('.check').click(function(){
        $('#input_${id}_score').val(vlapplet.getScore());
    });
});
</script>

</section>