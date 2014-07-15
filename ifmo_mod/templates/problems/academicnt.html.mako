<section>

<style type="text/css">
.action input[type="button"].save {
  position: absolute;
  left: -1000px;
}
button.start_lab {
  float: left;
  margin-right: 10px;
  height: 40px;
  margin-top: 1px;
}
</style>

<script>
var testWindow = undefined;

function openTestWindow() {
  testWindow = window.open('/external/ant/${courseid}/${unitid}/${ssoid}', 'windowDLC_TEST','height=520,width=740,modal=no,fullscreen=0,status=1,location=1,scrollbars=1', true);
  testWindow.focus();
}
</script>

<fieldset>
    <input type='hidden' id='input_${id}_course' name='input_${id}_course' value='${courseid}'/>
</fieldset>

<button class="start_lab" onclick="openTestWindow()">Start</button>

</section>