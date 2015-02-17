##mako

<%! from django.utils.translation import ugettext as _ %>
<%namespace name='static' file='/static_content.html'/>

<%inherit file="main.html" />

<%block name="pagetitle">${_("Date checker")}</%block>

<section class="container about ifmo-content">

    <style type="text/css" scoped="scoped">
        .ifmo-content span.tab {display: inline-block; width: 30px;}
        .ifmo-content table {width: 100%}
        .ifmo-content td {border-bottom: 1px solid lightgray}
        .ifmo-content td.date-error {background-color: lightpink}
    </style>

    <h1>Date checker</h1>

    <p><strong>Course ID: </strong>${course_id}</p>
    <p><strong>Course name: </strong>${course_name}</p>

    <p>Проверка дат на соответствие <em>Воскресенье, 21:00 UTC</em>.</p>

    <hr/>

    <div>
        ${content}
    </div>

</section>