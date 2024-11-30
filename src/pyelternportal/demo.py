"""Constants for demo (html and json)"""

from datetime import date, datetime, timedelta

DEMO_TODAY = date.today().strftime("%d.%m.%Y")
DEMO_TOMORROW = (date.today() + timedelta(days=1)).strftime(
    "%d.%m.%Y"
)
DEMO_NOW6 = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
DEMO_NOW5 = datetime.now().strftime("%d.%m.%Y %H:%M")
DEMO_NAME_D = "Herr Wagner"
DEMO_NAME_E = "Frau Müller"
DEMO_NAME_KU = "Herr Weiß"
DEMO_NAME_M = "Herr Bauer"

DEMO_HTML_BASE = """
<!DOCTYPE html>
<html>
<body>
<form class='form-signin' action='/includes/project/auth/login.php' method='post' autocomplete='off'><input type='hidden' name='csrf' value='1234567890abcdef'><div class="logo-head"><div id="logo"><div class="pull-right hidden-print"><div class="icons-right"><a href="start"><img src='/includes/project/images/logo_ep.png' style='height: 30px;'></a></div></div><a href="start"><h1 id="oben">Eltern-Portal</h1><h2 id="schule">Gymnasium Demo</h2></a></div><hr></div><label for='inputEmail'>Email Adresse</label><input type='email' name='username' id='inputEmail' class='form-control' placeholder='E-Mail-Adresse' required autofocus value=''><label for='password'>Passwort <span onClick='showPwd()'>👁</span></label><input type='password' name='password' id='password' class='form-control' placeholder='Passwort' required ><input type='hidden' name='go_to' value=''><button class='btn btn-lg btn-primary btn-block' type='submit' onclick='function() { this.disabled=true; return true; }()'>Anmelden</button><hr><div id='links' style='margin-top: 10px; text-align: center;'><a href='registrieren' class='btn btn-sm btn-default'>Registrieren</a> <a href='passwort_vergessen' class='btn btn-sm btn-default'>Passwort&nbsp;vergessen</a> <a href='/includes/files/EP_eltern_anmeldung_startseite_2021-07.pdf' class='btn btn-sm btn-default' target='_blank' rel='noopener'>Hilfe</a><hr><a onclick='$("#modal_impressum").modal("show");' style='cursor: pointer;' class='btn btn-sm btn-default'>Impressum</a> <a onclick='$("#modal_datenschutz").modal("show");' style='cursor: pointer;' class='btn btn-sm btn-default'>Datenschutzerklärung</a></div><div id="modal_impressum" class="modal fade text-start" tabindex="-1" role="dialog">
</body>
</html>
"""

DEMO_HTML_BLACKBOARD = """
<!DOCTYPE html>
<html>
<body>
<div class="" id="asam_content">
<div class='row'><div class='col-xs-12'><div class="grid">
<div class="grid-item"><div class='well' style='background-color: #fcdb92'><p style='color: #2F4F4F; font-size: 10px; margin-top: -10px; padding-bottom: 5px; margin-right: -5px;' class='text-right' >eingestellt am #TODAY# 00:00:00</p><h4 style='color: #2F4F4F; padding-bottom: 5px;' class=''>Münchner Elternabend Medien</h4><p style='color: #2F4F4F;'>Medienpädagogik</p><p style='color: #2F4F4F;'>Anhang: <a href='aktuelles/get_file/?repo=1&csrf=1234567890abcdef' title='Münchner Elternabend Medien.jpg herunterladen' target='_blank' rel='noopener'><img src='/includes/project/images/paperclip.gif'></a></p></div></div>
</div></div></div>
</body>
</html>
""".replace(
    "#TODAY#", DEMO_TODAY
)

