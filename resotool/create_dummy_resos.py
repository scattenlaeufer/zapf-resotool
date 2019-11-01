#!/usr/bin/env python3

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resotool.settings")
import django

django.setup()
import markdown

from resotool.models import (
    Resolution,
    User,
    UserGroup,
    Recipient,
    ResoType,
    ResolutionEmail,
    SendStatus,
)
from resotool import settings


if not settings.DEBUG:
    print("Don't create dummy data in production!")
    exit()


if len(Resolution.objects.all()) > 0:
    Resolution.objects.all().delete()

if len(UserGroup.objects.all()) > 0:
    UserGroup.objects.all().delete()

if len(User.objects.all()) > 0:
    User.objects.all().delete()

if len(Recipient.objects.all()) > 0:
    Recipient.objects.all().delete()

user_group_1 = UserGroup(name="ZaPFikon")
user_group_1.save()
user_group_2 = UserGroup(name="DeepStAPF")
user_group_2.save()

user1 = User(name="Björn", university="RWTH Aachen")
user1.save()
user1.user_groups.add(user_group_1, user_group_2)

user2 = User(name="Jörg", university="FU Berlin")
user2.save()
user2.user_groups.add(user_group_1, user_group_2)

user3 = User(name="Stephie", university="HU Berlin")
user3.save()
user3.user_groups.add(user_group_1, user_group_2)

user4 = User(name="Peter", university="TU Darmstadt")
user4.save()
user4.user_groups.add(user_group_1)

user5 = User(name="Marlou", university="Uni Münster")
user5.save()
user5.user_groups.add(user_group_1)

reso1_text = """Die ZaPF solidarisiert sich mit der Bewegung „Fridays For Future“.

Wir fordern von den (Hoch)Schulen, die nötigen Freiräume zu schaffen, um Kindern, Jugendlichen und
junge Erwachsenen die Teilnahme an Protesten zu ermöglichen. Weiter verurteilen wir Repressionen gegen
an den Protesten Teilnehmenden. Dies betrifft sowohl die Androhung, als auch die konkrete Anwendung
solcher Maßnahmen.

Außerdem rufen wir alle Fachschaften dazu auf, die Proteste im Rahmen ihrer Möglichkeiten zu unterstüt-
zen und sich dafür einzusetzen, Studierenden die oben erwähnten Freiräume zu gewähren.
"""
reso1_text_html = markdown.markdown(reso1_text)
reso1_motivation = """Lorem ipsum dolor sit amet, consectetur adipiscing elit.
In posuere maximus tortor eget finibus. Nullam condimentum diam vitae
vestibulum lacinia. Donec dapibus porta dignissim. Etiam varius felis in sem
vestibulum sodales. Donec facilisis sollicitudin lorem, ac pulvinar justo
dignissim sed. Suspendisse sagittis sagittis est a dignissim. Maecenas dictum
mauris at risus tempor, ornare gravida dui facilisis. Fusce gravida facilisis
enim ut euismod. Ut hendrerit felis molestie dui sagittis sollicitudin. Aliquam
erat volutpat. Sed molestie ullamcorper pulvinar. Donec ultrices dui sit amet
maximus lobortis. Cras dignissim risus ut neque molestie egestas.

Phasellus ultrices sollicitudin velit, ac sagittis tellus iaculis in. Aliquam
elementum pretium magna, eu pulvinar nunc porttitor aliquet. Phasellus tempus
lorem ut turpis porttitor, vel sollicitudin quam egestas. Suspendisse est ante,
pellentesque a mi in, dapibus hendrerit elit. Ut aliquet sem mi, eget mattis
arcu gravida id. Ut fringilla, quam non ornare porta, nulla dolor volutpat
quam, sed luctus nibh odio posuere turpis. Donec quis felis vitae mauris
tincidunt posuere. Vivamus dignissim ex ultricies ornare consequat. Cras
accumsan nunc in dui molestie luctus. Ut auctor quis risus vel mattis.
Suspendisse commodo arcu vel iaculis viverra. Nulla augue purus, tempor eget
vestibulum eget, iaculis faucibus lorem. Sed sed purus in sem accumsan
sagittis. Pellentesque elit odio, hendrerit id eros eu, feugiat rhoncus odio.

Class aptent taciti sociosqu ad litora torquent per conubia nostra, per
inceptos himenaeos. Class aptent taciti sociosqu ad litora torquent per conubia
nostra, per inceptos himenaeos. Morbi et hendrerit metus, eu finibus turpis.
Nam porttitor elementum ligula, a efficitur ipsum dictum sit amet. Quisque
scelerisque odio at enim laoreet, quis tempor neque commodo. Curabitur tempus
tempor libero, ac viverra felis malesuada a. Proin feugiat, magna eu ultricies
dapibus, urna lorem venenatis tortor, fermentum imperdiet justo nibh eu risus.
Maecenas elit dui, molestie vel tincidunt et, fermentum quis odio. Curabitur
lorem lacus, ornare id quam eget, dignissim venenatis diam. Nunc sagittis,
massa ac tristique pharetra, metus libero finibus nulla, sed sagittis lacus
nulla a nunc. Nam in erat nec diam scelerisque congue id facilisis nulla.
Aenean tristique efficitur leo ac faucibus. Curabitur non libero nisi.
"""
reso1_motivation_html = markdown.markdown(reso1_motivation)
reso1 = Resolution(
    title="Solidarisierung der ZaPF mit Fridays for Future",
    reso_text=reso1_text,
    reso_text_html=reso1_text_html,
    motivation_text=reso1_motivation,
    motivation_text_html=reso1_motivation_html,
    reso_type=ResoType.RESOLUTION,
)
reso1.save()
reso1.user_set.add(user1, user2, user3)

