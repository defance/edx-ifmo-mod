## mako
<section>

    <style type="text/css">
        input[type="button"].start_lab {
          float: left;
          margin-right: 5px;
          height: 40px;
          /*margin-top: 1px;*/
        }
    </style>

    <%
        html_academy_link = "http://htmlacademy.ru/{course_name}/{course_element}".format(
            course_name=course_name,
            course_element=course_element
        )
    %>
    <div class="action">
        <input type="button" class="start_lab" onclick="javascript:window.location='${html_academy_link}'" value="Start" />
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