DEMO_HTML_LOGIN = """
<!DOCTYPE html>
<html>
<body >
<div class="logo-head"><div id="logo"><div class="pull-right hidden-print"><div class="icons-right"><a href="einstellungen" style="margin-right:0.5em" class="btn btn-default btn-sm"><span class="glyphicon glyphicon-wrench"></span></a><a href="logout" style="margin-right:0.5em" class="btn btn-danger btn-sm"><span class="glyphicon glyphicon-off"></span></a><a href="start"><img src='/includes/project/images/logo_ep.png' style='height: 30px;'></a></div><div class="text-right settings">letzter Login: heute um 09:00 Uhr</div></div><a href="start"><h1 id="oben">Eltern-Portal</h1><h2 id="schule">Gymnasium Neufreimann</h2></a></div><nav class="navbar navbar-head"><button type="button" class="navbar-toggle collapsed btn btn-primary btn-lg" data-toggle="collapse" data-target="#top-navbar" aria-expanded="false"><span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button><div class="pupil-selector"><div class="form-group"><select class="form-control" onchange="set_child(this.value)"><option value="1" selected>Erika Mustermann (5a)</option></select></div></div><div class="clearfix"></div><div class='collapse navbar-collapse' id='top-navbar'><ul class='nav navbar-nav navbar-left'><li class='dropdown blue '><a href='service' class='dropdown-toggle iconed' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><div class='component'><div class='icon'></div></div>Service<span class='caret'></span></a><ul class='dropdown-menu'><li><a href='service/stundenplan'>Klassen Stundenplan</a></li><li><a href='service/klassenbuch'>Klassenbuch</a></li><li><a href='service/termine'>Schulaufgaben / Weitere Termine</a></li></ul></li><li class='dropdown orange '><a href='buchungen' class='dropdown-toggle iconed' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><div class='component'><div class='icon'></div></div>Buchung<span class='caret'></span></a><ul class='dropdown-menu'><li><a href='buchungen/sprechstunde'>Buchung Sprechstunde</a></li><li><a href='buchungen/wahlkurse'>Voranmeldung Wahlkurse</a></li><li><a href='buchungen/intensivierungskurse'>Voranmeldung Intensivierungskurse</a></li></ul></li><li class='dropdown red '><a href='aktuelles' class='dropdown-toggle iconed' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><div class='component'><div class='icon'></div></div>Aktuelles<span class='caret'></span> <span class='badge list-group-item-danger'>0</span></a><ul class='dropdown-menu'><li><a href='aktuelles/schwarzes_brett'>Schwarzes Brett &nbsp;&nbsp;&nbsp;&nbsp;<span class='badge list-group-item-danger'>0 NEU</span></a></li><li><a href='aktuelles/elternbriefe'>Elternbriefe&nbsp;&nbsp;<span class='badge list-group-item-danger'>0 NEU</span></a></li><li><a href='aktuelles/umfragen'>Umfragen/Abfragen&nbsp;&nbsp;<span class='badge list-group-item-danger'>0 NEU</span></a></li></ul></li><li class='dropdown green '><a href='meldungen' class='dropdown-toggle iconed' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><div class='component'><div class='icon'></div></div>Meldungen<span class='caret'></span> <span class='badge list-group-item-danger'>0</span></a><ul class='dropdown-menu'><li><a href='meldungen/krankmeldung'>Krankmeldung</a></li><li><a href='meldungen/befreiung'>Antrag auf Unterrichtsbeurlaubung</a></li><li><a href='meldungen/kommunikation'>Kommunikation Eltern/Klassenleitung&nbsp;&nbsp;<span class='badge list-group-item-danger'>0 NEU</span></a></li><li><a href='meldungen/kommunikation_fachlehrer'>Kommunikation Eltern/Fachlehrer&nbsp;&nbsp;<span class='badge list-group-item-danger'>0 NEU</span></a></li></ul></li><li class='dropdown yellow '><a href='dokumente' class='dropdown-toggle iconed' data-toggle='dropdown' role='button' aria-haspopup='true' aria-expanded='false'><div class='component'><div class='icon'></div></div>Dokumente<span class='caret'></span></a><ul class='dropdown-menu'><li><a href='dokumente/formulare'>Formulare</a></li><li><a href='dokumente/allgemein'>Allgemeine Dokumente</a></li></ul></li></ul></div></nav></div>
</body>
</html>
"""

DEMO_HTML_LOGOUT = """
<!DOCTYPE html>
<html>
<body>
</body>
</html>
"""

DEMO_JSON_APPOINTMENT = """
{
    "success": 1,
    "result": [
        {
            "id": "id_1",
            "title": "Schulaufgabe in Englisch",
            "title_short": "SA in Englisch",
            "class": "event-important",
            "start": "1729720800000",
            "end": "1729799200000",
            "bo_end": "0"
        },
        {
            "id": "id_2",
            "title": "Schulaufgabe in Deutsch",
            "title_short": "SA in Deutsch",
            "class": "event-important",
            "start": "1730934000000",
            "end": "1731012400000",
            "bo_end": "0"
        },
        {
            "id": "id_3",
            "title": "Schulaufgabe in Mathematik",
            "title_short": "SA in Mathematik",
            "class": "event-important",
            "start": "1732834800000",
            "end": "1732913200000",
            "bo_end": "0"
        }
    ]
}
"""

