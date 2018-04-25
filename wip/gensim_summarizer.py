# -*- coding: utf-8 -*-

from gensim.summarization.summarizer import summarize
text = '''
– Forstår ikke helt begrunnelsen.
Eksperter stusser over argumentene som brukes for å reversere Siv Jensens senkede inflasjonsmål. – Veldig kortsiktig, mener sjeføkonom.


– Forstår ikke helt begrunnelsen

Eksperter stusser over argumentene som brukes for å reversere Siv Jensens senkede inflasjonsmål. – Veldig kortsiktig, mener sjeføkonom.

Siv Jensen og finansdepartementet har allerede senket inflasjonsmålet til to prosent,  men nå har KrF gått sammen med venstrepartiene og bedt regjeringen skru det tilbake til 2,5 prosent. Partiet presiserer samtidig at det er regjeringen som bestemmer.

Aps finanspolitiske talsperson, Rigmor Aasrud, bekrefter at finanskomiteen i Stortinget går imot Jensens senkede inflasjonsmål.

Det er fordi to prosents inflasjon vil presse opp rentene «unødvendig tidlig», gi sterkere krone og større problemer for den norske eksportindustrien, argumenterer Aasrud.

Stortingsflertallet vekker oppsikt.

Og økonomer stusser over argumentene.

– Jeg forstår ikke helt den begrunnelsen, at problemet med å senke inflasjonsmålet er at renten kommer opp for tidlig. Norges Bank har selv fastslått at det har liten betydning, sier analytiker Jeanette Strøm Fjære i DNB Markets til E24.

– Dette blir uansett et veldig kortsiktig hensyn, sier sjeføkonom Elisabeth Holvik i Sparebank 1 Gruppen til E24.

– Renteøkningen fremskyndes helt marginalt i Norges Bank siste rapport. Imens viser prognosene at Norge vil få lavere renter om noen år med to prosents inflasjonsmål, fortsetter sjeføkonomen, som mener det siste er det avgjørende.


Mener Ap tar feil.

Hun har også problemer med å kjøpe begrunnelsen om at regjeringens senkede inflasjonsmål skader eksportindustrien.

Det er tvert imot helt motsatt, sier sjeføkonomen:

– Etter at Norge innførte målet om 2,5 prosent inflasjon, har lønns- og kostnadsutviklingen vært mye høyere enn i andre land. Det har skadet konkurransekraften til eksportindustrien, sier Holvik.

Normalen i utlandet er nemlig et inflasjonsmål på to prosent.

– Vi har altså hatt et høyere inflasjonsmål enn andre land. Jeg mener det var bra å senke målet til to prosent. Ved å øke det tilbake til 2,5 prosent, risikerer man på sikt å skade eksportindustrien, sier Holvik.


Det gode 2,5-argumentet.

Å ha samme inflasjonsnivå som andre land er kanskje det viktigste argumentet for inflasjonssenkingen regjeringen har gjort, mener Strøm Fjære i DNB Markets.


Men også et høyere 2,5 prosent-mål har sine fordeler, påpeker hun.

– Med et høyere inflasjonsnivå vil også det nominelle rentenivået holdes noe høyere. Det gir sentralbanken mer handlingsrom for å stimulere økonomien i nedgangstider, sier hun.

– Det pågår nå en debatt i flere land om hvorvidt man skal heve inflasjonsmålet for å gi seg mer handlingsrom i pengepolitikken, legger hun til.

Norges Bank vil ikke kommentere.

Men NHO-sjeføkonom Øystein Dørum er ikke begeistret for politikere som vingler frem og tilbake mellom hva målet skal være.

– Stortinget sier nei til lavere inflasjonsmål. Meget oppsiktsvekkende. Kan ikke endre rammevilkårene for kronekursen «hver måned», skriver han på Twitter.

Imens ønsker ikke Norges Bank å kommentere dagens nyhet overfor E24.

Sentralbanken har imidlertid selv støttet regjeringens endring:

«Det er vanskelig å finne tungtveiende argumenter for at Norge nå bør ha et annet mål for inflasjonen enn landene rundt oss», skrev Norges Bank i et tilsvar til Finansdepartementet tilbake i mars.

I både USA og Den europeiske sentralbanken er inflasjonsmålet to prosent.


Oljemilliarder.

Inflasjonsstyringen i Norge ble innført i 2001 med et mål om en inflasjon som over tid holdt seg rundt 2,5 prosent. Man satte målet til 2,5 og ikke 2,0 prosent, fordi man på den tiden regnet med at det skulle fases inn mange oljemilliarder i norsk økonomi.

Det regnet man med ville gi en noe høyere prisvekst i Norge enn i landene rundt oss. 

I sin nyeste pengepolitiske rapport fra mars skriver Norges Bank at effekten av å endre inflasjonsmålet avhenger av en rekke faktorer, men de skriver at det trolig har størst betydning for inflasjonsforventningene.

På kort sikt mener Norges Bank at renten kan bli høyere fordi «det vil ikke være behov for en fullt så ekspansiv pengepolitikk for å bringe inflasjonen mot målet».
'''

print(summarize(text=text, word_count=50))