## mako

<section>

  % if msg:
    <div class="ifmo-applet-message capa_alert">${msg|n}</div>
  % endif

    <style type="text/css">
        input[type="button"].start_lab {
          float: left;
          margin-right: 5px;
          height: 40px;
        }
    </style>

    <script>
    $(function(){
        if(location.hash === '#problem_check') {
            setTimeout(function(){$('.check').trigger('click');}, 10);
            window.location.hash = '';
        }
    });
    </script>

    <form id="inputtype_${id}" class="capa_inputtype">
        <fieldset>
            <input type='hidden' id='input_${id}_name' name='input_${id}_name' value='${name}'/>
            <input type='hidden' id='input_${id}_shortname' name='input_${id}_shortname' value='${shortname}'/>
            <input type='hidden' id='input_${id}_element' name='input_${id}_element' value='${element}'/>
            <input type='hidden' id='input_${id}_user' name='input_${id}_user' value='${userid}'/>
        </fieldset>
    </form>

    <%
        html_academy_link = "https://htmlacademy.ru/{name}/{element}".format(
            name=name,
            element=element
        )
    %>
    <div class="action">
        <input type="button" class="start_lab" onclick="javascript:window.location='${html_academy_link}'" value="Start" />
    </div>

</section>