DEMO_HTML_LESSON = """
<!DOCTYPE html>
<html>
<body >
<div class="" id="asam_content">
<table class='table_header' width='100%' border='0'><tr><td><h2><img src='/includes/project/images/service_blau_20h.png' style='margin-right:10px;margin-bottom:10px;' />Stundenplan der Klasse<span class='hidden-xs' style='float: right; padding-top: 6px; font-size: 14px; margin-right: 1px;'>[<a href='/includes/pdf_gen.php?opt=6' title='Stundenplan drucken' target='_blank' class='link_service' rel='noopener'>Drucken</a>]</span></h2></td></tr></table><div class='table-responsive'><style>th { text-align: center; }</style><table width='100%' class='table table-condensed table-bordered'><tr><th width='15%' align='center'>&nbsp;</th><th width='17%' align='center'>Montag</th><th width='17%' align='center'>Dienstag</th><th width='17%' align='center'>Mittwoch</th><th width='17%' align='center'>Donnerstag</th><th width='17%' align='center'>Freitag</th></tr><tr><td width='15%' align='center' valign='middle' >0.<br>08.00 - 08.10</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td></tr><tr><td width='15%' align='center' valign='middle' >1.<br>08.10 - 08.55</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ku<br />OG2_24</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>E<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>M<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>D<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>M<br />OG1_18</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >2.<br>08.55 - 09.40</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ku<br />OG2_24</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>E<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>M<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>D<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>M<br />OG1_18</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >3.<br>10.00 - 10.45</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>NuT_NWw/Sm<br />OG2_21/</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Geo<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>NuT_NWm/Sw<br />OG2_21/</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ev/K/Eth<br />OG1_18/OG1_19/OG1_23</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Mu<br />EG_54</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >4.<br>10.45 - 11.30</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>E_Iw/Sm<br />OG1_18/</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Geo<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Sw/E_Im<br />/OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ev/K/Eth<br />OG1_18/OG1_19/OG1_23</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Mu<br />EG_54</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >5.<br>11.45 - 12.30</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>D<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Sm/Sw<br />/</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>D<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>E<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>NuT_B<br />OG2_21</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >6.<br>12.30 - 13.15</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>E<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Sw/Sm<br />/</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>D<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>E<br />OG1_18</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>NuT_B<br />OG2_21</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >7.<br>13.15 - 14.00</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Chor_US_Wahl<br />EG_54</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Stimm_Wahl/Schach_Wahl<br />EG_54/OG1_15</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Fussball_Wahl/Big_Band_Wahl<br />/EG_54</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >8.<br>14.00 - 14.45</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ku_Wahl_Werkzeuge/Chor_US_Wahl<br />OG2_24/EG_54</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ku_Wahl_Foto/D_Fö/Stimm_Wahl<br />OG2_24/OG1_18/EG_54</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Big_Band_Wahl/Fussball_Wahl<br />EG_54/</span></span></td></tr><tr><td width='15%' align='center' valign='middle' >9.<br>14.45 - 15.30</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>TTennis_Wahl/Orch_US_Wahl/Ku_Wahl_Werkzeuge<br />/EG_54/OG2_24</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ku_Wahl_Foto<br />OG2_24</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td></tr><tr><td width='15%' align='center' valign='middle' >10.<br>15.30 - 16.15</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Orch_US_Wahl<br />EG_54</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Schwim_Wahl<br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span>Ku_Wahl_Foto<br />OG2_24</span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td></tr><tr><td width='15%' align='center' valign='middle' >11.<br>16.15 - 17.00</td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td><td width='17%' align='center' valign='middle' style=''><span style='overflow-x:hidden; word-break:break-all;display: table-cell;'><span><br /></span></span></td></tr></table></div>        </div>
</body>
</html>
""".replace(
    "#EName#", DEMO_NAME_E
)

