<section>

    <object name="vlapplet" classid="java:${code}" type="application/x-java-applet" archive="${archive}"
            height="${height}" width="${width}" >
        <param name="archive" value="${archive}" />
    </object>

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