<section>

  % if "true" == attempted and msg:
    <div class="ifmo-applet-message capa_alert">${msg|n}</div>
  % endif

    <object id="usolcev_applet_${id}" type="application/x-java-applet"
            classid="java:${code}" archive="${archive}"
	        width="${width}" height="${height}" >
        <!--param name="codebase" value="./" /-->
        <param name="code" value="${code}" />
        <param name="archive" value="${archive}" />
        <param name="scriptable" value="true" />
        <param name="mayscript" value="true" />

        <param name="hash" value="${hash}" />
        <param name="meta" value="${meta}" />

        <param name="variant" value="${variant}"/>
        <param name="previousUserState" value="${user_state}" />
        <param name="attempted" value="${attempted}"/>

        % if meta == "debug":
        <param name="data_out" value="true"/>
        % endif

        <pre>Java applet failed to load</pre>
    </object>

    <form id="inputtype_${id}" class="capa_inputtype">
        <fieldset>
            <input type='hidden' id='input_${id}' name='input_${id}' value=''/>
        </fieldset>
    </form>

    <script>
    $(function(){
        $('.check').click(function(){
            $('#input_${id}').val($('#usolcev_applet_${id}')[0].getSecuredState("true"));
        });
        $('.save').click(function(){
            $('#input_${id}').val($('#usolcev_applet_${id}')[0].getSecuredState("false"));
        });
    });
    </script>

</section>