DEMO_HTML_LETTER = """
<!DOCTYPE html>
<html>
<body>
<div class="" id="asam_content">
<table class='table_header' width='100%' border='0'><tr><td align='left' valign='top' width='15%' class=''>#1</td><td align='right' valign='top' width='85%' class='' id='empf_1'>Empfang bestätigt.</td></tr><tr><td align='left' valign='top' width='100%' class='' colspan='2' style='word-wrap: break-word;'><span onmouseover='' style='cursor: pointer;' onclick='eb_bestaetigung(1);' class='link_nachrichten ' title='Empfang bestätigen'><h4>1. Klassenelternabend</h4> (keine Datei - Empfang durch Klick auf Titel bestätigen) #NOW#</span><br /><span style='font-size: 8pt;'>Klasse/n: 5a</span><br />Erinnerung: Herzliche Einladung zum 1. Elternabend heute Abend um 19.00 Uhr im Klassenzimmer Ihres Kindes<br />
Wir freuen uns auf Sie!<br />
Gymnasium Demo</td></tr></table>
</div>
</body>
</html>
""".replace(
    "#NOW#", DEMO_NOW6
)

DEMO_HTML_POLL = """
<!DOCTYPE html>
<html>
<body >
<div class="" id="asam_content">
<!-- UMFRAGEN -->
<div class="row">
<div class="col-xs-12 col-md-8 col-md-offset-2">

<div class="row m_bot">
<!-- titel -->
<div class="col-xs-6">
<a href="aktuelles/umfragen/2_0" title="" class=" umf_list">Elternbeiratswahl</a>
<a id="umf_file" title="Anhang" href="aktuelles/get_file/?repo=1&csrf=1234567890abcdef" target="_blank" class="" style="cursor: pointer;" rel='noopener'>
<img style="margin-bottom: 6px; margin-right: 5px; margin-left: 5px;" src="/includes/project/images/dokumente_grey_20h.png">
</a>
</div>
<!-- datum bis -->
<div class="col-xs-3 text-center">
<span>#TODAY#</span>                            </div>
<!-- abgeschlossen -->
<div class="col-xs-3 text-center">
<span style='pad'>#TODAY#<img class='pull-right' src='/includes/project/images/haken.png' /></span>                            </div>
</div>

</div>
</div>
</div>
</body>
</html>
""".replace(
    "#TODAY#", DEMO_TODAY
)

DEMO_HTML_POLL_DETAIL = """
<!DOCTYPE html>
<html>
<body >
<div class="" id="asam_content">
<form class='form-horizontal' action='/includes/nachrichten_dir/umfragen_editor_db_ins.php' method='post'><input type='hidden' name='csrf' value='1234567890abcdef'><div class='form-group'><div class='col-xs-12 col-md-10 col-md-offset-1'><h3 style='padding-bottom: 10px; line-height: 115%;#><span style='text-decoration: underline;'>Elternbeiratswahl</span><a id='umf_file' title='Anhang' href='aktuelles/get_file/?repo=88&csrf=7b0ec63e19360b5a' target='_blank' style='cursor: pointer;' rel='noopener'><img style='margin-bottom: 5px; margin-right: 5px; margin-left: 5px;' src='/includes/project/images/dokumente_grey_20h.png'><span style='font-size:12px'>(Anhang durch Klick herunterladen)</span></a></h3><input type='hidden' name='UMF_ID' value='2'></div></div><div class='form-group'><div class='col-xs-12 col-md-10 col-md-offset-1'>Liebe Eltern und Erziehungsberechtigte,<br />
<br />
hiermit laden wir Sie herzlich zur Elternratswahl ein. Im Anhang finden Sie die Steckbriefe der elf Kandidatinnen und Kandidaten für den Elternbeirat. Ab sofort haben Sie die Möglichkeit, Ihre Stimme abzugeben. Details zur Wahl finden Sie ebenfalls in der angehängten Datei.<br />
<br />
Herzliche Grüße<br />
Gymnasium Demo</div></div>
</body>
</html>
"""