recipient1 = Recipient(name="AFD", opening="Hallo,", email="afdhausen@weird.de")
recipient1.save()
recipient2 = Recipient(name="Grüne", opening="Hallo", email="grünehausen@seltsam.de")
recipient2.save()
recipient3 = Recipient(name="CDU", opening="Hallo,", email="cduhausen@schlecht.de")
recipient3.save()

mail1 = "wunderbarer Text der dir sagt warum du diese blöde Mail bekommen hast"

resomail1 = ResolutionEmail(resolution=reso1, recipient=recipient1, email_text=mail1)
resomail1.save()

resomail2 = ResolutionEmail(
    resolution=reso1,
    recipient=recipient2,
    email_text=mail1,
    status=SendStatus.IN_PROGRESS,
)
resomail2.save()

resomail3 = ResolutionEmail(
    resolution=reso1, recipient=recipient3, email_text=mail1, status=SendStatus.FAILURE
)
resomail3.save()

resomail4 = ResolutionEmail(
    resolution=reso1, recipient=recipient1, email_text=mail1, status=SendStatus.SUCCESS
)
resomail4.save()


reso2_text = """In den vergangen Jahren hat sich der studentische
Akkreditierungspool als Instanz zur Schulung von studentischen begutachtenden
Personen in allen Bereichen rund um den Themenkomplex der Akkreditierung von
Studiengängen, sowie als Kontaktquelle zu den studentischen begutachtenden
Personen etabliert. Die ZaPF als Vertretung der Physikstudierenden wertschätzt
und unterstützt die Arbeit des Pools und die dadurch gegebene
Qualitätssicherung.

Deshalb fordern wir, bei der Suche nach studentischen begutachtenden Personen
auf den studentischen Akkreditierungspool zurückzugreifen und dessen
Vorschlägen zu folgen. Eine Aquirierung von studentischen begutachtenden
Personen auf anderen Wegen lehnen wir ab. Dies gilt sowohl für Programm- als
auch für Systemakkreditierungsverfahren und interne Verfahren an
systemakkreditierten Hochschulen.

Des Weiteren rufen wir Fachschaften, die direkte Anfragen nach studentischen
begutachtenden Personen von Akkreditierungsagenturen erhalten, dazu auf, diese
Agenturen an den studentischen Akkreditierungspool weiterzuverweisen."""
reso2_text_html = markdown.markdown(reso2_text)
reso2 = Resolution(
    title="Zu studentischen begutachtenden Personen in Akkreditierungsverfahren",
    reso_text=reso2_text,
    reso_text_html=reso2_text_html,
    reso_type=ResoType.POSITIONSPAPIER,
)
reso2.save()
reso2.user_set.add(user4, user5)

reso3_text = """
Die ZaPF beauftragt den StAPF auf Basis der zu stellenden Anfrage nach
Informationsfreiheitsgesetz an das BMBF Gespräche mit der MeTaFa, dem BMBF und
dem DLR über die mittel- und langfristige Zukunft der Finanzierung von
Bundesfachschaftentagungen aus Mitteln des Topfes für "Förderung
hochschulbezogener zentraler Maßnahmen studentischer Verbände und anderer
Organisationen" aufzunehmen.

Als Grundlage dieser Gespräche soll das Protokoll des Arbeitskreises zum Umgang
mit Förderabsagen dienen.
"""
reso3_text_html = markdown.markdown(reso3_text)
reso3 = Resolution(
    title="Arbeitsauftrag an den StAPF zu Vörderungen durch das BMBF",
    reso_type=ResoType.SELBSTVERPFLICHTUNG,
    reso_text=reso3_text,
    reso_text_html=reso3_text_html,
)
reso3.save()
reso3.user_set.add(user1, user2)
