## mako

<%!
    from django.core.urlresolvers import reverse
%>

<section>

    <style type="text/css">
    input[type="button"].start_lab {
      float: left;
      margin-right: 5px;
      height: 40px;
      margin-top: 20px;
    }
    </style>

    <script>
    var testWindow = undefined;

    <%
        ant_link = reverse('ant_external', kwargs={
            'course': courseid,
            'unit': unitid,
            'ssoid': ssoid
        })
    %>

    function openTestWindow() {
      testWindow = window.open('${ant_link}', 'windowDLC_TEST','height=600,width=800,modal=no,fullscreen=0,status=1,location=1,scrollbars=1', true);
      testWindow.focus();
    }
    </script>

    <fieldset>
        <input type='hidden' id='input_${id}_course' name='input_${id}_course' value='${courseid}'/>
    </fieldset>

    <div class="action">
        <input type="button" class="start_lab" onclick="openTestWindow()" value="Start" />
    </div>

</section>