DEMO_HTML_REGISTER = (
    """
<!DOCTYPE html>
<html>
<body >
<div class="" id="asam_content">
<table class='table table-bordered'>
<thead><tr><th scope='col' style='width: 20%;'></th>
<th scope='col'>Englisch - Lehrkraft: #NAME_E# (Einzelstunde)</th></tr></thead>
<tbody><tr><td>Hausaufgabe</td><td><i>Keine Hausaufgabe eingetragen.</i></td></tr></tbody></table>
<table class='table table-bordered'><thead><tr><th scope='col' style='width: 20%;'></th>
<th scope='col'>Englisch - Lehrkraft: #NAME_E# (Einzelstunde)</th></tr></thead>
<tbody><tr><td>Hausaufgabe</td>
<td>Vocab p.206 (no green boxes)<br />- <i>Zu Erledigen bis: #TOMORROW#</i></td>
</tr></tbody></table>
<table class='table table-bordered'><thead><tr><th scope='col' style='width: 20%;'>
</th><th scope='col'>Kunst - Lehrkraft: #NAME_KU# (Doppelstunde)</th></tr></thead>
<tbody><tr><td>Hausaufgabe</td><td><i>Keine Hausaufgabe eingetragen.</i></td></tr>
<tr><td>Datei(e)n</td>
<td>Datei 1:
<a href='service/get_lesson_file/?csrf=1234567890abcdef&f=1'
target='_self'>Arbeitsauftrag Kunst.docx</a> (16.5 KB)<br /></td></tr></tbody></table>
<table class='table table-bordered'><thead><tr><th scope='col' style='width: 20%;'></th>
<th scope='col'>Deutsch - Lehrkraft: #NAME_D# (Einzelstunde)</th></tr></thead>
<tbody><tr><td>Hausaufgabe</td>
<td>SB S. 215 (Adverbien)<br />- <i>Zu Erledigen bis: #TOMORROW#</i></td></tr></tbody></table>
<table class='table table-bordered'><thead><tr><th scope='col' style='width: 20%;'></th>
<th scope='col'>Fach:  - Lehrkraft: #NAME_M# (Einzelstunde)</th></tr></thead>
<tbody><tr><td>Hausaufgabe</td>
<td>Säulendiagramm mit zwei Datensätzen (siehe Datei im Anhang) fertig stellen<br />
- <i>Zu Erledigen bis: #TOMORROW#</i></td></tr>
<tr><td>Datei(e)n</td><td>Datei 1:
<a href='service/get_lesson_file/?csrf=1beaf60e2d93ff85&f=360'
target='_self'>Rucksack Beispieldaten.pdf</a> (460.8 KB)<br /></td></tr></tbody></table>
</div>
</body>
</html>
    """.replace(
        "#NAME_D#", DEMO_NAME_D
    )
    .replace("#NAME_E#", DEMO_NAME_E)
    .replace("#NAME_M#", DEMO_NAME_M)
    .replace("#NAME_KU#", DEMO_NAME_KU)
    .replace("#TOMORROW#", DEMO_TOMORROW)
)

DEMO_HTML_SICKNOTE = """
<!DOCTYPE html>
<html>
<body >
<div class='' id='asam_content'>
<table class="ui table">
<tr>
<td class="one wide">
</td>
<td class="four wide">
#TODAY#<br />#TODAY#
</td>
<td class="eleven wide"></td>
</tr>
</table>
</div>
</body>
</html>
""".replace(
    "#TODAY#", DEMO_TODAY
)

DEMO_HTML_MESSAGE = """
<!DOCTYPE html>
<html>
<body>
<div class='' id='asam_content'>
<div class='table-responsive'>
<table width='100%' border='0' cellpadding='4' cellspacing='2' class='table2'>
<tr><td align='left' valign='top' width='100%' class=''>Neue Nachrichten </td></tr>
<tr><td align='left' valign='top' width='100%' style='border: none;'><small>Keine neuen Nachrichten.</small></td></tr>
</table>
</div>
<div class='table-responsive'>
<table width='100%' border='0' cellpadding='4' cellspacing='2' class='table2' style='margin-top: 30px;'>
<tr><td align='left' valign='top' width='35%' class=''>Name</td><td align='left' valign='top' width='20%' class=''>F&auml;cher</td><td align='left' valign='top' width='35%' class=''>Kommunikation</td><td align='left' valign='top' width='10%' class=''></td></tr>
<tr class=''><td colspan='2' align='left' valign='top' class='' style='border: none;'><a name='I' title='Namen mit I' style='color:#767206; font-weight: bold;' >I</a></td><td colspan='1' align='right' valign='middle' class='' style='border: none;'></td><td colspan='1' align='right' valign='middle' class='' style='border: none;'>&nbsp;</td></tr>
<tr class=''><td align='left' valign='top' width='35%' class='' style='padding-top: 7px; padding-bottom: 7px;'>"#NAME_D#, StR</td><td align='left' valign='top' width='20%' class=''>D, E</td><td align='left' valign='top' width='35%' class=''><a href='meldungen/kommunikation_fachlehrer/1' title='Nachricht senden'>1 Anfrage</a><br /><img src='/includes/project/images/arrow_down.png' height='16' width='16' border='0' /> #NOW#</td><td align='center' valign='center' width='10%' class=''><a href='meldungen/kommunikation_fachlehrer/1' title='Nachricht senden'><img src='/includes/project/images/meldungen_gruen_20h.png' border='0' /></a></td></tr>
</table>
</div>
</body>
</html>
""".replace(
    "#NAME_D#", DEMO_NAME_D
).replace(
    "#NOW#", DEMO_NOW5
)

DEMO_HTML_MESSAGE_TEACHER = """
<!DOCTYPE html>
<html>
<body>
<div class='' id='asam_content'>
<div class='form-group'><label class='col-lg-3 col-md-3 col-sm-2 col-xs-12 control-label' style=''><img src='/includes/project/images/arrow_down.png' height='16' width='16' border='0' /> #NOW#</label><div class='col-lg-6 col-md-7 col-sm-9 col-xs-12' style=''><a href='meldungen/kommunikation_fachlehrer/1/1' class='btn btn-default btn-block ' style='text-align: left; white-space: normal;' role='button'>Informationen Englisch</a></div></div>
</div>
</body>
</html>
""".replace(
    "#NAME_D#", DEMO_NAME_D
).replace(
    "#NOW#", DEMO_NOW5
)

DEMO_HTML_MESSAGE_DETAIL = """
<!DOCTYPE html>
<html>
<body >
<div class='' id='asam_content'>
<div class='row'><div class='col-xs-12'><h2><img src='/includes/project/images/meldungen_gruen_20h.png' style='margin-right:10px;margin-bottom:10px;' />Kommunikation mit #NAME_D#</h2></div></div>
<div class='row'><div class='col-lg-3 col-md-3 col-sm-2 col-xs-12 text-right bold' style='padding-bottom: 20px;'>Betreff:</div><div class='col-xs-12 col-sm-9 col-md-7 bold' id='betreff_set'>Lernen lernen 5. Klasse</div></div>
<div class='row'><div class='col-lg-3 col-md-3 col-sm-2 col-xs-12 text-right bold' style='padding-bottom: 20px;'>Für:</div><div class='col-xs-12 col-sm-9 col-md-7 bold' id='betreff_set'>Johanna Ullrich</div></div>
<div id='last_messages'>
<div class='row' style='margin-bottom: 22px;'><label class='col-lg-3 col-md-3 col-sm-2 col-xs-12 control-label text-right'>
<span class='link_buchungen'>#NAME_D#</span>:<br><small style='font-weight: normal'>(#TODAY#)&nbsp;</small></label>
<div class='col-lg-6 col-md-7 col-sm-9 col-xs-12'>
<div class='form-control arch_kom' rows='2' maxlength='256' style='height: 100%;cursor:pointer'>Liebe Eltern und Erziehungsberechtigte,<br />
<br />
heute habe ich die erste Einheit zum Lernen lernen in der 5a durchgeführt.<br />
Wir haben allgemeine Schwierigkeiten des Schulalltags besprochen und Lösungen erörtert (Arbeitsblatt 1). Außerdem haben wir einen Wochenplan erstellt (Arbeitsblatt 2), in dem die Schülerinnen und Schüler ihre fixen Termine und mögliche Lernzeiten eingetragen haben. Auf der Rückseite finden Sie einen leeren Wochenplan als Kopiervorlage, falls sich die Termine ändern sollten und Sie erneut einen Wochenplan erstellen möchten.<br />
Die Schülerinnen und Schüler sollen die Arbeitsblätter in ihren Lernen lernen Schnellhefter (Farbe schwarz) abheften. Gerne können Sie die Inhalte nochmal mit Ihrem Kind durchsprechen.<br />
<br />
Liebe Grüße<br />
#NAME_D#</div></div></div></div>
</body>
</html>
""".replace(
    "#NAME_D#", DEMO_NAME_D
).replace(
    "#TODAY#", DEMO_TODAY
)
