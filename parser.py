import json
import re

EMPTY_REGION = {
    "name": "Other",
    "items": [],
    "description": ""

}
MAIN_DUMP = ""
def get_one_item(title, data):
    '''
    Parse data and return only one item
    '''
    title = title.replace("(", "\(")
    title = title.replace(")", "\)")
    pattern = r"<page>\s+<title>" + title + r"</title>(?s:.)+?</page>"
    result = re.search(pattern, data)
    return result.group(0)

def get_dump(path):
    with open(path, 'r') as f:
        return f.read()

def get_first_name_from_double_meaning_word(word):
    try:
        pattern = r"(.+?)\|"
        result = re.search(pattern, word)
        first_part = result.group(1)
        return first_part + "]]"
    except Exception as e:
        return word

def logs(text):
    with open("logs.txt", "a+") as f:
        f.write(text + "\n")



def parse_continent(continent_name):
    dump = get_one_item(continent_name, MAIN_DUMP)
    def region_parse(dump):
        region = {}
        pattern = r"name(?:\s|)=(?:\s|)(.+)"
        result = re.search(pattern, dump)
        region["name"] = result.group(1)
        countries = []

        # if we don't find items, it mean regionname is list of countries in this region. So we create region with name OTHER
        try:
            pattern = r"items=(.+)"
            result = re.search(pattern, dump)
            pattern = r"\[\[.+?\]\]"
            countries_re = re.findall(pattern, result.group(1))
            for country in countries_re:
                countries.append(get_first_name_from_double_meaning_word(country))
            region["countries"] = countries
        except Exception as e:
            pattern = r"\[\[.+?\]\]"
            countries = re.findall(pattern, region["name"])
            region["countries"] = countries
            region["name"] = "Other - {}".format(region["name"])

        pattern = r"description=(.+)"
        result = re.search(pattern, dump)
        region["description"] = result.group(1)

        return region


    continent = {}
    pattern = r"<title>(.+)</title>"
    result = re.search(pattern, dump)
    continent["title"] = result.group(1)


    pattern = r"<id>(.+)</id>"
    result = re.search(pattern, dump)
    continent["id"] = result.group(1)

    pattern = r"<text.+>.+((?s:.)+?)(==)"
    result = re.search(pattern, dump)
    continent["description"] = result.group(1)


    pattern = r"(\|(?:\s|)region\d+name(?s:.)+?)(\n\n)"
    regions = re.findall(pattern, dump)

    continent["regions"] = []
    for region in regions:
        parsed_region = region_parse(region[0])
        continent["regions"].append(parsed_region)

    continent["description"] = result.group(1)

    return continent


# dump = get_dump("main_dump.xml")
#
# europe = get_one_item("Europe", dump)

europe = """<page>
    <title>Europe</title>
    <ns>0</ns>
    <id>11209</id>
    <revision>
      <id>3880367</id>
      <parentid>3874675</parentid>
      <timestamp>2019-11-09T17:01:15Z</timestamp>
      <contributor>
        <username>Traveler100bot</username>
        <id>160739</id>
      </contributor>
      <comment>/* By plane */Convert units template std format</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|Vatican_banner_Rafael's_&quot;School_of_Athens&quot;.jpg|caption=Raphael's &quot;School of Athens&quot;|origin=0,0}}
'''Europe''' attracts more tourists than any other continent: over 600 million international visitors annually, more than half of the global market. Out of Earth's ten most visited countries, seven are in Europe, with good reason

Although Europe is not one country, the ease of crossing borders might make you think otherwise, and transport infrastructure is generally efficient and well-maintained. At the other end of a short ride on a starkly modern [[high speed train]], a brief [[Flying|flight]], or an easy [[Driving|drive]], you will likely be able to delve into a new [[Phrasebooks#Europe|phrasebook]] and culture.

Europe has cultural heritage dating back [[European history|more than three millennia]]: the continent has seen the rise and fall of [[Ancient Greece]] and the [[Roman Empire]], and birthed the [[Renaissance architecture|Renaissance]] and the [[Industrial tourism|Industrial Revolution]]. Countless kingdoms, republics and empires have left [[archaeological sites]] and [[old towns]] galore, and the most magnificent cathedrals in the world for you to explore. Aside from history, Europe is the home of high culture, is renowned for its diverse cuisines, and is justly celebrated for its exciting and romantic cities.

Europe stretches from the shivering [[Arctic|Arctic Ocean]] in the north, to the pleasantly warm subtropical [[Mediterranean Sea]] in the south, and contains a vast array of temperate climates and variety of landscapes in between. The east of the continent is connected to [[Asia]], and for historical reasons a boundary is usually drawn from the [[Urals|Ural mountains]] via the [[Caucasus]] to the [[Aegean Sea]], while the continent's western extremities jut bracingly into the [[Atlantic Ocean]].

==Regions==

{{Worldimagemap/Europeimagemap}}
{{Regionlist

|regionmap=
|regionmaptext=
|regionmapsize=


|region1name=[[Balkans]]
|region1color=#69999f
|region1items=[[Albania]], [[Bosnia and Herzegovina]], [[Bulgaria]], [[Croatia]], [[Kosovo]], [[Moldova]], [[Montenegro]], [[North Macedonia]], [[Romania]], [[Serbia]]
|region1description=A rich and often turbulent history, with wonderful nature, charming multicultural towns, impressive monasteries and citadels dotting the hillsides, and mighty mountains liberally sprinkled with beautiful forests and pleasant lakes.

|region2name=[[Baltic states]]
|region2color=#b5d29f
|region2items=[[Estonia]], [[Latvia]], [[Lithuaia]]
|region2description=Fascinating states with glorious beaches along an extensive coastline, medieval towns, and beautiful natural scenery.

|region3name=[[Benelux]]
|region3color=#d5dc76
|region3items=[[Belgium]], [[Luxembourg]], [[Netherlands]]
|region3description=A largely flat area with a lot to offer. The Netherlands is known for its clogs, cheese, tulips, windmills, painters, and liberal attitudes. Belgium is a multilingual country with beautiful historic cities, bordering Luxembourg at the rolling hills of the [[Ardennes]].

|region4name=[[Britain and Ireland]]
|region4color=#b383b3
|region4items=[[Guernsey]], [[Ireland]], [[Isle of Man]], [[Jersey]], [[United Kingdom]]
|region4description=Britain has a patchwork of native and immigrant cultures, plus a fascinating history and dynamic modern culture, both of which remain hugely influential in the world. Ireland has rolling landscapes and characteristic customs, traditions and folklore.

|region5name=[[Caucasus]]
|region5color=#ac5c91
|region5items=[[Armenia]], [[Azerbaijan]], [[Georgia (country)|Georgia]]
|region5description=The Caucasus is a mountain range lying between the Black Sea and the Caspian Sea, part of the boundary between Europe and [[Asia]]. It is a dense, warm, friendly and generally safe region, with diverse landscapes and a wealth of ancient churches, cathedrals and monasteries.

|region6name=[[Central Europe]]
|region6color=#71b37b
|region6items=[[Austria]], [[Czech Republic]], [[Germany]], [[Hungary]], [[Liechtenstein]], [[Poland]], [[Slovakia]], [[Slovenia]], [[Switzerland]]
|region6description=Germanic culture meets Slavic culture in this region that straddles east and west, with historic towns, fairy-tale castles, beer, forests, unspoiled farmland, and mountain ranges, including the mighty [[Alps]].

|region7name=[[France]] and [[Monaco]]
|region7color=#a9a567
|region7items=
|region7description=France is the world's most popular destination and one of the most geographically diverse countries of Europe. Attractions include [[Paris]], picturesque [[Provence]], the [[French Riviera|Riviera]], Atlantic beaches, winter sports resorts of the [[French Alps|Alps]], [[castles]], rural landscape, and its gastronomy (particularly [[wine]]s and [[cheese]]s), history, culture and fashion.

|region8name=[[Greece]], [[Turkey]], [[Cyprus]] and [[Northern Cyprus]]
|region8color=#8a84a3
|region8items=
|region8description=With the most hours of sun in Europe, the Eastern Mediterranean is a haven for beach-goers, party-people and cultural enthusiasts alike, and is known for its rich and tasty cuisine.

|region9name=[[Iberia]]
|region9color=#d56d76
|region9items=[[Andorra]], [[Gibraltar]], [[Portugal]], [[Spain]]
|region9description=These countries are great destinations for their rich and unique cultures, lively cities, beautiful countryside and friendly inhabitants.

|region10name=Italian Peninsula
|region10color=#d09440
|region10items=[[Italy]], [[Malta]], [[San Marino]], [[Rome/Vatican|Vatican City]]
|region10description=[[Rome]], [[Florence]], [[Venice]] and [[Pisa]] are on many travellers' itineraries, but these are just a few of Italy's destinations. Italy has more history and culture packed into it than many other countries combined.


|region11name=[[Nordic countries]]
|region11color=#578e86
|region11items=[[Denmark]], [[Faroe Islands]], [[Finland]], [[Iceland]], [[Norway]], [[Sweden]]
|region11description=Spectacular scenery of mountains, lakes, glaciers, geysers, waterfalls and volcanoes with opportunity for outdoor life, known for the [[Vikings and the Old Norse|Viking Age]] around AD&amp;nbsp;1000. Also known for being bastions of progressive politics with the world's highest tax rates and most comprehensive welfare states.

|region12name=[[Russia]], [[Ukraine]], and [[Belarus]]
|region12color=#4f93c0
|region12items=
|region12description=Russia is a vast country that spans all the way [[Russian Far East|east]] to the Pacific Ocean. Ukraine is diverse, with a lot to offer, from the beach resorts of the Black Sea to the beautiful cities [[Odessa]], [[Lviv]], and [[Kiev]]. Belarus, sometimes called &quot;Europe's last dictatorship&quot;, is the largest remaining Soviet-style country in the world.
}}

==Cities==
&lt;!-- NOT MORE THAN 9 CITIES ALLOWED. DO NOT CHANGE THIS LIST BEFORE CONSENSUS ON THE TALK PAGE! --&gt;
* [[Amsterdam]] — canals, Rembrandt, hashish and red lanterns, the epitome of social liberal attitudes
* [[Barcelona]] — capital of Catalonia and home to Gaudí's famous ''Sagrada Família'' this place is much more than &quot;Spain's second city&quot;
* [[Berlin]] — scarred by four decades of division but experiencing an almost unprecedented boom, the capital of reunited Germany is one of Europe's most creative and innovative cities and still surprisingly affordable
* [[Istanbul]] — the heart of both the Ottoman and Byzantine Empire, this bi-continental city is a bridge between east and west and Europe's largest
* [[London]] — Europe's financial metropolis and the former heart of the British Empire, packed with all sorts of attractions from sports to museums and two millennia of history
* [[Moscow]] — the heart and brain of the largest country on Earth, Moscow has the heritage of both the tsars and the Soviets and all the other current or former occupants of the Kremlin
* [[Paris]] — the &quot;City of Light&quot; and one of the most visited places on Earth: romance, cuisine, the Eiffel Tower and a surprising amount of green await you
* [[Prague]] — home to Kafka and medieval emperors, this city has tons of well-preserved history as well as a vibrant nightlife to keep you fascinated
* [[Rome]] — an empire was named after this eternal city of seven hills and today it is chock full of old and new, and even contains its own state, the Vatican
&lt;!-- NOT MORE THAN 9 CITIES ALLOWED. DO NOT CHANGE THIS LIST BEFORE CONSENSUS ON THE TALK PAGE! --&gt;


==Other destinations==
[[File:Spain Andalusia Granada BW 2015-10-25 17-22-07.jpg|thumb|[[Granada#The Alhambra|The Alhambra]] (Andalusia, Spain)]]
&lt;!-- DO NOT CHANGE THIS LIST BEFORE CONSENSUS ON THE TALK PAGE! --&gt;
* [[Alps]] — both a barrier and a bridge for millennia, Europe's climate is formed by them and the continent's transportation funneled into their passes. This mountain range is also Europe's most beloved winter sports and hiking destination, as well as home to mythical mountains like [[Mont Blanc]] or the [[Matterhorn]]
* [[Cinque Terre]] — a gorgeous national park, which connects five picturesque villages
* [[Curonian Spit]] — a sand dune which separates the Curonian Lagoon from the Baltic Sea, on the Russian-Lithuanian border
* [[Białowieża National Park]] — the last and largest remaining parts of the immense primeval forest that once spread across the European Plain
* [[Blue Lagoon]] — amazing geothermal spa with the water temperature around 40°C all year round, even in freezing conditions
* [[Mallorca]] — a Spanish island famous for seaside resorts, nightlife, and spectacular landscapes
* [[Meteora]] — six Eastern Orthodox monasteries built on natural sandstone rock pillars
* [[Plitvice National Park]] — beautiful turquoise-coloured lakes surrounded by a large forest
* [[Stonehenge]] — the well-known Neolithic and Bronze Age stone monument on Salisbury Plain
&lt;!-- DO NOT CHANGE THIS LIST BEFORE CONSENSUS ON THE TALK PAGE! --&gt;

==Understand==
Europe has an area of 10,180,000&amp;nbsp;km² (3,930,000 square miles), and 742 million inhabitants. European nations came to dominate the world from the 16th century and onwards. As the continent was devastated by the World Wars in the early 20th century, most Europeans now seek peace and unity.

===History===
{{seealso|Prehistoric Europe|European history}}

''Homo Sapiens'' reached Europe from Africa through the Middle East roughly 40&amp;nbsp;000 years ago, and displaced the ''Homo Neanderthalensis'', which died out around 30&amp;nbsp;000 years ago.

[[File:Roman Theatre Plovdiv.jpg|thumb|244x244px|The Roman Theatre of [[Plovdiv]], which is so well-preserved that it is still used as a theatre today.]]

As writing, farming and urban culture all spread to Europe from the [[Middle East]], European culture has owed much to &quot;foreign&quot; influences from its very beginning. The Mediterranean was one of the first centres of writing and city-states. Among its numerous cultures, those of [[Ancient Greece]] are the earliest well-known ones that arose in Europe. Greek poets such as Homer, Hesiod, and Kallinos dated to the 8th century BC are the oldest European writers still widely studied. Ancient Greece has been credited with the foundation of Western culture, and has been immensely influential on the language, politics, educational systems, philosophy, science, and arts of the European continent.


The city of [[Rome]], inhabited since at least 800&amp;nbsp;BC, became the centre of the [[Roman Empire]], which conquered much of Europe, as well as North Africa and the Middle East, and came to define a common European identity, through the [[Latin Europe|Latin]] language and alphabet, as well as law and architecture.  [[Christianity]] and [[Judaism]] were both found throughout the Empire by the early second century AD and the former seems to have been particularly popular with soldiers along the Germanic frontiers. After two centuries of on and off persecution, Constantine officially tolerated Christianity (though he did not convert until his dying moments) and intervened in theological debates, cementing a path that would lead to an openly Christian Empire that persecuted non-Christians and &quot;the wrong kind&quot; of Christianity alike. This pattern could be found throughout most of Europe in the ensuing millennium. Under the rule of Constantine's distant successor from another dynasty Theodosius, Christianity would be declared the state religion of Rome, and became mandatory for all Roman subjects, thereby leading to the eventual Christianisation of all Europe. Theodosius, who died in 395 after having briefly ruled both halves of the Empire, would also prove to be the last person to rule both the Eastern and Western Roman Empire, as the land was divided among his sons after his death. While this was not seen as a dramatic move at the time and such divisions had occurred before, the rift would grow deeper and never heal before the fall of the Western Empire some eighty years later. The cultural divide would deepen and ultimately result in a schism of Christianity during the Middle Ages that endures today.

====Middle Ages====
{{seealso|Vikings and the Old Norse|Hanseatic League}}

The Migration Period began around AD&amp;nbsp;300, and saw especially Germanic tribes moving across the continent, in part fleeing from Hunnic invasions. Military and political errors led to humiliating defeats for the Romans such as the Battle of Adrianople of 376 that saw emperor Valens and most of his army perish fighting Goths. Around AD&amp;nbsp;500 (AD 476 is a commonly cited date, but there are good arguments for slightly different dates) the Western Roman Empire ceased to be, with most of it invaded by Germanic tribes, such as the Franks in Gaul and Germania, and the Visigoths in Spain. The millennium that followed the fall of Rome has by posterity been called the Middle Ages.

[[File:Bayeux Tapestry in the museum.jpg|thumb|The Bayeux Tapestry in [[Bayeux]], [[France]], depicts the [[Normandy|Norman]] Invasion of England by William the Conqueror.]]

The eastern half of the Roman Empire continued on as the '''Byzantine Empire''', which dominated the eastern Mediterranean for a thousand years, was significantly weakened by the fourth crusade sacking Constantinople in 1204 and finally ceased to be when its capital ([[Constantinople]]) was finally conquered by the Ottoman Turks in 1453, who came to dominate southeastern Europe until the First World War. Roman scholarship survived in the Byzantine Empire, and later in the Muslim World.

The Franks rose to power under the Merovingian dynasty, and converted to Catholic Christianity in the 5th century. An Arab-Muslim force landed on the Iberian peninsula in 711, wiping out the Visigoths, conquering most of Iberia within the next few years, before being stopped by the Franks near [[Tours]] and [[Poitiers]] in 732. Much of Spain remained Muslim until the 15th century. The most notable Frankish ruler Charlemagne conquered much of Western Europe, and was crowned Holy Roman Emperor by the pope in 800&amp;nbsp;AD. The Carolingian empire largely disintegrated on Charlemagne's death in 814, and the last East-Frankish king of the Carolingian dynasty died in 911. The 9th and 10th centuries are also remembered for the [[Vikings and the Old Norse|Viking raids and expeditions]] from Scandinavia across most of Europe.


The 10th to 13th centuries are known as the High Middle Ages, and saw a wave of urbanisation especially in Western Europe, with the rise of cathedrals and universities, the first of which, University of [[Bologna]], has remained in continuous operation since 1088. The High Middle Ages were marked by the Crusades; a series of military campaigns launched by the Catholic church, many of them towards the [[Holy Land]]. Several crusades went nowhere near Jerusalem and one ended in the conquering and destruction of Constantinople, weakening the Byzantine Empire enough that it would collapse two centuries hence. Merchant-ruled city-states such as the [[Hanseatic League]], [[Novgorod]], [[Genoa]] and [[Venice]], came to control much of commerce in Europe, while the [[Mongol Empire]] came to conquer most of the European plains in the 13th century.

The Black Death (bubonic plague) killed one-third of Europe's population around 1350, making it probably the worst epidemic in European history.&lt;!--we cannot say for certain how many people perished due to diseases brought by the &quot;Columbian Exchange&quot; and we can argue until the cows come home whether it (or any of its component parts) was &quot;a single epidemic&quot;--&gt; The Black Death led to an increase in anti-Jewish pogroms and is cited as causing dissatisfaction with secular and religious authorities which had been largely powerless to stop it.

====Early modern period====
{{seealso|Medieval and Renaissance Italy}}

[[File:Florence duomo fc01.jpg|thumb|[[Florence]], the birthplace of the Renaissance with an astonishing cultural heritage]]

An intellectual movement called the [[Medieval and Renaissance Italy|Renaissance]] (rebirth) began in Italy and started to spread across Europe in the final years of the 15th century, rediscovering Classical Graeco-Roman culture. The invention of the printing press made books much more affordable, leading to broader literacy and the emergence of literature in languages besides Latin. This also enabled the faster spread of &quot;heretical&quot; ideas during the [[Protestant Reformation]] that unlike prior reform movements did not stay contained to scholarly circles (writing mostly in the vernacular and not Latin) and was not snuffed out in its infancy or contained locally like the 15th-century Jan Hus movement in what is now the Czech Republic. This period, which saw the invention of movable type, the voyages of Columbus and Vasco da Gama and the beginning of the Protestant Reformation, is usually considered the beginning of the Early Modern Era. The 17th and 18th centuries would bring about the '''Age of Enlightenment''', which saw the birth of [[Science tourism|modern science]], as well as the introduction of secularism and constitutional government. The ideals of the Enlightenment would greatly influence the founding fathers of the [[United States of America|United States]] during the [[Early United States history|American War of Independence]], with many of these ideals being incorporated into the United States Constitution.

Gunpowder weapons revolutionized warfare, including artillery that could tear down most medieval fortresses. A series of wars, especially the very destructive [[Thirty Years' War]] of the 17th century, replaced the political patchwork of nobles' fiefs and city-states with centralized empires, such as the [[Russian Empire]], the [[Austrian Empire]], and the [[Ottoman Empire]].


From the late 15th century, European navigators found the way to Asia, the Americas (see [[voyages of Columbus]]) and Oceania. They paved the way for Spain, Portugal and later other countries to establish colonies and trading posts on other continents, through superior military power, and epidemics that decimated much of the population, especially in America. The independence of the USA, Haiti and many other parts of the Americas at the turn of the 18th to the 19th century ended the first wave of colonialism. European interests turned to Africa, India, East Asia and Oceania, and from the 1880s onward Africa was colonised during what is commonly known as the &quot;Scramble for Africa&quot;, leaving only Liberia and Ethiopia independent. Most colonies became independent in the decades following World War II, and today only Spain has [[Spanish North Africa|some small possessions in mainland Africa]], while France, Spain and Portugal continue to control some islands off the African coast. Immigration from former colonies has shaped the face of Europe, and of countries such as France, Britain, the Netherlands, Belgium, Portugal and Spain in particular.

====Age of Revolutions====
{{seealso|Russian Empire|Austro-Hungarian Empire|British Empire|Industrial Britain|Nordic history}}

The '''Industrial Revolution''' began in Britain in the 18th century (see [[Industrial Britain]]), but took a century to spread to continental Europe.

Modern times in Europe are considered to have begun with the 1789 French Revolution, which was the beginning of the end of European aristocratic power and absolute monarchy, and led to a series of wars, including the [[Napoleonic Wars]]. Although Napoleon was ultimately defeated, the legacy of his rule over much of Europe can still be seen today, with the concept of secularism (also known as the &quot;separation of church and state&quot;) having been introduced by Napoleon into the occupied territories. The 19th century saw the rise of democracy, social reform and nationalism, with the unification of countries such as [[Germany]] and [[Italy]]. Some historians speak of the &quot;long 19th century&quot; beginning with the first major liberal European revolution in 1789 and ending with the beginning of the First World War, giving rise to the &quot;short 20th century&quot; that spans the 75 years from 1914 to 1989 and was dominated by the rise and fall of Soviet-style communism and an overall decline in the importance of Europe on the world stage.

[[World War I]], at its time known as the ''Great War'', caused unprecedented destruction, and made the end to the Russian, German, Austro-Hungarian and Ottoman empires. The [[Soviet Union]] replaced the Russian Empire, and fascist movements rose to power in Italy, and later in Spain, Portugal and Germany. While Europeans were weary of war, the League of Nations failed to stop the [[World War II in Europe|Second World War]], which came to be the most destructive war ever in Europe.

====Cold War and European integration====
{{seealso|Soviet Union|World War II in Europe|Holocaust remembrance|Cold War Europe}}

During World War II, there was destruction, wide-spread human suffering and large-scale war crimes. It singlehandedly ended the period in which the dominant power of Europe was the dominant power of the world, and the United States and the [[Soviet Union]] became the new superpowers.


The war led to a broad consensus across all political camps and in several countries that more cooperation among European countries was necessary to avoid another even bloodier war. Furthermore, the spectre of the Soviet-dominated East made cooperation appear more desirable for those countries in the West where parliamentary democracy had returned after the war. The first step was to cooperate in the fields of Coal and Steel (both essential to modern industry and any war effort) with West Germany, France, the Benelux states and Italy creating the European Coal and Steel Community in 1951. While Britain was a sympathetic spectator, it believed at the time that its interest lay in the Commonwealth and the (at the time still considerable) remains of the [[British Empire]], so it did not join this or any other attempt at European integration until two decades later. The six members of the European Coal and Steel Community meanwhile pressed on, signing the Treaty of Rome in 1956 and making more and more steps at common institutions, with formalized meetings of heads of government or ministers and a European parliament with democratic elections every five years. The 2014 elections were again the second biggest election in the world by numbers of votes cast (after Indian federal elections).

The end of the Second World War also gave rise to the [[Cold War]], which was perhaps most visible in Europe. Most of Europe was either dominated by the Soviet Union or closely allied with the US, with only a handful of neutral countries like Yugoslavia, Austria, Finland and Switzerland and even those that officially stayed neutral often heavily leaned one way or the other. The remaining dictatorships in the western aligned countries slowly fell - Spain transitioned to democracy shortly after Franco's death, Portugal's &quot;Estado Novo&quot; did not long outlast its founder Antonio Salazar and the Greek military junta fell in 1974. Meanwhile, Leninist dictatorships in the East remained firmly entrenched, even in places like Romania, Albania or Yugoslavia where leaders were able to implement less Moscow-dominated foreign policies or in places like Poland, Czechoslovakia or Hungary where popular uprisings had to be quashed by Soviet or domestic tanks. However, when Mikhail Gorbachev took over in the USSR, the economic malaise and political oppression led to widespread protests and by 1989 most regimes were either falling or reforming and Soviet tanks were not rolling in this time. While this is rightfully remembered as a mostly peaceful revolution, there was some violence in Romania and its president Nicolae Ceaușescu was the only dictator to find a violent death. Germany reunited in 1990 and the Soviet Union was dissolved in 1991 bringing the Cold War to an end.

As the process of European integration proved successful, most countries that could soon joined the European Communities. [[Ireland]], [[Denmark]] and the United Kingdom (after France gave up on its longstanding veto to British membership) joined in 1973, while Greece, Portugal and Spain joined in the 1980s after their dictatorships had been replaced by democratic regimes. Another round of enlargements occurred in 1995 when due to the end of the Cold War three democratic and capitalist neutral countries - Austria, Sweden and Finland - joined after there was no Cold War need to withhold participation any more. At the same time more and more powers were given to the European level and it was renamed the European Union in 1992 with a new currency to be introduced in 2002 after attempts to link European currencies in stable fixed exchange rates faced threats of speculation. However, the euro, as the new currency came to be called, was not introduced in all countries then-members of the EU, and it is today used by countries that are not members of the EU and will likely not join the EU for years to come, like Monaco or Kosovo. Several other countries that had pegged their currencies to French francs or the Deutsche Mark now peg their currencies to the euro instead.


The end of the Cold War also rose the question of whether former Soviet allies could join the EU and when and how this would take place. Unlike most previous expansions of the EU, which admitted no more than three countries at a time, this expansion was the biggest to date and on 1 May 2004 four former Soviet satellites (Poland, the Czech Republic, Slovakia and Hungary), three former Soviet Republics (Estonia, Latvia, Lithuania) one former Yugoslav Republic (Slovenia) and two former British colonies in the Mediterranean (Cyprus and Malta) joined the EU in what was dubbed the &quot;Eastern Expansion&quot;. Romania and Bulgaria joined in 2007 and Croatia became the second former Yugoslav Republic to join in 2013. Seven countries are in different stages of &quot;accession talks&quot;, but none of them are anywhere close to resolution and some of them seem to be maintained more out of diplomatic courtesy than anything else. [[Iceland]]  submitted an accession bid in the wake of the 2007 financial crisis but has subsequently expressed no intention of joining. North Macedonia, Montenegro and Serbia are applicants, but are considered to be economically and politically not ready for joining. The continued negotiations with Turkey (which seem to only exist on paper anyway at the moment) are in constant threat of being ended outright over diplomatic disagreements with its government. Norway and Switzerland remain outside the EU and are not having talks about accession. However, all non-members mentioned here have various forms of bilateral agreements and often follow EU rules and regulations and are sometimes party to some European agreements that are partly linked to the EU.

While the Iron Curtain is no more, Russia joining the EU is generally regarded unthinkable, and in some of the former Soviet states or satellites, whether to seek cooperation with Russia or with the EU is a major political issue. Neither Russia nor the EU has been particularly keen to pursue closer  political relations with the other.

Since the start of the Arab Spring, there has been a huge influx of Middle Eastern refugees fleeing war in their countries into Europe. This huge influx of immigrants has led to widespread discontent and a huge backlash, resulting in the rise of right-wing extremist parties, with such formerly fringe parties now forming the main oppositions or in some cases, even the governments in various countries. 

In 2016 the United Kingdom voted by referendum to leave the EU, with the date for leaving set for 31 October 2019. The relationship between the UK and the EU after leaving is being negotiated, and until the exit date is reached, things will, from a traveller's point of view, proceed as if the UK had never voted to leave.

===Geography===
[[File:Tour Eiffel Wikimedia Commons.jpg|thumb|upright|Eiffel Tower in [[Paris]] ]]
Europe makes up the western one fifth of the Eurasian landmass, bounded by bodies of water on three sides: the Arctic Ocean to the north, the Atlantic Ocean to the west, and the Mediterranean Sea to the south. Europe's eastern borders are ill-defined, and have been moving eastwards throughout history. Currently, the Ural and Caucasus Mountains, the Caspian and Black Seas and the Bosporus Strait are considered its eastern frontier, making [[Istanbul]] the only metropolis in the world on two continents. [[Cyprus]] is also considered a part of Europe culturally and historically, if not necessarily geographically. The geographic boundaries are a contentious issue and several eastern boundaries have been proposed.


Europe's highest point is Russia's Mount Elbrus in the [[Caucasus|Caucasus Mountains]], which rises to 5,642&amp;nbsp;m (18,510&amp;nbsp;ft) above sea level. Outside the Caucasus, the highest point is [[Mont Blanc]] in the [[Alps]] at 4,810&amp;nbsp;m (15,771&amp;nbsp;ft) above sea level. Other important mountain ranges include the [[Pyrenees]] between France and Spain and the [[Carpathians]] that run through Central Europe to the Balkans. Most regions along the North and Baltic Seas are flat, especially eastern England, the Netherlands, northern Germany and Denmark. The North and Baltic Seas also feature labyrinthine archipelagos and hundreds of miles of sandy beaches.

Europe's longest river is the Volga, which meanders 3,530&amp;nbsp;km (2,193&amp;nbsp;mi) through Russia, and flows into the Caspian Sea. The Danube and the Rhine formed much of the northern frontier of the [[Roman Empire]], and have been important waterways since pre-historic times. The [[Danube]] starts in the [[Black Forest]] in Germany and passes through the capital cities [[Vienna]], [[Bratislava]], [[Budapest]], and [[Belgrade]] before emptying in the Black Sea. The Rhine starts in the Swiss Alps and caused the [[Schaffhausen|Rhine Falls]], the largest plain waterfall in Europe. From there, it makes up the French-German border border flowing through Western Germany and the Netherlands. Many castles and fortifications have been built along the Rhine, including those of the [[Rhine Valley]].

===Climate===
Most of Europe has '''temperate''' climate. It is milder than other areas of the same latitude (e.g. north-eastern U.S.) due to the influence of the Gulf Stream. However, there are profound differences in the climates of different regions. Europe's climate ranges from subtropical near the Mediterranean Sea in the south, to subarctic and arctic near the Barents Sea and Arctic Ocean.

In general, seasonal differences increase further inland, from a few degrees on small Atlantic islands, to burning summer sun and freezing winter on the Russian plains.

Atlantic and mountain regions have high precipitation; especially north-western Spain, the United Kingdom, Ireland, Norway, the [[Alps]], and the Dinaric mountains on the western [[Balkans]]. North of the Alps, summers are slightly wetter than winters. In the Mediterranean most rain falls in the winter, while summers are mostly dry.

'''Winters''' are relatively cold in Europe, even in the Mediterranean countries. The only areas with daily highs around 15°C in January are [[Andalucia]] in Spain, some [[Greek Islands]], and the Turkish Riviera. Western Europe has an average of around 4–8°C in January, but temperatures drop below freezing throughout the winter. Regions east of [[Berlin]] have cold temperatures with average highs below freezing. [[Moscow]] and [[Saint Petersburg]] in [[Russia]] have average highs of -5°C and lows of -10°C in January. Most of the [[Nordic countries]] have averages below -10°C.

Winter in Europe might be most comfortable to spend in the light and warmth of a big city, unless you specifically want to enjoy the snow. In December, [[Christmas markets]] and other [[Christmas and New Year travel|Christmas and New Year]] attractions can be found. While tourism peaks during the holidays, the rest of the winter is low season in cities, providing decently cheap accommodation, and smaller crowds at famous attractions.

While the [[winter sport]] season begins in December in the [[Alps]] and other snowy regions, daylight and accumulated snow can be scarce until February. Mountains in the Alps, Pyrenees, Carpathians and Scandinavia have snow well into '''spring''' while the valleys get warm; allowing visitors to experience many seasons on the same day. The highest peaks of the Alps have perpetual snow.


Most of Europe has the most comfortable weather in '''summer''', though southern Europe can get unbearably hot. In August, the United Kingdom, Ireland, Benelux, Germany and northern France have average highs of around 23°C, but these temperatures cannot be taken for granted. The Mediterranean has the highest amount of sun-hours in Europe, and the highest temperatures. Average temperatures in August are 28°C in [[Barcelona]], 30°C in Rome, 33°C in [[Athens]] and 39°C in [[Alanya]] along the [[Turkish Riviera]]. Many workplaces close down in July or August, leaving the cities deserted and the seaside crowded.

'''Autumn''' provides colourful trees and harvest of [[fruits and vegetables]], with associated festivals (see [[agritourism]]), and is a good time to visit the countryside.

Summers have longer '''daylight''' than winter; the variation increases with latitude. At 60 degrees north ([[Shetland Islands]], [[Oslo]], [[Stockholm]], [[Helsinki]] and [[St Petersburg]]), ''white nights'' can be enjoyed in June, while the sun is above the horizon for only six hours in December. North of the Arctic Circle, visitors can see the [[Midnight Sun]] in summer, and the Arctic Night in winter.

The [http://meteoalarm.eu/?lang=en_UK Network of European Meteorological Services] has a useful website  providing up-to-date information for extreme weather, covering most of the EU countries.

{{Anchor|Schengen Agreement}}

==Get in==
{{infobox|Schengen Area|These countries are members of the Schengen Area: [[Austria]], [[Belgium]], [[Czech Republic]], [[Denmark]], [[Estonia]], [[Finland]], [[France]], [[Germany]], [[Greece]], [[Hungary]], [[Iceland]], [[Italy]], [[Latvia]], [[Liechtenstein]], [[Lithuania]], [[Luxembourg]], [[Malta]], [[Netherlands]], [[Norway]], [[Poland]], [[Portugal]], [[Slovakia]], [[Slovenia]], [[Spain]], [[Sweden]], and [[Switzerland]].

Although technically not part of the Schengen area, there are no border controls when travelling to [[Andorra]], [[Monaco]], [[San Marino]] and the [[Vatican City]] from the neighbouring countries, so they can for all practical purposes be considered part of it.}}

Rules for entering Europe depend on where you are going. Citizens of [[European Union]] countries and the European Free Trade Association (EFTA) countries (Iceland, Liechtenstein, Norway and Switzerland) can travel freely throughout the continent – except [[Russia]], [[Belarus]] and parts of the [[Caucasus]] – so the following applies only to non-EU/EFTA citizens.

If you are entering '''[[Travelling around the Schengen Area|a Schengen country]]''' ''and'' you plan to visit only other Schengen countries, you need '''only one Schengen visa'''. {{Schengen-visalist}}

If your rights in the European Union or Schengen depend on your connections with the UK, note the implications of '''[[European Union#Brexit|Brexit]]''', which may happen in 2019 or 2020.

The 90-day visa-free stay applies for ''the whole Schengen area'', i.e. it is not 90 days per country as some assume. Citizens of the above countries who wish to travel around Europe for longer than 90 days must apply for a residency permit. This can be done in any Schengen country, but Germany or Italy are recommended, because many other countries require applicants to apply from their home countries.

'''Non-Schengen countries''', on the other hand, maintain their own immigration policies. Consult the country article in question for details.  If you wish to visit a non-Schengen country and return to the Schengen area, you will need a multiple-entry visa. Cyprus, Ireland, and the United Kingdom are EU members, but they are not part of the Schengen Area while EU members Bulgaria, Croatia and Romania are in the process of joining the Schengen Area. To add confusion [[Switzerland]], [[Liechtenstein]], [[Iceland]] and [[Norway]] are not EU members but part of the Schengen area.


===Customs===
Countries in the [[European Union]] maintain similar customs controls. They form a customs union and you usually do not need to pass through customs when travelling between EU countries. There are still some goods that need handling at customs, or special permits, etc., also travelling inside the EU, and the customs may do checks not only at the border. Check details if you have a pet, arms, exceptional quantities of alcohol, or similar.

Note the difference between EU countries and Schengen countries. Between what countries you have to pass through customs does not depend on where you have to go through immigration controls or vice versa.

You are legally allowed to bring through the EU border limited amounts of tobacco (exact numbers depend on your arrival country) and 1 litre of spirits (above 22% alcohol) or 2 litres of alcohol (e.g. sparkling wine below 22% alcohol) and 4 litres of non-sparkling wine and 16 litres of beer. If you are below 17 years old it's half of these amounts or nothing at all.

Countries not in the EU maintain their own customs policies.

===By plane===
The largest air travel hubs in Europe are, in order, '''[[London]]''' (LON: [[LCY]], [[Heathrow Airport|LHR]], [[Gatwick Airport|LGW]], [[Stansted Airport|STN]], [[LTN]], [[SEN]]), '''[[Frankfurt]]''' ({{IATA|FRA}}), '''[[Paris]]''' ({{IATA|CDG}}, {{IATA|ORY}}), '''[[Madrid]]''' ([[Madrid–Barajas Airport|MAD]]), and '''[[Amsterdam]]''' ([[Amsterdam Airport Schiphol|AMS]]), which in turn have connections to practically everywhere in Europe. However, nearly every European capital and many other major cities have direct long-distance flights to at least some destinations. Other, smaller airports can make sense for specific connections: for example, '''[[Vienna]]''' ([[Vienna International Airport|VIE]]) has a very good network of flights to the [[Middle East]] and Eastern Europe, while '''[[Helsinki#By plane|Helsinki]]''' ({{IATA|HEL}}) is the geographically closest place to transfer if coming in from [[East Asia]]. If coming from North America, there is an abundance of cheap flights from the United States and Canada that connect in '''[[Reykjavík]]''' ({{IATA|KEF}}) to virtually any major city in northern and western Europe.

Depending on your final destination it might make sense to avoid the last connection, or rather replace it with a train-ride, as many airports are connected to the train-network (sometimes directly to high-speed lines) and some airlines offer tickets for both train and plane in cooperation with a railway company (which often works out to be a steep discount) (see: [[rail air alliances]]). However due to the quirky nature of airline-pricing the exact opposite might be true as well, meaning that a &quot;longer&quot; flight might actually end up being cheaper. As everywhere: ''caveat emptor!''

===By train===
The '''[[Trans-Siberian Railway]]''' from [[Beijing]] and [[Vladivostok]] to [[Moscow]] is a classic rail journey. The '''[[Silk Road|Historic Silk Road]]''' is becoming increasingly popular with adventurers trying to beat down a new path after the finalized construction of a railway link between [[Kazakhstan]] and [[China]]. The [[Almaty]]–[[Urumqi]] service runs twice per week, and Moscow is easily reached from Almaty by train. Other options include several connections from the Middle East offered by [http://en.tcdd.gov.tr ''Turkish Railways'' (TCDD)]. There are weekly services from [[Tehran]] in [[Iran]] to [[Istanbul]] via [[Ankara]], but the services from [[Syria]] and [[Iraq]] have been suspended, hopefully temporarily, due to the ongoing armed conflicts in those countries. For information on how to get from Istanbul to many other points in Europe by train see our itinerary on the [[Orient Express]].


===By ship===
It is still possible, but expensive, to do the classic transatlantic voyage between the United Kingdom and the United States. The easiest option is by the historic, and only remaining [[ocean liners|ocean liner]] operator, [http://www.cunard.com/ Cunard Line], which sails around 10 times per year in each direction, but expect to pay USD1,000–2,000 for the cheapest tickets on the 6-day voyage between Southampton and New York. If your pockets are not deep enough, your options of crossing the North Atlantic without flying are pretty much limited to [[freighter travel]] and [[Hitchhiking boats|&quot;hitchhiking&quot; with a private boat]].

Most major cruise ships that ply the waters of Europe during summer (June–September) also do cruises in [[Latin America]] and [[Southeast Asia]] for the rest of the year. That means those ships have a transatlantic journey twice per year, at low prices considering the length of the trip (at least a week). These are often called ''positioning cruises''. [http://www.cruisenetwork.com/msc-transatlantic-cruise.jsp MSC] has several ships from the [[Caribbean]] to Europe at April and May.

There are several lines [[Ferries in the Mediterranean|crossing the Mediterranean]], the main ports of call in North Africa are [[Tangier]] in [[Morocco]] and [[Tunis]] in [[Tunisia]]. If you're time rich, but otherwise poor, it may be possible to [[Hitchhiking boats|&quot;hitchhike&quot; a private boat]] as well.

==Get around==
There are virtually no border controls between countries that have signed and implemented the '''[[w:Visa policy in the European Union|Schengen Agreement]]''', except under special circumstances during major events. Likewise, a visa granted for any Schengen country is valid in all other Schengen countries.  Be careful: not all European Union countries are Schengen countries, and not all Schengen countries are members of the EU.  See the [[#Countries|table above]] for the current list.
[[File:Baarle-Nassau frontière café.jpg|thumb|255x255px|A café that straddles the border between the Netherlands and Belgium.]]
Since 2015, the '''free mobility''' within the European Union '''has been disrupted''' somewhat by the large number of refugees entering the area. Some borders have been closed (at least partly) and traffic at some is much less smooth than normal. Identification documents are now being asked for at some border crossings. Expect delays at international borders.

Airports in Europe are divided into &quot;Schengen&quot; and &quot;non-Schengen&quot; sections, which effectively act like &quot;domestic&quot; and &quot;international&quot; sections elsewhere.  If you are flying from outside Europe into one Schengen country and continuing to another, you will clear passport control in the first country and then continue to your destination with no further checks. However, if travelling between an EU Schengen country and a non-EU Schengen country, ''customs controls are still in place''.

Travel between a Schengen country and a non-Schengen country will entail the normal border checks. Regardless of whether you are travelling within the Schengen Area, at some ports and airports, staff will still insist on seeing your ID card or passport (this may now also occur at land borders, particularly Sweden, Denmark and Switzerland).

As an example of the practical implications on the traveller:
*Travel from Germany to France (both EU, both Schengen): no controls
*Travel from Germany to Switzerland (both Schengen, Switzerland ''not'' in EU): customs checks, but no immigration control
*Travel from France to the United Kingdom (both EU, UK ''not'' in Schengen): immigration control, but no customs check. This will likely change if the UK leaves the EU as expected in 2019.
*Travel from Switzerland to the United Kingdom: immigration ''and'' customs checks
Citizens of EEA/Schengen countries never require visas or permits for a stay of any length in any other EEA/Schengen country for any purpose. The only remaining exception is the employment of Croatian workers in some countries.


===By train===
{{main|Rail travel in Europe}}
[[File:BruxellesMidi ICE Thalys.JPG|thumb|European high-speed trains in [[Brussels]]]]

Europe, and particularly Western and Central Europe, has trains which are fast, efficient, and cost-competitive with flying. [[High speed rail|High-speed trains]] like the Italian Frecciarossa, the French TGV, the German ICE, the Spanish AVE and the cross-border Eurostar and Thalys services speed along at up to 320&amp;nbsp;km/h (200&amp;nbsp;mph) and, when taking into account travel time to the airport and back, are often faster than taking the plane.  The flip side is that tickets bought on the spot can be expensive, although there are good discounts available if you book in advance or take advantage of various deals. Roughly speaking,  European high-speed rail tickets work similar to airline tickets with the best offers for non-refundable tickets on low demand routes and times and high prices for &quot;last minute&quot;.

If you want flexibility without spending an arm and a leg, various passes can be a good deal. In particular, the [[Inter Rail]] (for Europeans) and [[Eurail]] (for everybody else) passes offer good value if you plan on traveling extensively around Europe (or even a single region) and want more flexibility than cheap plane (or some advance purchase train) tickets can offer. Sometimes individual railroads offer one-off passes for their country, but they are often seasonal and/or only announced on short notice.

The most extensive and most reliable train travel planner for all of Europe is the one of the German railways (''Deutsche Bahn'', DB), which can be found [http://reiseauskunft.bahn.de/bin/query.exe/en here] in English.

As most long-distance trains and almost all high-speed trains are powered electrically, and through economies of scale even in diesel-trains, trains are &quot;greener&quot; than cars and a lot &quot;greener&quot; than planes. How trains fare compared to buses depends mostly on three factors: the fuel (if electric, then how the electricity is generated), the occupancy and road congestion (congested roads make buses inefficient). The most fuel-efficient train that operates in Europe, DB's ICE3, consumes the equivalent of 0.3 litres of petrol in electricity per seat per {{km|100}}. If you are a proponent of [[ecotourism]] the website of Deutsche Bahn offers a CO&lt;sub&gt;2&lt;/sub&gt; emission calculation tool to help you calculate the carbon footprint for your trip.

Most large cities in Europe have an extensive [[urban rail]] network that is usually the fastest way around town.

===By plane===
{{infobox|EU Passenger Rights|[http://ec.europa.eu/transport/themes/passengers/air_en European Union (EU) Regulation 261/2004 of 17 February 2005] gives certain rights to passenger on all flights, scheduled or chartered and flights provided as part of a package holiday. It only applies to passengers either flying from an EU airport (to any destination) by any carrier, or from a non-EU airport to an EU airport on an EU carrier. It is the carrier that operates the flight that is considered.

'''Denied boarding'''

''If'' you have a valid ticket, a confirmed reservation, and checked in by the deadline given to you by the airline, then you are entitled to a compensation, which is:

* '''{{EUR|250}}''' if the flight is '''shorter than 1500 km'''
:* but '''only {{EUR|125}}''' if it is delayed '''less than 2 hours'''
* '''{{EUR|400}}''' if the flight is '''between 1500 km and 3500 km'''
:* but '''only {{EUR|200}}''' if it is delayed '''less than 3 hours'''
* '''{{EUR|600}}''' if the flight is '''longer than 3500 km'''
:* but '''only {{EUR|300}}''' if it is delayed '''less than 4 hours'''

* '''and''' a refund of your ticket (with a free flight back to your initial point of departure, when relevant)
* '''or''' alternative transport to your final destination.

The airline also have to cover the following expenses:


* two telephone calls or emails, telexes or faxes
* meals and refreshments in reasonable relation to the waiting time
* hotel accommodation if you are delayed overnight.

Usually they will give you a prepaid phone card, and vouchers for a restaurant and a hotel.

'''Delayed flight'''

If your flight is delayed 3 hours or more you are entitled to compensation: {{EUR|250}} (flights of {{km|1500}} or less), {{EUR|400}} (flights of more than {{km|1500}} within the EU and all other flights between {{km|1500 and 3500}}), {{EUR|600}} (flights of more than {{km|3500}}).

If your flight is delayed 5 hours or longer you get a refund of your ticket (with a free flight back to your initial point of departure, when relevant).

'''Luggage'''

If your checked-in luggage is lost, damaged or delayed, the airline is liable and must compensate you by up to {{EUR|1300}}. You have to claim compensation in writing to the airline within 7 days (lost or damaged luggage) or within 21 days of receiving delayed luggage. If the damaged luggage had a defect not caused by the airline, you do ''not'' receive compensation.
}}

All flights within and from the European Union limit '''liquids, gels and creams''' in hand baggage to 100 ml/container, carried in a transparent, zip-lock plastic bag (1 l or less). The bag must be presented during security checks and only one bag per passenger is permitted.

====Discount airlines====
Dozens of budget airlines allow cheap travel around Europe, sometimes cheaper than the train or even bus fares for the same journey, however &quot;legacy&quot; airlines  (or their subsidiaries) can be a better deal when you have luggage.  The cheapest flights are often offered by low cost airlines such as Eurowings, EasyJet, Norwegian, Ryanair, Transavia, Vueling and WizzAir. All of these flights should be booked on the internet well in advance, otherwise the price advantage may become non-existent. Always compare prices with major carriers like British Airways, Air France-KLM or Lufthansa. Only in very few cases prices are higher than {{EUR|80}} on any airline when booking a month or more ahead of time (except on very long routes, e.g. Dublin–Istanbul). You should also make sure where the airport is, since some low cost airlines name very small airports by the next major city, even if the distance is up to two hours drive by bus (e.g. Ryanair and Wizzair's &quot;Frankfurt&quot;-[[Hahn]], which is not Frankfurt/Main International). Budget airlines tickets include little service; account for fees (e.g. on luggage, snacks, boarding passes and so on) when comparing prices.
====&quot;Holiday charter&quot; airlines====
Many airports throughout central Europe have several airlines that serve warm water destinations around the Mediterranean, particularly [[Palma de Mallorca]] and [[Antalya]]. They are aimed towards outgoing tourists on package deals but almost all of them sell (remaining) tickets &quot;unbundled&quot;. Depending on your plans, particularly if you go &quot;against the flow&quot; (e.g. Heading into a cold weather destination at the beginning of the holiday season) they can offer amazing deals and their luggage fees are usually among the lowest in the business. At some airports they may also be the only airlines on offer besides a lone flight by the flag carrier to its hub.

===By bus===
{{see also|Intercity buses in Europe|Intercity buses in Germany|Intercity buses in France}}
Cheap flights and high speed rail have relegated buses to second or third fiddle in many markets, serving the needs of migrants, secondary routes, or countries with poor rail, such as the Balkans, and sparsely inhabited areas such as the Nordic countries or Russia. However, legal reforms in Germany and later France have allowed bus companies to serve cities that had seen no or hardly any intercity service.


Cooperation between bus companies may be non-existent. Expect to have to check connections locally or separately for every company involved. Systems vary from one country to the next, though the bigger players (e.g. Flixbus, Eurolines, Student Agency) are increasingly active in several countries.

For a long time, buses mostly served package tours, or were chartered for a specific trip. One exception to this was in a sense the European answer to Chinatown buses, companies based in Eastern Europe, the Balkans or Turkey and mostly serving as a means for the diaspora to visit the home of their forebears. While most of those companies still exist doing what they always did, they are today overshadowed by more tourist oriented companies with denser networks and a bigger focus on domestic routes.

'''[http://www.eurolines.com/ Eurolines]''' connects over 500 destinations, covering the whole of Europe and [[Morocco]]. Eurolines buses make very few stops in smaller cities, and are generally only viable for travel between large cities. Eurolines offers several types of [http://www.eurolines-pass.com passes] but each individual journey must be booked in advance of its departure date/time. That means that, depending on availability, you may or may not be able to simply arrive at the bus terminal and board any available bus. The pass works well for travellers who either prefer only to see major cities, or who intend to use the pass in conjunction with local transportation options.&lt;!--the section on Eurolines is too long in comparison to the other operators that get only half a line--&gt;

'''[http://www.touring.de/index.php?id=2&amp;L=1 Touring]''' (German variant of Eurolines), '''[http://nettur.rst.com.pl/11503/ Sindbad] {{dead link|August 2018}}''' (Polish), '''[http://www.linebus.com Linebus] {{dead link|August 2018}}''' (Spanish) and '''[http://www.nationalexpress.com National Express]''' (from the UK) are other options. Newer players include [http://www.flixbus.com Flixbus], [http://www.studentagency.eu/en student agency], [http://www.megabus.com Megabus] and [http://fr.ouibus.com/fr ouibus]. Most of these companies originated in a certain country and still mostly serve that country, but cross border services or domestic services in a third country are becoming increasingly common.

===By ship===
: ''Main articles: [[Baltic Sea ferries]], [[Ferries in the Mediterranean]], [[Ferry routes to Great Britain]]''

The '''Baltic sea''' has several routes running between the major cities ([[Gdańsk]], [[Stockholm]], [[Helsinki]], [[Tallinn]], [[Riga]], etc.) Most ships are very large and on a par with Caribbean cruise liners both in size and service.

In the '''Atlantic''', [http://www.smyril-line.com Smyril Line] is the only company sailing to the rather remote North Atlantic islands of [[Iceland]] and the [[Faroe Islands]]. It sails from [[Denmark]], which also has numerous lines to [[Norway]] and [[Sweden]]. There are also numerous services to Denmark, the [[Benelux]] and even across the Biscay to [[Spain]]. Further south there is a weekly service from [[Portimão]] to the [[Canary Islands]] via the remote volcanic [[Madeira]] island.

There are many [[Ferry routes to Great Britain| ferry routes]] serving the United Kingdom and Ireland, not just between Great Britain and Ireland, but also around the numerous other islands of the archipelago, most extensively in the Western and Northern Isles of [[Scotland]]. From southern [[England]] and the [[Republic of Ireland]], several routes still cross the '''English Channel''' to [[France]] and [[Spain]], despite the opening of the Channel Tunnel. The [[Channel Islands]] are also all connected to one another and to France and England by high-speed catamaran. In the '''North Sea''', services operate from [[Belgium]], [[Denmark]] and the [[Netherlands]] to ports on the east coast of England. The hovercraft has been withdrawn from Cross-Channel service due to  competition from the Channel Tunnel, but there is still a hovercraft service from mainland Britain to the Isle of Wight.


In the '''Mediterranean Sea'''  a large number of ferries and cruise ships operate between [[Spain]], [[Italy]] and southern [[France]], including [[Corsica]], [[Sardinia]] and the [[Balearics]]. And on the Italian peninsula's east coast, ferries ply across the Adriatic sea to [[Albania]], [[Croatia]], [[Montenegro]] and [[Greece]], with [[Bari]] as one major terminal of many.

And finally the '''Black Sea''' has several ferries sailing across its waters, although service can be fairly sketchy at times. [[Poti]], [[Istanbul]] and [[Sevastopol]] are the main ports. Nearly all the Black Sea ports have a ferry going somewhere, but rarely anywhere logical – i.e., often along the same stretch of coast.

There are various ferries on the larger lakes and for crossing rivers. There are several regularly running cruise-lines on the larger rivers like the [[Rhine]], [[Danube]] and the [[Volga Region|Volga]]. Boating excursions within Europe, particularly along the scenic rivers and between many of the islands in the Mediterranean, are an excellent way to combine travel between locations with an adventure along the way. Accommodations range from very basic to extremely luxurious depending upon the company and class of travel selected. Another famous line is the ''[[Hurtigruten]]'' cruise-ferries which sails all along [[Norway]]'s amazing coastline and fjords.

===By car===
{{seealso|Driving in Europe}}
Driving in Europe is expensive – fuel costs around {{EUR|1.30-1.40}} &lt;!-- when? --&gt; per litre in most of the EU, while often cheaper in Russia. Rentals are around two to three times more expensive than in North America. Highway tolls are very common, city centre congestion charges increasingly so, and even parking can work up to {{EUR|50}} per day.

Western Europe for the most part has good road conditions and an extensive and well developed highway network, whereas Eastern Europe is still working hard on the large backlog left from communist days. Arguably some former eastern bloc countries are going overboard with this, neglecting rail and bus networks in the process of being caught in auto euphoria.

Avoid large cities if you are not used to driving in Europe. [[Old towns]] are impossible or difficult to go through by car. If you arrive by car, consider parking in a suburb, and use public transportation – in many places called park and ride (abbreviated P+R). Generally speaking, the more urban focused your itinerary and the richer the countries you're headed to, the more miserable you'll be driving compared to taking trains, urban rail and the occasional bus.

[[Winter driving]] is an issue in northern Europe and the high mountains, and occasionally in the south.

Traffic is right-handed except in [[Britain and Ireland]], [[Malta]], and [[Cyprus]].

====Renting a car====
If you plan to '''rent a car''' to drive around Europe, it often makes sense to check the rates in different countries rather than just hire a car in the country of arrival. The price differences can be substantial for longer rentals, to the extent that it can make sense to adjust your travel plans accordingly, e.g. if you plan on travelling around Scandinavia by car, it will often be much cheaper to fly into Germany and rent a car there. Compared to North America, you should be prepared for smaller, more efficient cars, and most of them have manual transmission, so don't expect an automatic without requesting one when placing your order (and often paying extra). Some rental agencies also have stipulations in their contracts, prohibiting the rental of a car in one country and taking it to some others. It is for example common that a car rented in Germany may not be taken to Poland due to concerns of theft. This is less common the other way round, so if you are planning on visiting both countries by rental car, it might be easier (and cheaper) to rent a car in Poland and drive to Germany with it.


===By bike===
{{seealso|Cycling in Europe}}
[[Cycling]] conditions vary greatly between different countries, between city centres, suburbs and countryside, and between different cities in any one country, so see our individual destination articles. In general terms, Belgium, the Netherlands, and Denmark are better destinations for cyclists than, say, Poland.

The [http://www.eurovelo.org/routes/ European cycle route network] or '''[[EuroVelo cycling routes|EuroVelo]]''' consists of 15 routes linking virtually every country on the continent. Some of these routes are not finished, but plans are to have 60,000&amp;nbsp;km of bike lanes; as of 2019, around 70,000&amp;nbsp;km are in place.

Bike share systems are becoming increasingly common, especially in countries like France or Germany. One of the biggest companies in this emerging business is [http://www.nextbike.de/en Nextbike], which mostly honour memberships in one city for reduced rates in another. Other cities like [[Paris]] have city run systems which only cover one place, but there are often special discount rates for tourists.

===By thumb===
[[Hitchhiking]] is a common way of travelling in some parts of Europe, especially in former eastern bloc countries. It can be a pleasant way to meet lots of people, and to travel without spending too many euros.

In the more eastern countries, you may run into language problems while hitchhiking, especially if you speak only English. It is not advisable to hitchhike in former Yugoslavia, for example between Croatia and Serbia, because you could run into big problems with nationalists. Between Croatia and Slovenia it's usually not a problem. In Moldova and Ukraine, it's better to take a train or bus. In western Europe, especially in the Netherlands and Germany, it can be weary and tedious to hitch-hike.

Another method is hitchhiking through pre-arranged [[ride sharing]]. Although this is not free, the price is usually much lower than even the cheapest bus or train-fare. There are several websites, most of them country-specific and/or catering to a specific language group, but long routes are not at all uncommon and international travellers are increasingly using this form of transport.

==Talk==


Most European languages belong to the '''Indo-European''' language family. They share a common ancestry, and have similar fundamental vocabulary (''father'', ''mother'', numeral words, etc) and grammatical structure. Further grammatical similarities and shared vocabulary have come about by close linguistic contact between European languages, with the influence of Classical Greek and Latin being particularly evident even in non-related ones. They can be broadly divided into the following sub-families:
* Germanic languages &amp;mdash; English, [[German phrasebook|German]], [[Dutch phrasebook|Dutch]], [[Frisian phrasebook|Frisian]] and the Nordic languages ([[Danish phrasebook|Danish]], [[Faroese phrasebook|Faroese]], [[Icelandic phrasebook|Icelandic]], [[Norwegian phrasebook|Norwegian]] and [[Swedish phrasebook|Swedish]])
* Romance languages, which are the descendants of Latin &amp;mdash; national languages [[French phrasebook|French]], [[Castilian Spanish phrasebook|Spanish]], [[Catalan phrasebook|Catalan]], [[Portuguese phrasebook|Portuguese]], [[Italian phrasebook|Italian]] and [[Romanian phrasebook|Romanian]], as well as regional languages such as [[Corsican phrasebook|Corsican]] and [[Galician phrasebook|Galician]].
* Balto-Slavic languages &amp;mdash; are found throughout Central Europe, Eastern Europe and the Balkans; such as the Slavic [[Bulgarian phrasebook|Bulgarian]], [[Russian phrasebook|Russian]], [[Ukrainian phrasebook|Ukrainian]], [[Czech phrasebook|Czech]], [[Polish phrasebook|Polish]], [[Serbian phrasebook|Serbian]], and the Baltic [[Latvian phrasebook|Latvian]] and [[Lithuanian phrasebook|Lithuanian]]
* Celtic languages &amp;mdash; found in the United Kingdom, Ireland, and France, they comprise [[Breton phrasebook|Breton]], Cornish, [[Irish phrasebook|Irish]], [[Manx Gaelic phrasebook|Manx]], [[Scottish Gaelic phrasebook|Scottish Gaelic]] and [[Welsh phrasebook|Welsh]].
* Other Indo-European languages include [[Albanian phrasebook|Albanian]], [[Armenian phrasebook|Armenian]] and [[Greek phrasebook|Greek]].

There are also languages not – or at least not closely – related to the Indo-European languages. The '''Uralic''' language family includes [[Hungarian phrasebook|Hungarian]], [[Finnish phrasebook|Finnish]], [[Estonian phrasebook|Estonian]] and [[Sami phrasebook|Sami]]. '''Turkic''' languages include [[Turkish phrasebook|Turkish]] and [[Azerbaijani phrasebook|Azerbaijani]]. Other exceptions include [[Maltese phrasebook|Maltese]] (a Semitic language), [[Georgian phrasebook|Georgian]] and [[Basque phrasebook|Basque]].

Speaking a Romance language may be of some limited use in Portugal, Spain, France, Italy and Romania where there may be similarities in words and grammar, while the same is true if you speak one of the Slavic languages in the East.

'''English proficiency''' varies greatly across the continent, but tends to increase the further north you get, in the [[Benelux]] and particularly the [[Nordic countries]] almost everyone can communicate in English with varying degrees of fluency. German-speaking areas in the middle also have good levels of proficiency. In the south and east you'll often be out of luck, especially outside major cities and tourist centres, though people working in the tourist industry usually speak at least basic English.

[[Russian phrasebook|Russian]] is still widely studied in [[Belarus]], [[Ukraine]], [[Moldova]], [[Armenia]] and [[Azerbaijan]]. It was widely studied as a second language in Central and Eastern Europe by the generations who lived through the communist era, but has largely been supplanted by English among the younger generations. Countries that were part of the former [[Soviet Union]] have significant Russian speaking minorities.

[[German phrasebook|German]] is also a useful foreign language in Eastern Europe.


The '''Latin alphabet''' stems from Europe, and is used for most European languages, often with some modified or additional letters. The related Cyrillic alphabet is used for Russian, some other Slavic languages and some non-Slavic minority languages spoken in Russia and other parts of the former Soviet Union. Both these alphabets were derived from the Greek alphabet. Other writing systems in use include the Georgian and Armenian alphabets.

==See==
[[File:Colosseum in Rome, Italy - April 2007.jpg|350px|thumb|Colosseum in Rome]]

The all too common concept of trying to &quot;do Europe&quot; is pretty unrealistic, and will most likely, if not ruin your vacation, then at least make it less enjoyable. While you can cross Europe on train in a weekend and fly across it in a few hours, it has more historical sites than any other continent, with more than 400 [[UNESCO World Heritage List|World Heritage Sites]] on the continent and thousands of other sites worth seeing. Instead of running a mad dash through Europe in an attempt to get the ritual photos of you in front of the Colosseum, the Eiffel Tower, Big Ben etc. over and done with, the key is prioritize, pick 2–3 sights you really want to see per week, and plan a route from that. There are likely to be some amazing, world class sights and attractions that you haven't even thought about, somewhere in between two given cities, and finding those will – in all likelihood – be infinitely more rewarding than following the beaten down post card route. Each of the larger cities can entertain a visitor for more than a week, and Europe is certainly worth more than one visit. The classic [[Grand Tour]] took longer by necessity than many modern &quot;Eurotrips&quot;, but you can still learn from the first &quot;tourists&quot;.

===Historical and cultural attractions===
Europe is full of deserted [[archaeological sites]], as well as living [[old towns]]. Structures from '''[[Ancient Greece]]''' are scattered around the eastern Mediterranean, including [[Delphi]], [[Olympia (Greece)|Olympia]], [[Sparta]], [[Ephesus]], [[Lycia]] and of course the '''Parthenon''' in [[Athens]].

The '''[[Roman Empire]]''' left ruins across the continent. [[Rome]] itself has the magnificent '''Colosseum''', '''Pantheon''' and the '''Roman Forum'''. Many Roman ruins can also be found in [[Spain]], such as the remains at [[Merida (Spain)|Merida]], [[Santiponce|Italica]], [[Segovia]], [[Toledo (Spain)|Toledo]] and [[Tarragona]]. With 47 sites, [[Italy]] has the most {{UNESCO}}s of any country in the world, directly followed by Spain with 43. Though notably less, France, (southern and western) Germany and England also have some Roman sites, as have most other regions that were once part of the Roman Empire. Several of those sites are UNESCO world heritage sites as well.

The Umayyid and Abassid Dynasties of the '''Caliphate''' left significant architectural influence in Iberia, with buildings like the [[Granada|Alhambra]] and the [[Córdoba (city, Spain)|Mezquíta de Córdoba]] among the finest examples of Islamic architecture in Europe, if not the world. 

Constantinople's (now [[Istanbul]]'s) most famous landmark, '''Hagia Sofia''', is a testament to the continuity from the Byzantine Empire to the Ottomans. After almost a millennium of being the largest Eastern Orthodox (Christian) cathedral in the world, it was converted in 1453 into one of the world's most impressive mosques.

The '''Ottoman Empire''' left significant influence in Eastern Europe and the Mediterranean, with many buildings and cultures deriving important concepts from them. Many Ottoman-era buildings can be found in places like [[Mostar]], [[Veliko Tarnovo]], [[Belgrade]], [[Crimea]], [[Albania]], and of course Turkey. """


# print(parse_continent(""))

def parse_country(country_name):
    dump = get_one_item(country_name, MAIN_DUMP)
    # def parse_first_layer_region(dump):
    #     region = {}
    #     pattern = r"name=(.+)"
    #     result = re.search(pattern, dump)
    #     region["name"] = result.group(1)
    #     region["names_of_second_layer_region"] = []
    #     # if we don't find items, it mean regionname is list of countries in this region. So we create region with name OTHER
    #     try:
    #         pattern = r"items=(.+)"
    #         result = re.search(pattern, dump)
    #         pattern = r'(.+?)((,\s)|( and\b)|($))'
    #         items = re.findall(pattern, result.group(1))
    #         for item in items:
    #             region["names_of_second_layer_region"].append(item[0])
    #
    #     except Exception as e:
    #         region["items"] = EMPTY_REGION
    #
    #
    #     pattern = r"description=(.+)"
    #     result = re.search(pattern, dump)
    #     region["description"] = result.group(1)
    #
    #     return region

    country = {}
    pattern = r"<title>(.+)</title>"
    result = re.search(pattern, dump)
    country["title"] = result.group(1)


    pattern = r"<id>(.+)</id>"
    result = re.search(pattern, dump)
    country["id"] = result.group(1)

    pattern = r"<text.+>.+((?s:.)+?)(==)"
    result = re.search(pattern, dump)
    country["description"] = result.group(1)

    try:
        pattern = r"(\|(?:\s|)region\d+name(?s:.)+?)(\n\n)"
        regions = re.findall(pattern, dump)
        country["first_layer_region_names"] = []

        if len(regions) == 0:
            country["first_layer_region_names"].append("Other")

        for region in regions:
            pattern = r"name(?:\s|)=(?:\s|)(.+)"
            name = re.search(pattern, region[0])
            country["first_layer_region_names"].append(name.group(1))

    except Exception as e:
        country["first_layer_region_names"].append("Other")
    country["description"] = result.group(1)

    return country

dump = """
<page>
    <title>Italy</title>
    <ns>0</ns>
    <id>15920</id>
    <revision>
      <id>3876000</id>
      <parentid>3873725</parentid>
      <timestamp>2019-11-02T14:34:02Z</timestamp>
      <contributor>
        <ip>94.36.74.241</ip>
      </contributor>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|Italy banner 3 Florence.jpg|caption=A view across beautiful Florence from Piazzale Michelangelo}}
'''[http://www.italia.it/en/home.html Italy]''' ([[Italian phrasebook|Italian]]: ''Italia''), officially the '''Italian Republic''' (''Repubblica italiana''), is a country in Southern Europe, occupying the Italian Peninsula and the Po Valley south of the [[Alps]]. Once the core of the mighty [[Roman Empire]], and the cradle of the [[Medieval and Renaissance Italy|Renaissance]], it is also home to the greatest number of [[UNESCO World Heritage List|UNESCO World Heritage Sites]] in the world, including high art and monuments.

Italy is famous for [[Italian cuisine|its delicious cuisine]], trendy fashions, luxury sports cars and motorcycles, diverse regional cultures and dialects, as well as for its various landscapes from the seas to the Alps and Apennines, which makes reason for its nickname ''Il Bel Paese'' (the Beautiful Country).

==Regions==
{{Regionlist

| regionmap=Italy regions.png
| regiontext=
| regionmapsize=400px

| region1name=[[Northwest Italy]]
| region1color=#71b37b
| region1items=[[Piedmont]], [[Liguria]], [[Lombardy]] and [[Aosta Valley]]
| region1description=Home of the Italian Riviera, including [[Portofino]] and the [[Cinque Terre]]. The [[Alps]] and world-class cities like the industrial capital of Italy ([[Turin]]), its largest port ([[Genoa]]) and the main business hub of the country ([[Milan]]) are near beautiful landscapes like the [[Lake Como]] and [[Lake Maggiore]] area and lesser-known Renaissance treasures like [[Mantova]] and [[Bergamo]].

| region2name=[[Northeast Italy]]
| region2color=#8a84a3
| region2items=[[Emilia-Romagna]], [[Friuli-Venezia Giulia]], [[Trentino-Alto Adige]] and [[Veneto]]
| region2description=From the canals of [[Venice]] to the gastronomic capital [[Bologna]], from impressive mountains such as the [[Dolomites]] and first-class ski resorts like [[Cortina d'Ampezzo]] to the delightful roofscapes of [[Parma]] and [[Verona]], these regions offer much to see and do. German-speaking [[South Tyrol]] and the cosmopolitan city of [[Trieste]] offer a uniquely Central European flair.

| region3name=[[Central Italy]]
| region3color=#d5dc76
| region3items=[[Lazio]], [[Abruzzo]], [[Marche]], [[Tuscany]] and [[Umbria]]
| region3description=This region breathes history and art. [[Rome]] boasts many of the remaining wonders of the Roman Empire and some of the world's best-known landmarks, combined with a vibrant, big-city feel. [[Florence]], cradle of the Renaissance, is [[Tuscany]]'s top attraction, and the magnificent countryside and nearby cities like [[Siena]], [[Pisa]] and [[Lucca]] also offer a rich history and heritage. Abruzzo is dotted with picturesque cities such as [[L'Aquila]], [[Chieti]] and [[Vasto]], as well as [[Perugia]], [[Gubbio]] and [[Assisi]] in Umbria.

| region4name=[[Southern Italy]]
| region4color=#d09440
| region4items=[[Apulia]], [[Basilicata]], [[Calabria]], [[Campania]] and [[Molise]]
| region4description=Bustling [[Naples]], the dramatic ruins of [[Pompeii]] and [[Herculaneum]], the romantic [[Amalfi Coast]] and [[Capri]], laidback [[Apulia]], the stunning beaches of [[Calabria]], and up-and-coming agritourism make the region a great place to explore.

| region5name=[[Sicily]]
| region5color=#d56d76
| region5description=The beautiful island is famous for archaeology, seascape and some of Italy's best cuisine.

| region6name=[[Sardinia]]
| region6color=#b383b3
| region6description=Large, gorgeous island some 250 kilometers west of the Italian coastline offers mountains, beaches and the sea with some of the oldest historical structures dating back to the Nuragic Age.
}}
&lt;br clear=&quot;all&quot;/&gt;
'''[[San Marino]]''' and the '''[[Rome/Vatican|Vatican City]]''' are two microstates surrounded by Italy. As they use the euro, the Italian language and have no [[border crossing|border controls]], they are easy to visit.

==Cities==
[[File:Vue des toits depuis la Sainte-Trinité-des-Monts, Rome, Italy.jpg|250px|thumb|right|Rome (seen from Trinità dei Monti)]]
[[File:Florence bridges.jpg|thumb|250px|right|Florence (River Arno, with Ponte Vecchio in the foreground)]]
There are hundreds of Italian cities. Here are '''nine''' of its most famous:

&lt;!-- '''nine''' Please do not change this list without first discussing your proposed change on the talk page. Cities lists are limited by policy to NINE.--&gt;
*{{marker|type=city|name=[[Rome]]|url=|lat=41.9|long=12.5|wikidata=Q220}} (Italian: ''Roma'') — The Eternal City has shrugged off sacks and fascists, urban planning disasters and traffic snarls and is as impressive to the visitor now as two thousand years ago
*{{marker|type=city|name=[[Bologna]]|url=|lat=44.5075|long=11.351389|wikidata=Q1891}} — one of the world's great university cities that is filled with history, culture, technology and food
*{{marker|type=city|name=[[Florence]]|url=|lat=43.783333|long=11.25|wikidata=Q2044}} (Italian: ''Firenze'') — the Renaissance city known for its architecture and art that had a major impact throughout the world
*{{marker|type=city|name=[[Genoa]]|url=|lat=44.411111|long=8.932778|wikidata=Q1449}} (Italian: ''Genova'') — an important medieval maritime republic; it's a port city with art and architecture
*{{marker|type=city|name=[[Milan]]|url=|lat=45.466667|long=9.183333|wikidata=Q490}} (Italian: ''Milano'') — one of the main fashion cities of the world, but also Italy's most important centre of trade and business
*{{marker|type=city|name=[[Naples]]|url=|lat=40.845|long=14.258333|wikidata=Q2634}} (Italian: ''Napoli'') — one of the oldest cities of the Western world, with a historic city centre that is a UNESCO World Heritage Site
*{{marker|type=city|name=[[Pisa]]|url=|lat=43.716667|long=10.4|wikidata=Q13375}} — one the medieval maritime republics, it is home to the famed Leaning Tower of Pisa
*{{marker|type=city|name=[[Turin]]|url=|lat=45.066667|long=7.7|wikidata=Q495}} (Italian: ''Torino'') — a well-known industrial city, home of FIAT, other automobiles and the aerospace industry. Le Corbusier defined Turin as &quot;the city with the most beautiful natural location in the world&quot;
*{{marker|type=city|name=[[Venice]]|url=|lat=45.4375|long=12.335833|wikidata=Q641}} (Italian: ''Venezia'') — one of the most beautiful cities in Italy, known for its history, art, and of course its world-famous canals
&lt;!-- '''nine''' Please do not change this list without first discussing your proposed change on the talk page. Cities lists are limited by policy to NINE.--&gt;

==Other destinations==

&lt;!-- '''nine''' Please do not change this list without first discussing your proposed change on the talk page. Other destinations lists are limited by policy to NINE.--&gt;
*{{marker|type=vicinity|name=[[Amalfi Coast]]|url=|lat=40.633333|long=14.6|wikidata=Q212214}} (Italian: ''Costiera Amalfitana'') — stunningly beautiful rocky coastline, so popular that private cars are banned in the summer months
*{{marker|type=vicinity|name=[[Capri]]|url=|lat=40.55|long=14.233333|wikidata=Q173292}} — the famed island in the Bay of Naples, which was a favored resort of the Roman emperors
*{{marker|type=vicinity|name=[[Cinque Terre]]|url=|lat=44.119444|long=9.716667|wikidata=Q275639}} — five tiny, scenic, towns strung along the steep vineyard-laced coast of Liguria
*{{marker|type=vicinity|name=[[Alps|Italian Alps]]|url=|lat=46.505556|long=9.330278|wikidata=Q1286}} (Italian: ''Alpi'') — some of the most beautiful mountains in Europe, including Mont Blanc and Mount Rosa
*{{marker|type=vicinity|name=[[Lake Como]]|url=|lat=46|long=9.266667|wikidata=Q15523}} (Italian: ''Lago di Como'') — its atmosphere has been appreciated for its beauty and uniqueness since Roman times
*{{marker|type=vicinity|name=[[Lake Garda]]|url=|lat=45.633333|long=10.666667|wikidata=Q6414}} (Italian: ''Lago di Garda'') — a beautiful lake in Northern Italy surrounded by many small villages
*{{marker|type=vicinity|name=[[Pompeii]]|url=|lat=40.75|long=14.486111|wikidata=Q43332}} and {{marker|type=vicinity|name=[[Herculaneum]]|url=|lat=40.806|long=14.3482|wikidata=Q178813}} (Italian: ''Ercolano'') — two suburbs of Naples covered by an eruption of Mt. Vesuvius in AD 79, now excavated to reveal life as it was in Roman times
*{{marker|type=vicinity|name=[[Taormina]]|url=|lat=37.852222|long=15.291944|wikidata=Q199952}} — a charming hillside town on the east coast of Sicily
*{{marker|type=vicinity|name=[[Vesuvius]]|url=|lat=40.816667|long=14.433333|wikidata=Q524}} (Italian: ''Monte Vesuvio'') — the famous dormant volcano with a stunning view of the Bay of Naples
&lt;!-- '''nine''' Please do not change this list without first discussing your proposed change on the talk page. Other destinations lists are limited by policy to NINE.--&gt;

==Understand==
{{quickbar|location=LocationItaly.png}}
Italy is largely a peninsula situated on the Mediterranean Sea, bordering [[France]], [[Switzerland]], [[Austria]], and [[Slovenia]] in the north. The boot-shaped country is surrounded by the Ligurian Sea, the Sardinian Sea and the Tyrrhenian Sea in the west, the Sicilian and Ionian Sea in the South, and Adriatic Sea in the East. Italian is the official language spoken by the majority of the population, but as you travel throughout the country, you will find there are distinct Italian dialects corresponding to the region you are in. Italy has a diverse landscape, but it is primarily mountainous, with the Alps and the Apennines. Italy has two major islands: [[Sardinia]], off the west coast of Italy, and [[Sicily]], just off the southern tip (the &quot;toe&quot;) of the boot. Italy has a population of around 60 million. The capital is [[Rome]].

===History===
[[File:Pantheon, Rome.jpg|thumb|The Pantheon, a huge Roman temple, which is a symbol of the Roman civilization in Italy.]]

====Prehistory====

There have been humans on the Italian peninsula for at least 200,000 years. The Etruscan civilization lasted from prehistory to the 2nd century BC. The Etruscans flourished in the centre and north of what is now Italy, particularly in areas now represented by northern [[Lazio]], [[Umbria]] and [[Tuscany]]. [[Rome]] was dominated by the Etruscans until the Romans sacked the nearby Etruscan city of Veii in 396 BC. In the 8th and 7th centuries BC, Greek colonies were established in Sicily and the southern part of the Italy and the Etruscan culture rapidly became influenced by that of Greece. This is well illustrated at some excellent Etruscan museums; Etruscan burial sites are also well worth visiting.

====The Roman Empire====
{{see also|Roman Empire|Latin Europe}}

Ancient Rome was at first a small village founded around the 8th century BC. In time, it grew into one of the most powerful empires the world has ever seen, surrounding the whole Mediterranean, extending from the northern coast of [[Africa]] to as far north as the southern part of [[Scotland]]. The Roman Empire greatly influenced Western civilisation. Its steady decline began in the 2nd century AD, with a &quot;crisis&quot; in the 3rd century AD that hit particularly hard, bringing leaders who mostly relied on the military and were often deposed in just a few years of rule. The empire finally broke into two parts in 395 AD: the Western Roman Empire with its capital in [[Rome]], and the Eastern Roman Empire or Byzantine Empire with its capital in [[Istanbul|Constantinople]]. The western part, under attack from the Goths, Vandals, Huns and numerous other groups finally collapsed in the late 5th century AD, leaving the Italian peninsula divided. After this, Rome passed into the so-called ''Dark Ages.'' The city itself was sacked by Saracens in 846. Rome went from a city of 1,000,000 people in the first century AD to barely a dot on the map by the seventh century AD, and the stones of its ancient monuments were removed to build new buildings.

====From independent city states to unification====
{{see also|Medieval and Renaissance Italy}}
Following the fall of the Western Roman Empire, the Italian peninsula was divided into many independent city states, and remained so for the next thousand years.

In the 6th century AD, a Germanic tribe, the Lombards, arrived from the north; hence the present-day northern region of [[Lombardy]]. The balance of power between them and other invaders such as the Byzantines, Arabs, and Muslim Saracens, with the Holy Roman Empire and the Papacy meant that it was not possible to unify Italy, although later arrivals such as the Carolingians and the Hohenstaufens managed to impose some control. Thus Northern Italy was under the tenuous control of dynasties from what is now Germany and many cities vying for independence challenged the rule of both pope and emperor, siding with either against the other from time to time. In the south, the Kingdom of the Two Sicilies, a result of unification of the Kingdom of Sicily with the Kingdom of Naples in 1442, had its capital in Naples. In the north, Italy remained a collection of small independent city states and kingdoms until the 19th century. One of the most influential city states was the Republic of [[Venice]], considered one of the most progressive of its time. The first public opera house opened there in 1637, and for the first time allowed paying members of the general public to enjoy what had been court entertainment reserved for the aristocracy, thus allowing the arts to flourish. Italians turned to strongmen to bring order to the cities, leading to the development of dynasties such as the Medici in [[Florence]]. Their patronage of the arts allowed Florence to become the birthplace of the Renaissance and helped to enable men of genius such as Leonardo da Vinci and Michelangelo to emerge. Rome and its surrounding areas became the Papal States, where the Pope had both religious and political authority.

From 1494 onwards, Italy suffered a series of invasions by the Austrians, the French and the Spanish; the latter ultimately emerged victorious.

After Vasco da Gama sailed the [[Cape Route]] around Africa, and Christopher Columbus (who was from [[Genoa]] but working for the king and queen of Spain) [[Voyages of Columbus|sailed to the Americas]], much of the  Mediterranean commerce — especially with Asia through the Middle East — was displaced, making Italian merchants less important. While foreign empires such as [[Austro-Hungarian Empire|Austria]], France and Spain came to dominate the Italian peninsula, it remained a centre of the fine arts, and was from the 17th to the 19th century the main destination for the [[Grand Tour]] of wealthy young people from Britain and Europe.

The Kingdom of [[Sardinia]] began to unify Italy in 1815. Giuseppe Garibaldi led a drive for unification in southern Italy, while the north wanted to establish a united Italian state under its rule. The northern kingdom successfully challenged the Austrians and established Turin as capital of the newly formed state. In 1866, King Victor Emmanuel II annexed Venice. In 1870, shortly after France abandoned it (because they were preoccupied in a war against [[Prussia]] that would lead to German unification by 1871), Italy's capital was moved to Rome. The Pope lost much of his influence, with his political authority now being confined to the [[Rome/Vatican|Vatican City]], itself a result of a political compromise between the Pope and Benito Mussolini in the 1920s.

====The Kingdom of Italy====
After unification, the Kingdom of Italy occupied parts of Eastern and Northern Africa. This included the occupation of [[Libya]], during which Italy scored a decisive victory over the Ottoman Empire.

At the outbreak of [[World War I]], despite being in alliance with Germany and [[Austro-Hungarian Empire|Austria-Hungary]], Italy refused to participate in the war. Eventually, Italy entered the war, but as allies of the [[United Kingdom]] and [[France]]. As a result of the victory of Italy and its allies, Italy annexed former Austro-Hungarian land. However, Italy was not able to obtain much of what it desired, and this, in addition to the high cost of the war, led to popular discontent. This was manipulated by the nationalists, who evolved into the Fascist movement.

In October 1922, the National Fascist Party, led by Benito Mussolini, a former socialist who was thrown out of the party for his pro-war stance, attempted a coup with its &quot;March on Rome&quot;, which resulted in the King forming an alliance with Mussolini. A pact with Germany (by that time fascist as well) was concluded by Mussolini in 1936, and a second in 1938. During the [[World War II in Europe|Second World War]], Italy was invaded by the Allies in June 1943, leading to the collapse of the fascist regime and the arrest, escape, re-capture and execution of Mussolini. In September 1943, Italy surrendered. However, fighting continued on its territory for the rest of the war, with the allies fighting those Italian fascists who did not surrender, as well as German forces.

====Italian Republic====
In 1946, King Umberto II was forced to abdicate and Italy became a republic after a referendum. In the 1950s, Italy became a member of NATO and allied itself with the United States. The Marshall Plan helped revive the Italian economy which, until the 1960s, enjoyed a period of sustained economic growth. Cities such as Rome returned to being popular tourist destinations, expressed in both American and Italian films such as ''Roman Holiday'' or ''La Dolce Vita''. In 1957, Italy became a founding member of the European Economic Community. Beginning with the ''Wirtschaftswunder'' (German for &quot;economic miracle&quot;) of the 1950s, many Germans invested their new-found wealth in vacations in Italy and Northern Italy has been particularly popular with Germans ever since. Even to the point that the spread of pizza (a specialty from the South) to Northern Italy is said to have originated with German tourists demanding what they thought to be &quot;Italian food&quot;.
[[File:Panorama of Trevi fountain 2015.jpg|alt=|thumb|250x250px|The Trevi Fountain, symbol of 18th century Baroque Italy.]]
From the late 1960s till the late 1980s, however, the country experienced an economic and political crisis. There was a constant fear, inside and outside Italy (particularly in the USA), that the Communist Party, which regularly polled over 20% of the vote, would one day form a government. Many machinations by the parties of the establishment prevented this. Italy suffered terrorism from the right and the left, including the shocking kidnapping and murder of Prime Minister Aldo Moro, who shortly before had forged the &quot;historic compromise&quot; with the Communists. Some attacks thought to have been perpetrated by leftist groups are now known to have originated with right wing groups trying to discredit the Communist Party or with the Mafia. An involvement by the NATO &quot;stay behind&quot; organisation (supposed to function as a guerrilla force in the instance of a Soviet occupation), Gladio, that included many right-wing extremists has been alleged in several cases. This turbulent period is remembered as the Years of Lead, or ''anni di piombo''. 

Since 1992, Italy has faced massive government debt and extensive corruption. Scandals have involved all major parties, but especially the Christian Democrats and the Socialists, which were both dissolved, after having dominated politics since the end of the war. The 1994 elections led to media magnate Silvio Berlusconi's tenure as Prime Minister; his allies were defeated in 1996, but emerged victorious in 2001. They lost the election in 2006, but won again in 2008, and lost in 2013. Berlusconi is a controversial figure inside and outside of Italy, and has found himself in court numerous times. Some people even say his political career began as an attempt to escape legal repercussions through parliamentary immunity. Following the 2018 elections, two populist parties agreed to form a government with a majority of seats in the Chamber of Deputies. This has resulted in an uneasy arrangement, with the anti-establishment ''Movimento Cinque Stelle'' (Five Star Movement) and the far-right ''Lega'' (League) uniting to form an unprecedented populist coalition government.

[[File:Paolo Monti - Servizio fotografico - BEIC 6338550.jpg|thumb|200px|The modern 1960s Pirelli Tower in Milan is often considered a symbol of the new Italy, and of post-war economic growth and reconstruction.]]

===Climate===
The climate of Italy varies and often differs from the stereotypical [[Mediterranean climates|Mediterranean climate]]. Most of Italy has hot, dry summers, with July being the hottest month of the year. Winters are cold and damp in the North, and milder in the South. Conditions on peninsular coastal areas can be very different from the interior's higher ground and valleys, particularly during the winter months when the higher altitudes tend to be cold, wet and snowy. The Alps have a mountain climate, with cool summers and very cold winters.

===Literature===
Non-Guidebooks about Italy or by Italian writers.

* ''Italian Journey'' (original German title: Italienische Reise) by Johann Wolfgang von Goethe; a report on his travels to Italy via [[Innsbruck]] and the [[Brenner Pass]]. He visited [[Lake Garda]], [[Verona]], [[Vicenza]], [[Venice]], [[Bologna]], [[Assisi]], [[Rome]] and [[Alban Hills]], [[Naples]] and [[Sicily]] from 1786–7, published in 1816–7.
* ''The Agony and the Ecstasy'' by Irving Stone &amp;mdash; a biography of Michelangelo that also paints a lovely portrait of Tuscany and Rome.
* ''Brunelleschi's Dome: How a Renaissance Genius Reinvented Architecture'' by Ross King &amp;mdash; a compelling story of one of the greatest structural engineering achievements of the Renaissance. The story of the building of the immense dome on top of the basilica in Florence, Italy.
* ''Under the Tuscan Sun'' by Frances Mayes &amp;mdash; an account of a woman who buys and restores a holiday home in Cortona, Italy. Full of local flavour and a true taste of Tuscany.
* ''The Sea and Sardinia'' by D.H. Lawrence &amp;mdash; describes a brief excursion undertaken by Lawrence and Frieda, his wife aka Queen Bee, from Taormina in Sicily to the interior of Sardinia. They visited Cagliari, Mandas, Sorgono and Nuoro. Despite the brevity of his visit, Lawrence distills an essence of the island and its people that is still recognisable today. Also by D.H. Lawrence is ''Etruscan Places'', recording his impressions of [[Cerveteri]], [[Tarquinia]], [[Vulci]] and [[Volterra]].
* ''Italian Neighbours'' and ''A Season with Verona'' by Tim Parks. Two portraits of contemporary life in Italy as seen by an English writer who lived just outside Verona.
* ''Neapolitan Quartet Series'' by Elena Ferrante. A series of novels that explores the intense friendship of two Italian women during the 1950s-1970s. Primarily set in Naples and Florence, this series of novels has received international attention for its depiction of Naples and the rich friendship between these two fictional characters.

===Holidays===

The Italian names are parenthesised.
*'''1 January''': New Year's Day (''Capodanno'')
*'''6 January''': Epiphany (''Epifania'')
*'''March or April according to the Gregorian calendar''': Easter (''Pasqua'') and Easter Monday (''Pasquetta'')
*'''25 April''': Liberation Day (''la Festa della Liberazione'')
*'''1 May''': Labor Day (''la Festa del Lavoro'')
*'''2 June''': Republic Day (''la Festa della Repubblica'')
*'''15 August''': Ferragosto
*'''1 November''': All Saints' Day (''Ognissanti'')
*'''8 December''': Feast of the Immaculate Conception (''Immacolata Concezione'')
*'''25 December''': Christmas (''Natale'')
*'''26 December''': St. Stephen's Day (''Santo Stefano'')

==Get in==
{{infobox|Minimum validity of travel documents|* EU, EEA and Swiss citizens, and some non-EU citizens who are visa-exempt (e.g. New Zealanders and Australians), need only produce a passport which is valid for the entirety of their stay in Italy.
* Other nationals who are required to have a visa (e.g. South Africans) and even some who are not (e.g. travelers from the United States) must have a passport which has '''at least 3 months' validity''' beyond their period of stay in Italy.
* For more information, visit [http://www.esteri.it/MAE/EN/Ministero/Servizi/Stranieri/IngressoeSoggiornoInItalia.htm this webpage of the Ministry of Foreign Affairs of Italy].}}
[[File:Here it is, The Piazza dei Miracoli! Pisa, Italy.jpg|thumb|250px|right|Pisa (the Piazza dei Miracoli, with the cathedral and the leaning tower)]]
[[File:ViewofNaplesBay.jpg|thumb|250px|right|Naples (a view over the city, showing the Vesuvius)]]
[[File:Canal Grande Chiesa della Salute e Dogana dal ponte dell Accademia.jpg|thumb|250px|right|Venice (the grand canal)]]

{{Schengen}}

Foreign military entering Italy under a Status of Forces Agreement do not require a passport and need only show their valid military identification card and travel orders. Their dependents, however, are not exempt from visa requirements.

All '''non'''-EU, EEA or Swiss citizens staying in Italy for 90 days or less have to declare their presence in Italy within 8 days of arrival. If your passport was stamped on arrival ''in Italy'', the stamp counts as such a declaration. Generally, a copy of your hotel registration will suffice if you are staying at a hotel. Otherwise, however, you will have to go to a police office to complete the form ('''dichiarazione di presenza'''). Failing to do so may result in expulsion. Travellers staying longer than 90 days do not need to complete this declaration, but must instead have an appropriate visa and must obtain a residence permit ('''permesso di soggiorno''').

===By plane===
Larger airports are served by the major European airlines. Intercontinental flights mainly arrive in Milan and Rome, the main gateway into the country.

Most mid-range international flights arrive in the following Italian cities:

* [[Rome]] - with two airports: [[Leonardo da Vinci-Fiumicino Airport|Fiumicino]] ({{IATA|FCO}} - Leonardo da Vinci) and Ciampino ({{IATA|CIA}}) for budget airlines
* [[Milan]] - with two airports: Malpensa ({{IATA|MXP}}) and Linate ({{IATA|LIN}}); in addition, [[Bergamo]] ({{IATA|BGY}} - Orio al Serio) is sometimes referred to as &quot;Milan Bergamo&quot;
* [[Bologna]] ({{IATA|BLQ}} – Guglielmo Marconi)
* [[Naples]] ({{IATA|NAP}} - Capodichino)
* [[Pisa]] ({{IATA|PSA}} - Galileo Galilei)
* [[Venice]] ({{IATA|VCE}} – Marco Polo); in addition, Treviso (TSF - Antonio Canova) is sometimes referred to as &quot;Venice Treviso&quot;
* [[Turin]] ({{IATA|TRN}} – Sandro Pertini)
* [[Catania]] ({{IATA|CTA}} - Vincenzo Bellini)
* [[Bari]] ({{IATA|BRI}} - Palese)
* [[Genoa]] ({{IATA|GOA}} - Cristoforo Colombo)

====Prominent airlines in Italy====

*{{listing
| name=Alitalia | alt=AZ | url=http://www.alitalia.com | email=
| address= | lat= | long= | directions=
| phone=+39 892010 | tollfree= | fax=
| hours= | price=
| content=Flag carrier and national airline of Italy. It's part of the SkyTeam alliance, and also codeshares with other carriers outside the alliance. Rome Fiumicino ({{IATA|FCO}}) is the main hub, while Milano Malpensa ({{IATA|MXP}}) has been relegated to a lesser role.
}}
*{{listing
| name=Ryanair | alt=FR| url=http://www.ryanair.com | email=
| address= | lat= | long= | directions=
| phone=+39 899 55 25 89 | tollfree= | fax=
| hours= | price=
| content=Ten bases plus eleven more destinations in Italy.
}}
*{{listing
| name=easyjet | alt=U2 | url=http://www.easyjet.com | email=
| address= | lat= | long= | directions=
| phone=+39 199 201 840 | tollfree= | fax=
| hours= | price=
| content=Two bases and many destinations in Italy.
}}
*{{listing
| name=Wizz Air | alt=W6 | url=http://www.wizzair.com | email=
| address= | lat= | long= | directions=
| phone=+39 899 018 874 | tollfree= | fax=
| hours= | price=
| content=Links some Italian airports with Eastern Europe.
}}
*{{listing
| name=Blu Express | alt=BV  | url=http://www.blu-express.com/en/index.html | email=
| address= | lat= | long= | directions=
| phone=+39 06 98956677 | tollfree= | fax=
| hours= | price=
| content=Mainly focused on domestic routes, links Rome Fiumicino with some international destinations.
}}

===By train===
*From [[Austria]] via [[Vienna]], [[Innsbruck]] and [[Villach]]
*From [[France]] via [[Nice]], [[Lyon]] and [[Paris]]
*From [[Germany]] via [[Munich]]
*From [[Spain]] via [[Barcelona]]
*From [[Switzerland]] via [[Basel]], [[Geneva]] and [[Zürich]]
*From [[Slovenia]] via [[Ljubljana]]  to Opicina, a small village above [[Trieste]] or via [[Nova Gorica]] and a short walk to [[Gorizia]], Italy

If travelling to or from France on the [https://www.thello.com/ Thello] [[sleeper train]], buy sandwiches or other food before the journey.

===By car===
Italy borders on [[France]], [[Austria]], [[Switzerland]] and [[Slovenia]]. All borders are open (without passport/customs checks), but cars can be stopped behind the border for random checks.

=== By bus ===
[http://www.eurolines.it/index.php?option=com_frontpage&amp;Itemid=1&amp;lang=en Eurolines], [http://www.megabus.com Megabus] and [http://www.flixbus.com Flixbus] offer domestic and international routes. There are regular buses between Ljubljana, Slovenian coastal towns and Istria (Croatia) and Trieste (Italy). These services are cheap and from Trieste onward connections with the rest of Italy are plentiful. There is also a bus that goes from Malmö, Sweden via Denmark, Germany and Switzerland and then goes through the country and then back to Sweden.

===By boat===
{{see also|Ferries in the Mediterranean}}

Ferries arrive from [[Greece]], [[Albania]], [[Montenegro]] and [[Croatia]]. Most of them arrive at [[Venice]], [[Ancona]], [[Bari]] and [[Brindisi]].

Regular ferry services connect the island of [[Corsica]] in [[France]] to [[Genoa]], [[Livorno]], [[Civitavecchia]], [[Naples]] and Northern [[Sardinia]]. [[Barcelona]] is connected to [[Civitavecchia]] and to [[Genoa]].

Regular ferry services connect [[Sicily]] and [[Naples]] to [[North Africa]]n harbours.

A hydrofoil service connects [[Pozzallo]] on the south-eastern coast of [[Sicily]] and [[Malta]].

There is a year-round service between [[Trieste]] and Albania and summer services between Trieste and [[Piran]] (Slovenia) and [[Porec]] and [[Rovinj]] in Croatian Istria.  The service between Trieste and Rovinj takes less than 2 hours, which is quicker than the bus service.

==Get around==
[[File:Bologna-SanPetronioPiazzaMaggiore1.jpg|thumb|250px|right|Bologna (the red terracotta roofs and brick towers of the city's skyline)]]

[[File:20110724 Milan Cathedral 5260.jpg|thumb|250px|right|Milan (the Piazza del Duomo, with the city's stunning medieval cathedral)]]
===By train===
:''Main article: [[Rail travel in Italy]]''
[[File:Italy TAV.png|thumb|Italy's [[high speed rail]] network]]
Trains in Italy are generally a good value, frequent, and of uneven reliability. On some [[high speed rail|high-speed routes]] there is a choice between &quot;Nuovo Trasporto Viaggiatori&quot; (privately owned) and &quot;Trenitalia&quot; (state owned). On other routes, either Trenitalia or a regional operator provides the service.

*{{listing
| name=Nuovo Trasporto Viaggiatori | alt= | url=http://www.italotreno.it/EN/Pages/default.aspx | email=
| address= | lat= | long= | directions=
| phone=+39 060708 | tollfree= | fax=
| hours= | price=
| content=NTV's &quot;.Italo&quot; high-speed trains serve major cities. It is a luxurious service, and for some routes and dates, their prices are lower than the competition's.
}}
*{{listing
| name=Trenitalia | alt= | url=http://www.trenitalia.com/tcom-en | email=
| address= | lat= | long= | directions=
| phone=+39 892021 | tollfree= | fax=
| hours= | price=
|wikipedia=|wikidata=|lastedit=2016-09-28| content=Trenitalia runs a wide range of train types: '''[[high-speed trains]]''' (Frecciarossa, Frecciargento, Frecciabianca), '''Intercity''', '''regional trains''' (Regionali, Regionali Veloci) and '''international trains''' (Eurocity, Euronight). &lt;br /&gt;High-speed trains are very comfortable, travelling up to 360km/h and stopping only at major stations and connect only the main cities. They charge a supplement to the standard ticket, which includes the booking fee. Regional trains are the slowest, cheapest and least reliable, stopping at all stations. Intercity trains are somewhere between high-speed and local trains. They are generally reliable.
}}

==== Train types ====

On long-distance trains there are 1st and 2nd classes. A 2nd class ticket costs about 80% the price of a 1st class ticket. On high-speed trains you can also choose between basic, standard and flexible tickets. Basic tickets are of course the cheapest. During commuter hours, on major north-south routes during the holidays, or before and after large political demonstrations, trains on the lower train types are often overcrowded.

Although between Milan and Naples (including Bologna, Florence and Rome), high-speed trains cut travel times in half, on other routes, such as between Rome and Genoa, Naples and Reggio Calabria, Venice and Trieste, they travel on the traditional line, with only marginally shorter travel times compared to Intercity trains.

On long routes, such as [[Milan]] - [[Rome]] or [[Milan]] - [[Reggio di Calabria]], Trenitalia operates special [[sleeper trains|night trains]]: ''Intercity notte''. They depart around 22.00 and arrive in the morning.

==== Getting tickets ====

The lines to buy tickets are often long and slow, so get to the station early. There are efficient, multilingual, touch-screen ticket machines, but the lines for them are often long, too, because there are few of them.

You can also buy tickets online on the [http://trenitalia.com/ Trenitalia website]; you will receive a code (codice di prenotatione (PNR)) that is used to pick up the ticket from a ticket machine in the station (&quot;Self Service&quot;). The site will show the &quot;best&quot; (usually more expensive) connections - you may select to &quot;show all connections&quot; (or &quot;Regional trains&quot;) to see if there are slower but cheaper connections available.

For high-speed and intercity trains you can also choose a ''ticketless'' option. You get a PNR code via email and board the train directly. On board you must tell the conductor your PNR code.

High-speed trains can fill up, so if you're on a tight schedule, buy the tickets in advance. In general, you should buy the tickets ''before'' boarding the train. Fines start at €50. If you're running late and have no ticket, it's probably best to talk directly with the conductor (''il controllore'' or ''il capotreno'') outside the train before boarding.

'''Trenitalia Pass''': you buy a number of days of travel to be used within 2 months, however you still have to pay a supplement on the compulsory reservation services, i.e. TBiz, Eurostar Italia, and Intercity which will be €5-25, depending on the train type. Details are on the [http://www.trenitalia.com/tcom-en Trenitalia] website, and also on the [https://www.internationalrail.com/A846-trenitalia International Rail website].

==== Rules ====

You '''must''' validate the ticket before boarding most trains, by stamping it in one of the white boxes (marked ''Convalida''). Tickets that specify the day and time of travel do not need to be validated.

The cheapest way to travel in a region is to buy a '''zone ticket card'''. A chart displayed near the validating machine tells you how many zones you must ''pay'' between stations. To buy a zone card for the next region, get off the train at the last station, buy the ticket, and board the next train (usually departing in about an hour).

A '''smoking ban''' in public places is in effect in Italy. Smoking on any Italian train is subject to a fine.

===By plane===

The advent of low-cost carriers made domestic air travel cheaper. When booked in advance, plane tickets for long trips are often cheaper than train fares.
Alitalia, Ryanair, Easyjet and Blue Express operate domestic flights while small, new airlines appear and disappear often.

===By car===
:''Main article: [[Driving in Italy]]''

Italy has a well-developed system of motorways (''autostrade'') in the North, while in the South it's a bit worse for quality and extent. Most motorways are toll roads. The ''autostrade'' are marked with green signs, while general highways are marked with blue signs. Speeding on the ''autostrade'' is nowadays less common than in the past. There are automatic systems to punish speeding and hazardous driving. Italian Highway Patrol (''Polizia Stradale'') operates  unmarked cars equipped with advanced speed radars and camera systems.

The tolerated alcohol limit is '''0.50g/L''' in blood, or '''zero''' for drivers under 21 years of age or with less than 3 years of driving experience.

Fuel prices are in line with those in western Europe and more expensive than in North America and Japan. As of December 2016, prices were about €1.65/L for gasoline and €1.53/L for diesel.

Traffic in large Italian cities is heavy and finding a parking spot ranges from a challenging to an impossible enterprise at times. Park your vehicle at a park-and-ride facility or somewhere in the outskirts and use public transport. Be careful with ''Zone a Traffico Limitato'' or [https://www.italybeyondtheobvious.com/dont-mess-with-ztl-zones '''ZTL'''s (Limited Traffic Zones)]. They are restricted areas in the historical centres of many cities, where only authorized vehicles are permitted. Many tourists are fined (about €100) for entering a ZTL unknowingly.

EU licences are automatically recognized. If you don't have an EU driving licence, you need an International Driving Permit in addition to your home driver's license in order to drive. To obtain a  recognition of your driving licence (''adeguamento'' or ''tagliando di riconoscimento'') you will need to pass a medical examination.

All motor vehicles in Italy must have insurance (''assicurazione'') for at least third party liability.

[[File:Palermo-Sicily-Italy - Creative Commons by gnuckx (3492692842).jpg|thumb|250px|right|Palermo (cathedral)]]

===By bus===
====Local====
Buy town bus tickets from corner shops, bus-company offices or automated machines before boarding (on ''some'' systems, tickets ''might'' be bought on-board from an automated machine). Buying tickets from the bus driver is generally not possible.

The payment system for most mass transit in Italy (urban trains, city buses, subway) is based on voluntary payment combined with variable enforcement. Tickets are bought before boarding and validated on an on-board machine; inspectors may board the vehicle to check the passengers' tickets and issue fines to those lacking a validated ticket. The inspectors are generally recognizable by some item displaying the company's logo. When issuing a fine, inspectors are allowed to ask to see your documents, and they have to give some sort of receipt with date, time and location. They are never allowed to directly collect the fine (which generally can be paid at a post office). Assaulting an inspector during his work is a serious offense.

Daily, weekly, monthly and year-round tickets are generally available, in addition to multi-use tickets. These may or may not need to be validated. In almost every city there's a different pricing scheme, so check ticket formulas and availability in advance. For tourists it may be very convenient to buy daily (or multi-day) tickets that allow unlimited travel within a single day or period. Major cities have some type of '''City Card''', a fixed-fee card allowing travel on local public transportation, visits to a number of museums, and discounts in shops, hotels and restaurants.

Check for these possibilities at local tourist offices or on the city's website (which is often of the form www.comune.''cityname''.it as for example www.comune.roma.it).

====Intercity====
Intercity buses used to be a niche market in Italy, but now [http://www.megabus.com Megabus], [http://www.flixbus.com Flixbus] and others have filled the vacuum.

===By thumb===
Hitchhiking in Italy is associated with the 1960s hippies and &quot;on the road&quot; kind of culture. Therefore, it is considered out-dated and useless. You will almost never find Italians hitchhiking unless there's a serious problem with the bus or other means of transportation. Also, it is nowadays common to spot prostitutes by the side of the road pretending to hitchkike to attract clientele so it's advisable to avoid being mistaken for one.

Hitchhiking in the summer in touristy areas works well because you'll get rides from Northern European tourists, and it works well in rural areas as long as there is consistent traffic (because you're still playing the odds), but hitchhiking near large cities or along busy routes is '''frustrating'''. Hitchhiking along expressways and highways is forbidden by law and off the Autostrade, Italians are unlikely to pick up hitchhikers.

===By boat===
Approaching Italy by sea can be a great experience and is a good alternative to traditional onshore “tours”.
A yacht charter to Italy is a fulfilling way to experience the country. Although the yacht charter industry is smaller than one would expect for this incredibly popular tourist destination, there are many reasons to choose a yacht over a more conventional onshore approach. The Italian coast, like the French coast, attracts luxury yacht charters of the highest standards. “Touring” Italy from a private yacht is surprisingly convenient and comfortable. Italy’s dramatic coastline is best appreciated from the sea. You may take a swim whenever you like, and many famous sights are near the seashore. Cruising on a private yacht shields one from the crowds and traffic infesting popular destinations.

Tuscany, the Amalfi Coast, Sardinia and Sicily are the main nautical regions. Each has its own flavor and is rewarding in its own particular way.

==Talk==
{{seealso|Italian phrasebook}}

'''[[Italian phrasebook|Italian]]''' (''italiano'') is the language spoken natively by most Italians. Standard Italian is largely based on the dialect of Tuscan spoken in [[Florence]]. Every region in Italy has a distinct native Italic language in addition to Italian that may or may not be spoken by locals, depending on the area. In Rome or Milan, the spoken language is nowadays usually Italian with some local influence, whereas in rural areas the local language is more common; though people usually speak ''italiano'', too. Even though Italians call the native languages &quot;dialects&quot;, they are separate languages, much like Chinese languages; they even have their own way of writing. Some of these languages also have their own rich literary traditions, the most important ones being Neapolitan, Venetian and Milanese.

In Alto Adige/ [[South Tyrol]], Austro-Bavarian, a dialect of German, is most people's native language (except in the region's capital Bolzano), and German (which is spoken by almost all Austro-Bavarian speakers) is an official language of the autonomous province along with Italian (these regions were part of the Austro-Hungarian Empire until the end of World War I). In northern Italy, there are small pockets of other Romance languages like Ladin, a Rhaeto-Romance language related to [[Switzerland]]'s Romansh. Friulano, another Rhaeto-Romance language, is still spoken by an important minority in the border region near Astria and Slovenia . There are several [[Greek]]-speaking enclaves in the southern regions of [[Calabria]] and [[Puglia]] and there are an estimated 100,000 [[Albanian]] speakers in Apulia, Calabria and Sicily&amp;mdash;some of whom migrated in the Middle Ages and thus speak the rather medieval-sounding [[Arberesh phrasebook|Arberesh]] language. Some regions have additional official languages: German in Alto Adige/ South Tyrol, Slovene and German in Friuli-Venezia Giulia and French in Valle d'Aosta. Slovene is spoken near the Slovenian border and in Gorizia and [[Trieste]]. Most speakers of these minority languages also speak Italian.

'''English''' is spoken by shopkeepers and tour operators in touristic areas. Outside of the tourism industry, you're not guaranteed to find locals who are conversant in English. Before speaking English, begin the conversation in Italian and ask in Italian if the person understands English before switching. English is more common than it used to be, but older people and people in the countryside in particular are unlikely to know much of it. 

The '''Romance''' languages Spanish, French and Portuguese, are not widely spoken but are similar to Italian, so some words will be understood, especially in written form. In the northwesternmost region ([[Valle d'Aosta]]) there are French- and Franco-Provençal-speaking minorities. In neighboring [[Piedmont]], it's not uncommon to find people who speak French as well. Italian is somewhat similar to [[Spanish phrasebook|Spanish]], so if you speak Spanish, locals will generally be able to puzzle you out with some difficulty, and you should also find it easy to pick up Italian.

==See==
There is so much to see in Italy that it is difficult to know where to begin. Virtually every village has something to see.

* '''Etruscan Italy.''' If you have limited time and no potential to travel outside the main cities, then don't miss the amazing collection at the Etruscan Museum at Villa Giulia in Rome. Hiring a car gives access to the painted tombs and museum of [[Tarquinia]] or the enormous burial complex at [[Cerveteri]] and those are just the sites within easy reach of Rome.
[[File:Bikini mosaic.jpg|thumb|right|250px|Roman bikinis. Mosaic from the Villa Romana at [[Piazza Armerina]], Sicily.]]
* '''The Greek influence.''' Well-preserved Greek temples at [[Agrigento]] in the southwest of Sicily and at [[Paestum]], just south of Naples, give a good understanding of the extent of Greek influence on Italy.
* '''Roman ruins.''' From the south, in Sicily, to the north of the country, Italy is full of reminders of the Roman empire. In [[Taormina]], Sicily check out the Roman theatre, with excellent views of Mt. Etna on a clear day. Also in Sicily, don't miss the well-preserved mosaics at [[Piazza Armerina]]. Moving north to just south of Naples, [[Pompeii]] and [[Herculaneum]] were covered in lava by Mt. Vesuvius and, as a result, are well preserved. To [[Rome]] and every street in the center seems to have a few pieces of inscribed Roman stone built into more recent buildings. Don't miss the Colosseum, the Roman Forum, the Aqueducts, the Appian Way, and a dozen or so museums devoted to Roman ruins. Further north, the Roman amphitheatre at [[Verona]] is definitely not to be missed.
[[File:Florence duomo fc01.jpg|thumb|right|250px|Florence's cathedral; bell tower by Giotto to the left and the tower of the Palazzo Vecchio in front]]
* '''Christian Italy.''' The [[Rome/Vatican|Vatican]] is the seat of the Roman Catholic Church. Although inside Rome it has the status of a separate state. Don't miss St Peter's and the Vatican Museum. Rome, itself, has over 900 churches; a large number of these are worth a quick visit. Throughout Italy there is amazing Christian architecture covering the Romanesque (700-1200); Gothic (1100-1450); Renaissance (1400-1600); and ornate Baroque (1600-1830) styles. Although theft of artwork has been a problem, major city churches and cathedrals retain many paintings and sculptures, while others have been moved to city and Church museums. Frescoes and mosaics are everywhere, and quite stunning. Don't just look for churches: in rural areas there are some fascinating monasteries to be discovered. All but the largest churches are usually closed between 12.30 and 15.30.
* '''The Byzantine cities.''' The Byzantines controlled northern Italy until kicked out by the Lombards in 751. [[Venice]] is of course world famous and nearby Chioggia, also in the Lagoon, is a smaller version.  [[Ravenna|Ravenna's churches]] have some incredible mosaics. Visiting Ravenna requires a bit of a detour, but it is well worth it.
* '''The Renaissance.''' Start with a visit to Piazza Michelangelo in [[Florence]] to admire the famous view. Then explore the museums, both inside and outside Florence, that house Renaissance masterpieces. The Renaissance, or Rebirth, (''Rinascimento'' in Italian) lasted from 14th to the 16th centuries and is generally believed to have begun in Florence. The list of famous names is endless: in architecture  Ghiberti (the cathedral's bronze doors), Brunelleschi (the dome), and Giotto (the bell tower). In literature: Dante, Petrarch and Machiavelli. In painting and sculpture: Leonardo da Vinci, Michelangelo, Donatello, Masaccio and Botticelli.
* '''Streets and squares.''' You could visit Italy's cities, never go in a church, museum or Roman ruin, and still have a great time. Just wander around, keeping your eyes open. Apart from the Po and Adige valleys, most of Italy (including the cities) is hilly or mountainous, giving some great views. Look up when walking around to see amazing roof gardens and classical bell towers. In cities such as Rome, note the continued juxtaposition of expensive stores with small workplaces for artisans. Search for interesting food shops and ice cream shops (''gelaterie''). Above all, enjoy the atmosphere.
*  '''Operas'''. If you are interested in famous Italian operas, they are performed in Milan, Verona, Parma, Rome, Venice, Turin, Spoleto, Florence, Palermo and Genoa.
* '''Medieval hilltop towns'''.  Hundreds of these offer a backdrop of scenic landscapes.

===Monuments===
* [[UNESCO World Heritage List#Italy|UNESCO World Heritage]]

===Islands===
[[File:Stromboli und Strombolicchio.JPG|thumb|250px|Stromboli]]
* [[Sicily]]
* [[Sardinia]]
* [[Capri]]
* [[Ischia]]
* [[Elba]]
* [[Procida]]
* [[Aeolian Islands]]
* [[Ustica]]
* [[Pantelleria]]
* [[Aegadi Islands]]
* [[Pelagie Islands]]

===Museums===
[[File:Galleria degli Uffizi Florence.jpg|right|250px|thumb|The Uffizi gallery in Florence, considered one of the most prestigious art museums in the world.]]
Every major city has museums, but some of them have national and international relevance.

These are some of the most important permanent collections.

*  {{see
| name=Uffizi Museum | alt= | url=http://www.polomuseale.firenze.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Florence, is one of the greatest museums in the world and a must-see. Given the great number of visitors, advance ticket reservation is a good idea, to avoid hour-long queues.
}}
*  {{see
| name=Galleria dell'Accademia | alt= | url=http://www.galleriaaccademiafirenze.beniculturali.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=Also in Florence, it is home to Michelangelo's famous statue of David.
}}
*  {{see
| name=Brera Art Gallery | alt= | url=http://www.brera.beniculturali.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Milan is a prestigious museum held in a fine 17th-century palace, which boasts several paintings, including notable ones from the Renaissance era.
}}
*  {{see
| name=The Etruscan Academy Museum of the City of Cortona | alt= | url=http://www.cortonamaec.org/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Cortona, Tuscany.
}}
*  {{see
| name=Egyptian Museum | alt= | url=http://www.museoegizio.org/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Turin, holds the second-largest Egyptian collection in the world, after Egypt's Cairo Museum collection.
}}
*  {{see
| name=The Aquarium | alt= | url=http://www.acquariodigenova.it/en/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Genoa, one of the largest and most beautiful in the world, is in the '''Porto Antico''' (ancient port) in an area completely renewed by architect Renzo Piano in 1992.
}}
*  {{see
| name=Science and Technology Museum | alt= | url=http://www.museoscienza.org/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Milan, one of the largest in Europe, holds collections about boats, airplanes, trains, cars, motorcycles, radio and energy. Has also acquired the Toti submarine, which is open to visitors.
}}
*  {{see
| name=Roman Civilization Museum | alt= | url=http://en.museociviltaromana.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Rome, hold the world's largest collection about ancient Rome and a marvelous reproduction (scale 1:250) of the entire Rome area in 325 AD, the age of Constantine the Great.
}}
*  {{see
| name=National Cinema Museum | alt= | url=http://www.museonazionaledelcinema.org/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Turin, located inside the historic '''Mole Antonelliana''' building, the symbol of the city.
}}
*  {{see
| name=Automobile Museum | alt= | url=http://www.museoauto.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Turin, one of the largest in the world, with a 170-car collection covering the entire history of automobiles.
}}
*  {{see
| name=Capitoline Museums | alt=Musei Capitolini | url=http://www.museoauto.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=In Rome, with large collections of artworks and archaeological findings from the Roman period to the Renaissance. The oldest public art museum in the world.
}}
* '''[http://www.museivaticani.va/content/museivaticani/en.html The Vatican Museums]'''. Not, strictly speaking, in Italy as the [[Rome/Vatican|Vatican]] is a separate territory. Visit the 54 &quot;galleries&quot; of the museums to see the Sistine Chapel, the rooms painted by Raphael, some amazing early maps, and artwork across the centuries, mostly Christian in focus.
* '''The Etruscan Museum at Villa Giulia, Rome'''. Amazing collection of Etruscan art.

==Do==

One of the great things about Italy is that its long thin shape means that when you get fed up with sightseeing, you are often near a beach. In many of the more popular areas, large sections of beach are reserved as paid beaches. In the season they cover almost the entire beach with rows and rows of sunbeds (lettini) and umbrellas (ombrelloni). You have the right to pass through these establishments without being charged to get to the sea, and should be able to walk along the sea in front of them. More affordable are the beaches in [[Calabria]]: Many are free, so you will only need to pay for equipment if you choose to rent any.

South of Rome there are 20&amp;nbsp;km of free beach at the Circeo National Park. This is thanks to '''[http://www.valeriani.com/Mario-Valeriani.html Dr. Mario Valeriani]''', who was in charge of that area after World War II and never gave permits to build anything, in spite of the very generous bribes offered by a multitude of would-be investors and millionaires, as he thought this was a natural marvel that should remain as it was intended. So today we can all enjoy this stretch of nature. You can bring your own chair and sun cover and you will only be charged a parking fee on the main road.

While renting ''lettini'' for the day is not particularly expensive at establishments, they can fill up very quickly. There are some free beaches everywhere: they are easily identifiable by the absence of regimented rows of ''lettini''. They are often crowded: on a Saturday or Sunday in the summer you won’t find an empty stretch of beach anywhere. Most establishments offer full services including entertainment, bar and restaurant, gym classes and kindergarten. Close to urban areas you will never be far from a fish restaurant on the beach or, at the very least, a bar. On the beach, topless women are more or less accepted everywhere but complete nudity is absolutely not accepted anywhere in Italy and it carries a hefty fine and/or arrest.

===Classical music===

Italy was the birthplace of Western opera during the late 16th century and, unsurprisingly, Italy is home to some of the world's most famous opera houses, the best known of which is the Teatro alla Scala in [[Milan]]. The first-ever opera was Jacopo Peri's ''Dafne'' (now lost), which was premiered at the Palazzo Corsi in [[Florence]] in 1598, though the oldest surviving opera that is still regularly performed today is ''L'Orfeo'' by Claudio Monteverdi, which was premiered at the court of [[Mantua]] in 1607. Yet another important city in the history of opera is [[Venice]], in which the first public opera house was built, allowing paying members of the general public access to what was once court entertainment for the aristocracy. In fact, in the early 18th century, Italian opera was the most popular form of entertainment among the aristocracy in every European country except France, and even operas that premiered in non-Italian speaking areas such as London and Vienna were written in Italian. Many Italian composers, such as Monteverdi, Vivaldi, Rossini, Verdi and Puccini continue to be revered by classical music enthusiasts, and some of their pieces have even found their way into modern pop culture. In addition to the locals, many foreign composers such as Handel and Mozart also composed several critically acclaimed Italian operas which continue to enchant audiences to this day.

Besides opera, Italy has also been a key player in the development of other genres of Western classical music. The concerto was first popularised by the Italian composer Arcangelo Corelli during the baroque period, and the symphony can trace its origins to the overtures of Italian baroque opera. Ballet, despite its French name and terminology, and being more commonly associated with France or Russia, actually originated in Italy during the Renaissance. In fact, it was ''de rigueur'' for European composers, regardless of their origin, to spend some time in Italy studying music, and to this day, most terminology used in Western music scores continues to be in Italian.

===Visit the vineyards===
[[File:Vineyards in Chianti Country.jpg|thumb|250px|Wine-growing holding in the Chianti region]]

Italy is famous for its [[wine]]. And its vineyards tend to be in the middle of some beautiful scenery. Taking an organized tour is probably best. Day trips can usually be organized through hotels in major wine areas such as [[Chianti]] or through the local tourism office. There are several companies offering longer tours that include meals and accommodation. A simple web search for “Italian vineyard tours” or “wine tour Italy” will find them. These longer tours emphasise good food, great wine and a high standard of accommodation and are thus expensive.
If you rent a car and want to organize your own trips, a helpful website is that of the [http://www.movimentoturismovino.it/?lang=en Movimento Turismo del Vino]. The Italian page has a link to ''itinerari'' which is not available in English. Even if you don’t read Italian you can still find addresses and opening hours of some interesting wine producers. “Su prenotazione” means &quot;By Appointment Only&quot;.

===Cycling tours===

Several companies offer cycling tours of the Italian countryside. They provide cycles, a guide and transportation for your suitcase, and for you if it all gets a bit too tiring. Tours vary to accommodate different interests. Normally you change city and hotel every day. If you like cycling this is an excellent way of seeing Italy off-the-beaten-track. Search Google, etc. for &quot;Cycle Tours Italy&quot; for companies.

===Sailing===
Sailing is one of the best ways to see the Italian islands such as Sardinia and Sicily. Most charter companies offer options from bareboat to crewed and cabin charter, with all types of the boats.

===Spectator sports===
Italy is sports crazy and as such [[Football in Europe| soccer]], [[Rugby football| Rugby Union]] and several other sports enjoy a devout, if sometimes violent, following. In the 1980s Italy was one of the most notable first adopters of [[American Football]] in Europe, though corruption in the national federation and scandals have greatly reduced interest in this sport since.

==Buy==

===Money===
{{Template:Exchange rate euros}}
{{Euro}}

Italy plans to phase out the one- and two-cent coins in 2018, rounding prices to the nearest five-cent increment.

===Tipping===
Tips (la mancia) are not customary in Italy but are offered when a special service is given or to recognise high quality service. Most restaurants (with the notable exception of Rome) have a price for the service (called ''coperto'') and waiters do not expect a tip, but they will not refuse it, especially if given by foreign customers. In cafés, bars, and pubs it's however not uncommon, on paying the bill, to leave the change saying to the waiter or to the cashier ''tenga il resto'' (&quot;keep the change&quot;). Tip jars near the cash register are becoming widespread, however in public restrooms is often forbidden. Leaving the change is also quite common with taxi drivers, and hotel porters may expect a little something. When using a credit card, it is not possible to add manually an amount to the bill, so it is possible to leave some notes as a tip.

===Shopping===
Italy is an expensive country and its cities are more expensive than suburban and rural places. Usually, Southern Italy is less expensive than Northern Italy, especially for food; this will, of course, vary by location.

Meals can be had from as cheap as €3 (if you are happy with a sandwich [panino] or falafel from a street vendor); restaurant bills range from €10 (a burger with fries or salad and a soft drink from a pub) to €20 (a starter, main course and water from a regular restaurant).

Unless otherwise stated, prices are inclusive of IVA sales tax (same as '''VAT'''), which is 22% for most goods, and 10% in restaurants and hotels. On some products, such as books, IVA is 4%. In practice, you can forget about it since it is universally included in the display price. Non-EU residents are entitled to a VAT refund on purchases of goods that will be taken out of the [[European Union]]. Shops offering this scheme have a '''Tax Free''' sticker outside. Ask for a tax-free voucher before leaving the store. These goods have to be unused when passing the customs checkpoint upon leaving the EU.

While traveling through the countryside, do not rely on '''credit cards'''; in small towns they're accepted by only a few shops and restaurants.

Even during the winter months, it remains common for shops, offices and banks to close for up to 3 hours during the afternoon (often between 12.30 and 15.30). Banks, especially, have short hours with most only being open to the public for about 4 hours in the morning and barely an hour in the afternoon.

=== What to buy ===
Italy is a great place for all forms of shopping. Most cities, villages and towns, are crammed to the brim with many different forms of shops, from glitzy boutiques and huge shopping malls, to tiny art galleries, small food stores, antique dealers and general newsagents.

* '''Food''' is definitely one of the best souvenirs you can get in Italy. There are thousands of different shapes of pasta (not only spaghetti or macaroni). Then every Italian region has its local specialty like [[cheese]], [[wine]], ham, salami, oil and vinegar. Don't forget to buy Nutella. Note that some non-European countries (notably, the United States) have strict rules about what food items can be brought into the country from outside. Cured meats (and other uncooked produce) that you purchase in Italy may not be allowed into your country - check with your embassy or your customs agency to be sure, before you spend a large amount of money on something that may get confiscated.
* Italian '''[[fashion]]''' is renowned worldwide. Many of the world's most famous international brands have their headquarters or were founded in Italy.
[[File:Galleria Vittorio Emanuele II from TownHouse Hotel.jpg|thumb|250px|Galleria Vittorio Emanuele II in Milan]]
:Milan is Italy's fashion and design capital. In the city one can find virtually every major brand in the world, not only Italian, but also French, English, American, Swedish and Spanish. Your main place for la-crème-de-la-crème shopping is the Via Montenapoleone, but the Via della Spiga, Via Manzoni, Via Sant'Andrea and the Corso Vittorio Emanuele are equally luxurious, if less-prominent shopping streets. The Corso Buenos Aires is the place to go for mass-scale or outlet shopping. And, the beautiful Galleria Vittorio Emanuele in the centre and Via Dante boast some designer boutiques, too. Virtually every street in central Milan has clothing stores of some kind.

:However, Rome and Florence, are also fashion centres, and boast being the birthplace of some of the oldest fashion and jewelry houses in Italy. When in Rome, the chic and beautiful Via dei Condotti, leading to the Spanish Steps, will be your primary point of shopping reference, with boutiques, but subsidiary streets such as Via dei Babuino, Via Borgognona, Via Frattina, Via del Corso and the Piazza di Spagna. In Florence, Via de' Tornabuoni is the main high-fashion shopping street, and there you'll find loads of designer brands. However, in both cities, you'll be able to find a plethora of chic boutiques, designer or not, scattered around the centre.

:Prestigious brands such as Armani, Gucci and Prada can of course be found in Italian cities; since their pricing is set internationally, they will likely not be much cheaper than they are in your homeland.

* '''Jewelry and accessory''' shops can be found in abundance in Italy. There are many jewelry and accessory stores which hail from Italy. Vicenza and Valenza are considered the country's jewelry capitals, which are also famous for their silverware and goldware shops. All over Italy, notably Vicenza, Milan, Valenza, Rome, Naples, Florence and Venice, but also several other cities, you can find hundreds of jewelry or silverware boutiques. Apart from the famous ones, there are some great quirky and funky jewelry stores scattered around the country.
* '''Design and furniture''' is something Italy is proudly and justifiably famous for. Excellent quality furniture stores can be found all over, but the best deals are in Milan. Milan contains among the top design rooms and emporia in the world. For the newest design inventions, attend the Fiera di Milano in Rho, where the latest appliances are exhibited. Many Italian cities have great antique furniture stores. So, you can choose between cutting-edge, avant-garde furniture, or old world antiques to buy in this country, which are, by average, of good quality.
* '''Glassware''' is something which Venice makes uniquely but which is spread around the whole of the country. Venice is famously the capital of Murano (not the island), or glassware made in different colours. Here, you can get goblets, crystal chandeliers, candlesticks and decorations made in multi-coloured blown glass, which can be designed in modern, funky arrangements, or the classical style.
* '''Books''' can be found in bookshops in any city. The main book and publishing companies/stores in Italy include Mondadori, Feltrinelli, Hoepli or Rizzoli. Most big bookstores are found in Milan, Turin and nearby Monza, which are the capitals of Italy's publishing trade (Turin was made World Book Capital in 2006), however other cities such as Rome have many book shops. 99% of the books sold are in Italian.
* '''Art''' shops are found throughout Italy, notably in Florence, Rome and Venice. In Florence, the best place to buy art is the Oltrarno, where there are numerous ateliers selling replicas of famous paintings. Usually, depending in what city you're in, you get replicas of notable works of art found there, but also, you can find rare art shops, sculpture shops, or funky, modern/old stores in several cities.

=== How to buy ===
In a small or medium sized shop, it's standard to greet the staff as you enter, not when you approach the counter to pay. A friendly 'Buongiorno' or 'Buonasera' warms the atmosphere. When paying, the staff usually expect you to put coins down on the surface or dish provided, rather than placing money directly into their hands (old money-handling etiquette to avoid messy coin droppings), and they will do the same when giving you your change ('il resto'). This is normal practice and is not intended to be rude.

Haggling is very rare and only ever takes place when dealing with hawkers. They will generally ask for an initial price that is much higher than what they are willing to sell for, and going for the asking price is a sure way to get ripped off. Hawkers often sell counterfeit merchandise (in some cases, very believable counterfeits), and that hoping to buy a Gucci purse for €30 off the street might not be in your best interest.

In all other situations, haggling will get you nowhere. Always be careful about counterfeit merchandise: Italian laws can apply fines up to €3000 to people who buy it (this mostly applies to luxury brand clothing or accessories).

==Eat==
[[File:Troffiette genovese.jpg|thumb|250px|right|Trofie with pesto alla Genovese.]]
[[File:RedMeatWine.jpg|thumb|250px|right|A traditional Italian meal, with beef with sauce and dark red wine.]]
{{seealso|Italian cuisine}}

As one of the world's most renowned culinary traditions, it is unsurprising that Italian cuisine can be very good. That said, there are also many tourist traps that serve overpriced and mediocre food. Finding the right place to eat is therefore important; ask locals for their recommendation if possible, or perhaps even ask your hotel or look at online review sites for recommendations. The downside is that it is rare to find English-speaking waiters in the non-tourist-trap restaurants, so be prepared to have to speak some Italian.

===Cuisine===
Italian food inside of Italy is different than what they call &quot;Italian food&quot; in America. It is truly one of the most diverse in the world, and in any region, or even city and village you go, there are different specialities. For instance, it could be only misleading to say that Northern Italian cuisine is based on hearty, potato and rice-rich meals, Central Italian cuisine is mainly on pastas, roasts and meat, and Southern Italian cuisine on vegetables, pizza, pasta and seafood: there are so many cross-influences that you'd only get confused trying to categorize. And in any case, Italian cuisine, contrary to popular belief, is not just based on pasta and tomato sauce - that's only a tiny snippet of the nation's food; rice, potatoes, lentils, soups and similar meals are very common in some parts of the country. Italian food is based upon so many ingredients and Italians often have very discriminating tastes that may seem strange to visitors.

For instance, a '''sandwich''' stand might sell 4 different types of ham sandwiches that in each case contain ham, mayonnaise, and cheese. The only thing that may be different between the sandwiches is the type of ham or cheese used in them. Rustichella and panzerotti are two examples of sandwiches well-liked by Italians and tourists alike. Also, Italian sandwiches are quite different from the traditional Italian-American “hero”, “submarine”, or “hoagie” sandwich (which by the way mean nothing to any Italian). Rather than large sandwiches with a piling of meat, vegetables, and cheese, sandwiches in Italy are often quite small, very flat (made even more so when they are quickly heated and pressed on a panini grill), and contain a few simple ingredients and often without lettuce or mayonnaise.

The term '''panini''' may be somewhat confusing to travellers from Northern Europe where it has erroneously come to mean a flat, heated sandwich on a grill. In Italy the term is equivalent to &quot;bread rolls&quot; (plural - the singular is '''panino''') which can be simple rolls or sometimes with basic filling. However instead of a sandwich why not try a '''piadina''', which is a flat folded bread with filling, served warm and typical of the coast of Romagna?

Americans will notice that Italian pasta is usually available with a myriad of sauces rather than simply tomato and Alfredo. Also, Italian pasta is often served with much less sauce than in America. This is, in part, because pasta in a restaurant is usually regarded as the first course of a three- or four-course meal, not a meal in itself.

'''Structure of a traditional meal:''' Usually Italian meals for working days are: small breakfast, one-dish lunch, one-dish dinner. Coffee is welcomed at nearly every hour, especially around 10:00 and at the end of a meal. At the weekends and in restaurants (for other occasions), a meal typically consists of: ''antipasto'' (appetizers: marinated vegetables, mixed coldcuts, seafood, etc.), ''primo'' (pasta or rice dish), ''secondo'' (meat or fish course) often with a side dish known as a ''contorno'', and ''dolce'' (dessert).

Like the language and culture, food in Italy '''differs region by region'''. Local ingredients are also very important. In warm Naples, citrus and other fresh fruit play a prominent role in both food and liquor, while in Venice fish is obviously an important traditional ingredient.

'''Breakfast''' in Italy: this is very light, often just a cappuccino or coffee with a pastry (''cappuccino e cornetto'') or a piece of bread and fruit jam. Unless you know for certain otherwise, you should not expect a large breakfast. It is not customary in Italy to eat eggs and bacon and the like at breakfast - just the thought of it is revolting to most Italians. In fact, no salty foods are consumed at breakfast, generally speaking. Additionally, cappuccino is a breakfast drink; ordering one after lunch or dinner is considered strange and considered a typical &quot;tourist thing&quot;. A small '''espresso''' coffee is considered more appropriate for digestion.

Another enjoyable Italian breakfast item is '''cornetto''' (pl. cornetti): a croissant or light pastry often filled with jam, cream or chocolate.

'''Lunch''' is seen as the most important part of the day, so much that Italians have one hour reserved for eating (and in the past, another hour was reserved for napping). All shops close down and resume after the two hour break period. To compensate for this, businesses stay open later than in most other European towns, often until 8 pm. Good luck trying to find a place open during the so-called &quot;pausa pranzo&quot; (lunch break), when visiting a small town, but this is not the case in the city centers of the biggest cities or in shopping malls.

'''Dinner''' (i.e. the evening meal) time varies by region: in the north it is usually around 8 pm (even 7 pm in the homes), but it gets progressively later the further south one goes, up to 10 pm.

In Italy, cuisine is considered a ''kind of art''. Great chefs such as Gualtiero Marchesi and Gianfranco Vissani are seen as half-way between TV stars and magicians. Italians are extremely proud of their culinary tradition and generally love food and talking about it. However, they are not so fond of common preconceptions, such as that Italian food is only pizza and spaghetti. They also have a distaste for &quot;bastardized&quot; versions of their dishes that are popular elsewhere, and many Italians have a hard time believing that the average foreigner can't get even a basic pasta dish &quot;right&quot;.

Do not expect the kind of dedicated, focused service you will find in American restaurants. In Italy this is considered somewhat annoying and people generally prefer to be left alone when consuming their meal. You should expect the waiter to come and check on you after your first course, maybe to order something as second course.

Italy's most famous dishes like pizza or spaghetti are quite lame for some Italians, and eating in different areas can be an interesting opportunity to taste some less well known local specialties. Even for something as simple as pizza there are significant regional variations. That of Naples has a relatively thick, soft crust while that of Rome is considerably thinner and crustier. (Both styles are thin-crust compared to American-style pizza, however.)

When dining out with Italians, read the menu and remember that almost every restaurant has a typical dish and some towns have centuries-old traditions that you are invited to learn. People will appreciate when you ask for local specialties and will gladly advise you.

In Northern Italy, at around 17:00, most bars prepare an '''aperitivo''', especially in cosmopolitan Milan, with a series of plates of nibbles, cheese, olives, meat, bruschetta, etc. This is not considered a meal and it is considered gauche to indulge oneself in eating it as if it were dinner. All this food is typically free to anyone who purchases a drink but it is intended to be a pre-meal snack.

===Specialties===
Cities and regions have their own specialties, including:

*'''Risotto''' – Carnaroli or Arborio or Vialone Nano (etc.) rice that has been sautéed and cooked in a shallow pan with stock. The result is a creamy and hearty dish. Meat, poultry, seafood, vegetables, and cheeses are almost always added depending on the recipe and the locale. Many restaurants, families, towns, and regions will have a signature risotto or at least style of risotto, in addition or in place of a signature pasta dish (risotto alla Milanese is a famous Italian classic). Risotto is a typical dish in Lombardy and Piedmont.
*'''Arancini''' – Balls of rice with tomato sauce, eggs, peas and mozzarella cheese that are deep fried. A Sicilian specialty, they are now common nationwide.
*'''Polenta''' – Yellow cornmeal (yellow grits) that has been cooked with stock. It is normally served either creamy, or allowed to set up and then cut into shapes and fried or roasted. It is common in northern mountain restaurants, usually eaten with deer or boar. In the Veneto region, the best polenta is &quot;polenta bianca&quot;, a special, tasty, and white cornmeal called &quot;biancoperla&quot;.
*'''Gelato''' – This is the Italian word for ice cream. The non-fruit flavors are usually made only with milk. Gelato made with water and without dairy ingredients is also known as sorbetto. It's as fresh as a sorbet, but tastier. There are many flavors, including coffee, chocolate, fruit, and tiramisù. When buying at a gelateria, you have the choice of having it served in a wafer cone or a tub; in northern Italy you'll pay for every single flavour &quot;ball&quot;, and the panna (the milk cream) counts as a flavour; in Rome you can buy a small wafer cone (around 1,80€) a medium one (2,50€) or a large one (3,00€) without limit of flavours, and the panna is free.
*'''Tiramisù''' – Italian cake made with coffee, mascarpone, and ladyfingers (sometimes rum) with cocoa powder on the top. The name means &quot;pick-me-up&quot;.
{| class=&quot;galleryTable noFloat&quot;
|-
| [[File:Tagliatelle Scampi.JPG|thumb|220px|Tagliatelle agli Scampi]]
| [[File:Risotto al persico .JPG|thumb|220px|Risotto al persico]]
| [[File:Polenta con carne.JPG|thumb|220px|Polenta con carne]]
|}

====Pizza====
[[File:Pizza Rucola.JPG|thumb|250px|Pizza Rucola]]
Pizza is a quick and convenient meal. In most cities, '''Pizza al taglio'' shops sell pizza by the gram. When ordering, point to the display or tell the attendant the type of pizza you would like (e.g. pizza margherita, pizza con patate (roasted or french fries), pizza al prosciutto (ham), etc.) and how much (&quot;Vorrei (due fette - two slices) or (due etti - two-tenths of a kilogram) or simply say &quot;di più - more&quot; or &quot;di meno - less, per favore&quot;). They will slice it, warm it in the oven, fold it in half, and wrap it in paper. Other food shops also sell pizza by the slice. Italians consider those a sort of second-class pizza, chosen only when you cannot eat a &quot;real&quot; pizza in a specialized restaurant (pizzeria). Getting your meal on the run can save money—many sandwich shops charge an additional fee if you want to sit to eat your meal. Remember that in many parts of the country pizzas have a thinner base of bread and less cheese than those found outside Italy. The most authentic, original pizza is found in Naples - often containing quite a few ingredients, but most commonly ''pizza margherita'' (tomatoes, fresh basil and fresh mozzarella di bufala) or margherita with prosciutto.

The traditional, round pizza is found in many restaurants and specialized pizza restaurants (pizzerie). It is rare to find a restaurant that serves pizza at lunchtime, however. Do not expect to find the American-style thick-crust pizza in Italy.

Take-away pizzerias (pizzerie da asporto) are becoming ubiquitous in many cities and towns. These are often run by north African immigrants and quality may vary, though they are almost always cheaper than restaurants (€4-5 for a margherita on average, though sometimes as low as €3) and are also open at lunchtime (a few are also open all day long). Some will also serve kebab, which may also vary in quality. Though take-away pizzas are also considered &quot;second-class pizza&quot; by most Italians, they are quite popular among the vast population of university students and they are usually located in residential areas. This is not to be confused with the ever so popular &quot;Pizza al Taglio&quot; shops in Rome. These are a sort of traditional fast food in the Capital City and can be found at every corner. Quality is usually very good and pizza is sold by the weight; you choose the piece of pizza you want, then it is weighed on a scale and priced.
[[File:Rifugio Alpino Boffalora (4).JPG|thumb|180px|[[Cheese]] - Formaggi misti]]

====Cheese and sausages====
In Italy there are nearly 800 types of cheese, including the famous Parmigiano Reggiano and Grana Padano, and over 400 types of sausages.

Open-air markets offer a variety of cheeses and meats and are always open on Saturdays and usually other days, except Sunday, as well.

===Restaurants and bars===
[[File:Rifugio Alpino Boffalora (5).JPG|thumb|right|180px|the menu]]
Italian bars in the center of major cities charge more (typically double whatever the final bill is) if you drink or eat seated at a table outside rather than standing at the bar or taking your order to go. This is because bars are charged a very high tax to place tables and chairs outside, so since most people do not use tables anyway, they had decided long ago to only charge those who do. The further away you are from the center streets, the less this rule is applied. When calling into a bar for a coffee or other drink you first go to the cash register and pay for what you want. You then give the receipt to the barman, who will serve you.

Restaurants always used to charge a small ''coperto'' (cover charge). Some years ago attempts were made to outlaw the practice, with limited success. The rule now seems to be that if you have bread a coperto can be charged but if you specifically say that you don't want bread then no coperto can be levied. This has happened mainly because of backpackers who sat at a table, occupied it for an hour by just ordering a drink or a salad and consuming enormous amounts of bread.

Some restaurants now levy a service charge, but this is far from common. In Italian restaurants a large tip is never expected. The customary 15% of the United States may cause an Italian waiter to drop dead with a heart attack. Just leave a Euro or two and they will be more than happy.

The traditional meal can include (in order) ''antipasto'' (starter of cold seafood, gratinated vegetables or ham and salami), ''primo'' (first dish - pasta or rice dishes), ''secondo'' (second dish - meat or fish dishes), served together with ''contorno'' (mostly vegetables), cheeses/fruit, ''dessert'', coffee, and spirits. Upmarket restaurants usually refuse to make changes to proposed dishes (exceptions warmly granted for babies or people on special diets). Mid-range restaurants are usually more accommodating. For example, a simple pasta with tomato sauce may not be on the menu but a restaurant will nearly always be willing to cook one for kids who turn their noses up at everything else on the menu.

If you are in a large group (say four or more) then it is appreciated if you don't all order a totally different pasta. While the sauces are pre-cooked the pasta is cooked fresh and it is difficult for the restaurant if one person wants '''spaghetti''', another '''fettuccine''', a third '''rigatoni''', a fourth '''penne''' and a fifth '''farfalle''' (butterfly shaped pasta). If you attempt such an order you will invariably be told that you will have a long wait (because the time required for cooking isn't the same for all the types of pasta)!

When pizza is ordered, it is served as a ''primo'' (even if formally it is not considered as such), together with other ''primi''. If you order a pasta or pizza and your friend has a steak you will get your pasta dish, and probably when you've finished eating the steak will arrive. If you want ''primo'' and ''secondo'' dishes to be brought at the same time you have to ask.

Most restaurants do not offer '''diet food'''. The few that do usually write it clearly in menus and even outside.

To avoid cover charges, and if you are on a strict budget, many Italian railway stations have a buffet or self-service restaurant (Termini station in Rome is a great example of the latter). These are reasonably priced and generally the food is of a high quality.

===Gastronomia===
A gastronomia is a kind of self-service restaurant (normally you tell the staff what you want rather than serving yourself) that also offers take-aways. This can give a good opportunity to sample traditional Italian dishes at fairly low cost. These are not buffet restaurants. The food is sold by weight.

==Drink==
Bars, like restaurants, are non-smoking.

Italians enjoy going out during the evenings, so it's common to have a drink in a bar before dinner. It is called '''Aperitivo'''.

Within the last couple years, started by Milan, a lot of bars have started offering fixed-price cocktails at aperitivo hours (18 - 21) with a free, and often a very good, buffet meal. It's now widely considered stylish to have this kind of aperitivo (called '''Happy Hour''') instead of a structured meal before going out to dance or whatever.

===Wine===

Italian [[wine]] is exported all over the world, and names like Barolo, Brunello,  Prosecco, Valpolicella and Chianti are known everywhere. In Italy wine is a substantial topic, a sort of test which can ensure either respect or lack of attention from an entire restaurant staff. Doing your homework ensures that you will get better service, better wine and in the end may even pay less.

{{infobox|DOC, DOCG, IGT?|The ''Denominazione di origine controllata'' certificate restricts above all the grape blend allowed for the wine, and in itself it is not yet a guarantee of quality. The same applies to the stricter ''Denominazione di origine controllata e garantita''. These two denominations are indications of a traditional wine typical of the region, such as [[Chianti]], and often a good partner for local food. But some of the best Italian wines are labeled with the less strict ''Indicazione geografica tipica'' designation, often a sign of a more modern, &quot;international&quot; wine.}}

So before reaching Italy, try to learn a little about the most important wines of the region you are planning to visit. This will greatly increase you enjoyment. Italian cuisine varies greatly from region to region (sometimes also from town to town), and wine reflects this variety.  Italians have a long tradition of matching wines with dishes and often every dish has an appropriate wine. The popular &quot;color rule&quot; (red wines with meat dishes, white wines with fish) can be happily broken when proposed by a ''sommelier'' or when you really know what you are doing: Italy has many strong white wines to serve with meat (a Sicilian or Tuscan ''chardonnay''), as well as delicate red wines for fish (perhaps an Alto Adige ''pinot noir'').

Unlike in the UK, for example, the price mark-ups charged by restaurants for wines on their wine list are not usually excessive, giving you a chance to experiment. In the big cities, there are also many wine bars, where you can taste different wines by the glass, at the same time as eating some delicious snacks. Unlike in many other countries, it is unusual for restaurants to serve wine by the glass.

The ''vino della casa'' (house wine) can be an excellent drinking opportunity in small villages far from towns (especially in Tuscany), where it could be what the patron would really personally drink or could even be the restaurant's own product. It tends to be a safe choice in decent restaurants in cities as well. Vino della casa may come bottled but in lower-priced restaurants it is still just as likely to be available in a carafe of one quarter, one half or one litre. As a general rule, if the restaurant seems honest and not too geared for tourists, the house wine is usually not too bad. That said, some house wines can be dreadful and give you a nasty head the next morning. If it doesn't taste too good it probably won't do you much good, so send it back and order from the wine list.

Italians are justly proud of their wines and foreign wines are rarely served, but many foreign grapes like ''cabernet sauvignon'' and ''chardonnay'' are increasingly being used.

===Beer===
Although wine is a traditional everyday product, beer is very common as well. Beer did not belong to the Italian tradition in the way that wine does, but in the last 30-odd years there has been an explosion of English-style pubs in every town, big or small, with usually a huge selection of any kind of beer, ale, stout and cider, from every country in the world.

Major Italian beers include Peroni and Moretti and these are usually the ones offered by daytime cafes. If you are serious about beer drinking, there are many bars that specialise in serving a wide range of bottled beers (see city articles for more details), as well as Irish pubs and similar establishments. There is an increasing number of micro-breweries around the country. They often are run by local beer enthusiasts turned brewers, running small breweries with a pub attached. Their association is called [http://www.unionbirrai.com/ Unionbirrai].

In the Trieste region it is far more common to drink Slovenian beers and the most popular brands are 'Union' and 'Zlatorog'.  Surprisingly it is often cheaper to buy Slovenian beer in Italy (Trieste) than in Slovenia itself.

===Other drinks===
[[File:Limoncello 2005.jpg|thumb|A cold limoncello on a warm night]]
* '''Limoncello'''.  A liquor made of alcohol, lemon peels, and sugar. Limoncello can be considered a &quot;moonshine&quot; type of product (although usually made with legally obtained alcohol) as every Italian family, especially in the middle-south (near Naples) and southern part of the country, has its own recipe for limoncello. Because lemon trees adapt so well to the Mediterranean climate, and they produce a large amount of fruit continually throughout their long fruit-bearing season, it is not unusual to find many villa's yards filled with lemon trees bending under the weight of their crop. You can make a lot of lemonade, or better yet, brew your own limoncello. It is mainly considered a dessert liqueur, served after a heavy meal (similar to amaretto), and used for different celebrations. The taste can be compared to a very strong and slightly thick lemonade flavor with an alcohol tinge to it. Best served chilled in the freezer in small glasses that have been in the freezer. It is better sipped than treated as a shooter. A derived beverage is '''Crema di Limoncello''', a mix of limoncello and heavy cream, giving it a milder flavour.
*'''Grappa''' is a highly alcoholic drink made by distilling grape skins after the juice has been squeezed from them for winemaking, so you could imagine how it might taste.  If you're going to drink it, then make sure you get a bottle having been distilled multiple times.
*'''San Pellegrino''' is the most famous sparkling water in Italy and considered among the best. It can be found throughout Europe and beyond, but the best place to enjoy its distinct experience is in Italy itself. San Pellegrino can be found in almost every Italian supermarket or grocery store, and is also served in many restaurants. It can be enjoyed at room temperature or chilled.

Limoncello and grappa and other similar drinks are usually served after a meal as an aid to digestion. If you are a good customer restaurants will offer a drink to you free of charge, and may even leave the bottle on your table for you to help yourself. Beware that these are very strong drinks.

===Coffee===
Bars in Italy offer an enormous number of possible permutations for a way of having a cup of coffee. What you won't get, however, is 100 different types of bean; nor will you find &quot;gourmet&quot; coffees. If you like that kind of stuff, better take your own. A bar will make coffee from a commercial blend of beans supplied by just one roaster. There are many companies who supply roast beans and the brand used is usually prominently displayed both inside and outside of the bar.

The following are the most basic preparations of coffee:
* ''Caffè'' or ''Caffè Normale'' or ''Espresso'' – This is the basic unit of coffee, normally consumed after a meal.
* ''Caffè ristretto'' – This has the same amount of coffee, but less water, thus making it stronger.
* ''Caffè lungo'' – This is the basic unit of coffee but additional water is allowed to go through the ground coffee beans in the machine.
* ''Caffè americano'' – This has much more water and is served in a cappuccino cup. It is more like an American breakfast coffee but the quantity is still far less than you would get in the States. It started as an attempt to replicate the type of coffee preferred by occupying American soldiers during World War II, hence its name.

So far so good. But here the permutations begin. For the same price as a normal coffee, you can ask for a dash of milk to be added to any of the above. This is called ''macchiato''. Hence, ''caffè lungo macchiato'' or ''caffè americano macchiato''. But that dash of milk can be either hot (''caldo'') or cold (''freddo''). So you can ask, without the barman batting an eye, for a ''caffè lungo macchiato freddo'' or a ''caffè Americano macchiato caldo''. Any one of these options can also be had decaffeinated. Ask for ''caffè decaffeinato''. The most popular brand of decaffeinated coffee is HAG and it is quite usual to ask for ''caffè HAG'' even if the bar does not use that particular brand.

If you are really in need of a pick-me-up you can ask for a double dose of coffee, or a ''doppio''. You have to specify this when you pay at the cash register and it costs twice as much as a normal coffee. All the above permutations still apply, although a ''caffè doppio ristretto'' may be a bit strange.

Additionally, if you need a shot of alcohol, you can ask for a ''caffè corretto''. This usually involves adding grappa, brandy or sambuca; &quot;corrected&quot; being the Italian expression corresponding to &quot;spiked&quot;. Normally it is only a plain coffee that is corrected but there is no reason why you could not &quot;correct&quot; any of the above combinations.

Then there are coffee drinks with milk, as follows:
* ''Cappuccino'' – Needs no introduction. If you don’t like the froth you can ask for ''cappuccino senza schiuma''.
* ''Caffè latte'' – Often served in a glass, this is a small amount of coffee with the cup/glass filled up with hot milk.
* ''Latte macchiato'' – This is a glass of milk with a dash of coffee in the top. The milk can be hot or cold.

Finally, in the summer you can have ''caffè freddo'', which is basically plain coffee with ice, ''caffè freddo &quot;shakerato&quot;'' (shaked ice coffee) or ''cappuccino freddo'', which is a cold milky coffee without the froth.

This list is by no means exhaustive. With a vivid imagination and a desire to experiment you should be able to find many more permutations. Enjoy!

==Sleep==

In major cities and touristic areas you can find a good variety of accommodations, from world-class brand hotels to family-managed bed &amp; breakfasts and room rentals, but [[hostels]] are really few.
Camping is a good way to save money and camping sites are usually well managed, but especially during summer, managers tend not to accept last-minute groups of young people (given the high chance of problems that such groups of Italian guys tend to cause), so you'd better book in advance. Farmstays are an increasingly popular way to experience Italy, particularly in rural areas of [[Tuscany]], [[Piedmont]], [[Umbria]], [[Abruzzo]], [[Sardinia]] and [[Apulia]]. They provide a great combination of good and healthy food, wonderful sights and not-so-expensive prices. If you prefer self-catering accommodations, it's quite simple to find them on the wonderful [[Amalfi Coast]] or the less commercial and more genuine [[Calabria]] coast.

Hotel star ratings can only be taken as a broad indication of what you will get for your money. There are many marvellous 2-star hotels that you will want to return to every year and many 5-star hotels that you will never want to set foot in again. The star rating, as in all countries, is based on a bureaucratic assessment of the facilities provided and does not necessarily relate to comfort. Often the only difference between a 3-star and 4-star hotel is that the latter offers all meals while the former only offers breakfast.

==Cope==

=== Electricity ===
Italy uses 220 V, 50&amp;nbsp;Hz. Italy has its own electrical [[Electrical systems|plug]] design. The standard &quot;European&quot; two-prong plugs will fit, but grounded (three-prong) plugs from other countries will not. German-type &quot;Schuko&quot; sockets can also be found quite often, especially in the north, and you'll find adapters for that system in virtually all supermarkets. Adapters for other systems (including US plugs) are not that ubiquitous but can be found at airports or in specialised shops.  In private apartments or hotels you will often find all three types of electric sockets in one room so if your device won't fit in one socket keep trying.

If you're using American appliances that were designed for standard US household 110 V, 60&amp;nbsp;Hz current, make sure you get a ''voltage'' adaptor, not just a ''plug'' adaptor.  The higher voltage will damage or destroy your appliance, and could injure or kill you as well.

Power surges and power failures are virtually unknown in Italy, even less so than in the States; the energy, water and gas systems are state-run and very well equipped and maintained since even before WW2; the electrical system is fully updated to the latest tech specs and every household is required to comply when renovating. That includes the remote villages in the South, too.

==Learn==

For English-speakers looking to study in Italy, there are several options. In Rome, Duquesne University, John Cabot, Loyola University Chicago and Temple University maintain campuses. Right outside of Rome the University of Dallas maintains its own campus in Marino. St. John's University has a graduate program in Rome for International Relations and MBA. New York University has a study-abroad program in Florence available even to freshmen and maintains its own campus at Villa La Pietra.

For those who wish to go to local universities, the medium of instruction will generally be Italian. However, usage of English is widespread among those in the academic fields, and many universities will allow those in postgraduate research programmes to publish their papers and complete their thesis in English. Italy's most prestigious university is the '''[http://www.unibo.it University of Bologna]''' (''Università di Bologna''), founded in 1088, which is the oldest university in continuous operation in the world.

It depends on how you want to learn. Are you interested in studying in a huge touristy city like Florence or Rome? Or, are you interested in learning from a small town on the Italian Riviera. The smaller cities have better opportunity to learn Italian because English is spoken less. No matter where you decide, Italy is one of the best spots geographically to travel while you're not studying.

Think about learning what the Italians are best at: food, wine, Italian language, architecture, motors (cars and bikes) and interior design.

==Work==
Work in Italy is not easy to find. Many young adults, especially women, are without a job. Starting salaries in shops, offices, etc. range from €800 to €1,400 a month. There's a huge underground black market though, where you'll find many people working. This doesn't mean working in some kind of obscure crime syndicate: it simply means not being book-regulated. Most &quot;black&quot; workers can be found in small business such as bars, pubs and small shops, or as construction workers. Although this kind of job is illegal (but legal consequences are most on the employer) they're probably the easier thing to find if you're looking for a temporary job.

If you're thinking about establishing a small business be sure to get in contact with the local Chamber of Commerce and an accountant and they will help you to sort out the mess of Italian laws.

==Stay safe==
[[File:Carabinieri a cavallo.jpg|thumb|250px|right|Mounted Carabinieri in Milan.]]
For emergencies, call '''113''' (Polizia di Stato - State Police), '''112''' (Carabinieri - Gendarmerie), '''117''' (Guardia di Finanza - Financial police force), '''115''' (Fire Department), '''118''' (Medical Rescue), '''1515''' (State Forestry Department), '''1530''' (Coast Guard), '''1528''' (Traffic reports).

Italy is a safe country to travel in like most developed countries. There are few incidents of terrorism/serious violence and these episodes have been almost exclusively motivated by internal politics. Almost every major incident is attributed to organized crime or anarchist movements and rarely, if ever, directed at travelers or foreigners.

===Crime===
Violent crime rates in Italy are low compared to most European countries. If you're reasonably careful and use common sense you won't encounter personal safety risks even in the less affluent neighborhoods of large cities. However, petty crime can be a problem for unwary travelers. Pickpockets often work in pairs or teams, occasionally in conjunction with street vendors; take the usual precautions against pickpockets. Instances of rape and robbery are increasing slightly.

You should exercise the usual caution when going out at night alone, although it remains reasonably safe even for single women to walk alone at night. Italians will often offer to accompany female friends back home for safety, even though crime statistics show that sexual violence against women is rare compared to most other Western countries. In a survey by United Nations, 14% of Italian women had experienced attempted rape and 2.3% had experienced rape in their lifetimes.

The mafia, camorra, and other crime syndicates generally operate in southern Italy and not the whole country, and although infamous are usually not involved in petty crime.

Prostitution is rife in the night streets around cities. Prostitution in Italy is not exactly illegal, though authorities are taking a firmer stance against it than before. Brothels are illegal, though, and pimping is a serious offence, considered by the law similar to slavery. In some areas, it is an offence even to stop your car in front of a prostitute although the rows of prostitutes at the side of many roads, particularly in the suburbs, suggest that the law is not enforced. Due to the ambivalent situation regarding prostitution, a lot of prostitutes fall victim to human trafficking. In general, being the client of a prostitute falls in an area of questionable legality and is inadvisable. Being the client of a prostitute under 18 is a criminal offence. It is estimated that the percentage of foreign sex workers in Italy is as high as 90%, and they are often of Eastern European or West African origin. Claims about trafficking vary widely and are difficult to verify. Estimates vary from 7% to 100% of migrant sex workers. The 2009 US State Department report on Human Rights states &quot;In 2008, according to the Ministry of Interior, 4,350 persons were charged with trafficking in persons and pandering.&quot;

There are four types of police forces a tourist might encounter in Italy. The Polizia di Stato (State Police) is the national police force and stationed mostly in the larger towns and cities, and by train stations; they wear blue shirts and grey pants and drive light-blue-painted cars with &quot;POLIZIA&quot; written on the side. The Carabinieri are the national gendarmerie, and are found in the smaller communities, as well as in the cities; they wear very dark blue uniforms with fiery red vertical stripes on their pants and drive similarly colored cars. There is no real distinction between the roles of these two major police forces: both can intervene, investigate, and prosecute in the same way.

The Guardia di Finanza is a police force charged with border controls and fiscal matters; although not a patrolling police force, they sometime aid the other forces in territory control. They dress fully in light grey and drive blue or gray cars with yellow markings. All these police forces are generally professional and trustworthy, corruption being virtually unheard of. Finally, municipalities have local police, with names such as &quot;Polizia municipale&quot; or &quot;Polizia locale&quot; (previously, they were labelled &quot;Vigili urbani&quot;). Their style of dressing varies among the cities, but they will always wear some type of blue uniform with white piping and details, and drive similarly marked cars, which should be easy to spot. These local police forces are not trained for major policing interventions, as in the past they have mostly been treated as traffic police, employed for minor tasks; in the event of major crimes, the Polizia or Carabinieri will be summoned instead.

After leaving a restaurant or other commercial facility, it is possible, though unlikely, that you will be asked to show your bill and your documents to Guardia di Finanza agents. This is perfectly legitimate (they are checking to see if the facility has printed a proper receipt and will thus pay taxes on what was sold).

For all practical matters, including reporting a crime or asking for information, you may ask any police. The Italian Army has also been directly tasked with protecting key locations, including some city landmarks you may want to visit that might be target for terrorist attacks; in case of emergency you can, by all means, ask them for help, but they are not police officers and will have to call the police for you to report a crime and so on.

Police officers in Italy are not authorized to collect fines of any kind and have no authority to ask you for money for any reason (unless you are pulled over in your foreign vehicle and fined, see &quot;Get around/By car&quot; above).

Possession of drugs is always illegal, but it is a criminal offence only above a certain amount.

The main emergency number, handled by the State Police, used to be 113. The medical emergency number is 118, but personnel of the 113 call centre are trained to handle mistakes and will immediately hook you up with actual medical emergency services. Some regions (e.g. Lombardy) have adopted or are adopting the common European emergency number 112.

There are many bars in Italy that cater to tourists and foreigners with &quot;home country&quot; themes, calling themselves such things as &quot;American bars&quot; or &quot;Irish pubs&quot;. In addition to travelers, these bars attract a large number of Italians who, among other reasons, go there specifically to meet travelers and other foreigners. While the motivation for the vast majority of these Italians is simply to have a good time with new friends, there may be one or two petty criminals who loiter in and out of these establishments hoping to take advantage of travelers who are disoriented or drunk. Traveling to these places in groups is a simple solution to this problem. Alternatively, if you are alone, avoid getting drunk!

When entering with a car into a city, avoid restricted, pedestrian-only areas (ZTL) or you could be fined about €100.

As in other countries, there are gangs known for tampering with ATMs by placing &quot;skimmers&quot; in front of the card slot and get a clone of your card. Check the machine carefully and, if unsure, use a different one.

Naples and Rome are the cities with the highest rates of crime towards tourists. These two cities are riddled with beggars and criminals and special care must be taken especially near such locations as the main historical monuments (the Colosseum for example) and the popular gathering places for tourists (Campo de' Fiori Square in Rome for example). It must be stated also that every train station in the country attracts lowlifes, and in general train stations, at night, are not places where one might want to linger too long.

===Tourist scams===

Read up on the legends concerning tourist scams. Most of them occur regularly in bigger cities such as Rome, Milan, or Naples.

Around popular tourist sites, there are people trying to sell cheap souvenirs. They may also carry roses and say they are giving you a gift because they like you but the minute you take their 'gift' they demand money. They are very insistent, pleading and pesty and often the only way to get rid of them is to be plain rude. Do the best you can to not take their &quot;gifts&quot; as they will follow you around asking for money. Simply saying &quot;no&quot; or &quot;vai via&quot; (&quot;go away&quot;) will get them off your back until the next vendor comes up to you.

Another typical encounter throughout tourist spots is the fake 'deaf and dumbs' who enter restaurants or bars, leaving small objects (lighters, keychains, or small toys) on tables with a note asking for financial help. Do not examine their wares; leave them down and they will come back and collect it then leave.

A particular scam is when some plainclothes police will approach you, asking to look for &quot;drug money&quot; or to see your passport. This is a scam to take your money. You can scare them by asking for their ID. Guardia di Finanza (the grey uniformed ones) do customs work.

Another scam involves men approaching you, asking where you are from, and beginning to tie bracelets around your wrists. When they are done they will try to charge you upwards of €20 for each bracelet. If anyone makes any attempt to reach for your hand, retract quickly. If you get trapped, you can refuse to pay, but this may not be wise if there are not many people around. Carry small bills or just change, in your wallet, so if you find yourself cornered to pay for the bracelet, you can convince them that €1 or €2 is all you have.

Yet another scam involves being approached by a man, asking you to help break a large bill - usually €20 or €50. Do not give him your money. The bill he is giving you is fake, but at first glance it might seem real.

The best advice to avoid scams is to get away from anyone you have never seen before who starts talking to you.

When taking a taxi, be sure to remember the license number written on the car door. In seconds, people have had a taxi bill increased by €10 or even more. When giving money to taxi drivers, be careful.
All licensed taxi drivers in Italy until 2012 are actually ethnic Italians, so any unmarked car pretending to be a private taxi driven by a non-Italian such as an Indian or a Hispanic is very likely a scam.

===Racism===

Racially-motivated violence is rare but it does make the news a few times a year.

Italians may assume a person with prominent &quot;foreign&quot; features to be an immigrant and, regrettably, treat him/her with some measure of contempt or condescension.

Tourists can generally expect not to be insulted to their face, but unfortunately casual racism and bigotry is not absent from conversation (especially bar talk, and especially if sports games featuring non-white players are on).

Sports-induced attacks (hooliganism) on foreigners are not unknown, and supporters of foreign teams playing in Italy should exercise extra care not to wear their colors openly on the day of the game, outside of the sports ground.

==Stay healthy==
[[File:Careggi Hospital entry.jpg|thumb|250px|Careggi hospital in Florence.]]
Italian hospitals are public and offer completely free high-standard treatment for EU travellers, although, as anywhere else, you may have to wait quite long to be treated unless you're in a serious condition. Emergency rooms are called &quot;Pronto Soccorso&quot;. Emergency assistance is granted even to non-EU travelers. For non-emergency assistance, non-EU citizens are required to pay out-of-pocket, there is no convention with US health insurances (although some insurance companies might later reimburse these expenses).

Italy has a four-color code of urgency, red being the most immediate (assistance is given without any delay) and white being the lowest (anyone with a red, yellow and green code will pass before you). With a white code, meaning the treatment is not urgent and does not necessitate emergency personnel, you are also required to pay for the full consultation, so do not go to the Pronto Soccorso just to check your knee after last year's fall.

===Water===
While safe to drink, the tap water (''acqua del rubinetto'') in some peninsular parts of Italy can be cloudy with a slight off taste. With the exception of certain towns that use mountain water for their municipal supplies, such as [[Spoleto]], most Italians prefer bottled water, which is served in restaurants.  Make sure you let the waiter/waitress know you want still water (''acqua naturale'' or ''acqua senza gas'') or else you could get  water with either natural gas or with added carbonation (''frizzante'' or ''con gas'').

Rome, in particular, has exceptional pride in the quality of its water.  This goes right back to the building of aqueducts channeling pure mountain water to all the citizens of Rome during Roman times. Don't waste plastic bottles. You can refill your drinking containers and bottles at any of the constant running taps and fountains dotted around the city, safe in the knowledge that you are getting excellent quality cool spring water - try it!

Water in southern Italy might come from desalination plants and sometimes may have a strange taste, due to extended droughts, but it is always perfectly safe as the state runs continuous tests. If in doubt use bottled water. Elsewhere tap water is perfectly drinkable and very well maintained. If not, a &quot;non potabile&quot; warning is posted.

Many towns have fountains with tap water that you can use to refill your container, but do not use water from fountains with an &quot;Acqua non potabile&quot; sign on them.

==Respect==

Italy has a reputation for being a welcoming country and Italians are friendly and courteous, as well as '''very''' used to small talk and interacting with foreigners. Italian society is also much less formal than Northern European or English-speaking ones, especially in terms of introductions (Italians will introduce people to friends only rarely and very casually, not formally, so do not always expect proper introductions). Also, don't expect that the average Italian will speak or even understand English, or that those who do will speak English in your presence: they will revert to Italian almost immediately.

Once a foreigner has mastered the language sufficiently, though, he/she will be required to start using polite forms of speech when addressing older folk, people who are not in their circle of friends, and any office/store clerk they come in contact with. In fact, using familiar verb and pronoun forms is rather rare except among friends, family, and sometimes peers. The Italian polite form of speech form uses the third singular person instead of the second person singular: &quot;Lei&quot; (also the word for &quot;she&quot;, but used for both male and female as a formal way of saying &quot;you&quot;) instead of &quot;tu&quot; (you [familiar]).

Italians greet family and close friends with two light kisses on the cheek. Males do, too. To avoid ending up kissing on the lips, first move to the right (kiss the other person on their left cheek) and then to the left. Other than that, the hand-shaking rules are the same as anywhere else in the western world.

Italians today are no longer the skirt-chasing Romeos described in 1950s movies.

Any other topic is more or less the same as in other Western countries with no special care to be taken or any special do's or don't's.

====Clothing====

Whole essays can be written about the Italians' relationships with clothes. Three of the most important observations:
# Most Italians (especially young ones from the upper and upper-middle social class) are very appearance-conscious; don't be surprised or insulted if you are looked at askance for your 'eccentricity' in not wearing the latest customised jeans or boots.
# It's important not to judge people in return by their choice of clothing. Styles do not necessarily carry the same connotations in Italy that they would in Britain or some other countries. A woman in stilettos, miniskirt and full makeup at eight in the morning is probably just going to work in a bank. Almost all youths lounge about in skin-tight tee-shirts and casually knotted knitwear (and are very perplexed by the response they get when they take their sense of style and grooming to a less 'sophisticated' climate).
# Sometimes, clothing rules are written. To visit a church or religious site you will need to cover yourself up; no bare backs, chests, shoulders and sometimes no knees, either. Sometimes museums and other attractions can also be strict; no bathing costumes, for example. If you want to visit a church or religious site it's a good idea to take something to cover yourself up with; for example a jumper or large scarf. Some churches supply cover-ups, such as sarongs are loaned to men with shorts so that they can modestly conceal their legs. Even where there are no written rules, bare chests and large expanses of sunburnt skin are unacceptable away from beaches or sunbathing areas, whatever the temperature is. It is considered impolite for a man to wear a hat in a Catholic church.

==== Politics====
In the 21st century, politics became polarized between those who supported prime minister Berlusconi and those who opposed him. After his government fell in 2011, this has slowly faded. Still, if you bring in the argument, be prepared for a heated debate. Trust in the political system itself is fading, reflecting in a sharp drop in electoral turnout (which was traditionally high); expect most Italians to talk about politics with hopelessness, when not with anger.

Italians are usually modest about their country's role in the world. It should be easy to talk to people about history and politics without provoking arguments. People will listen to your opinion in a polite way as long as you express yourself politely. Fascism is out of the mainstream of Italian politics and sometimes seen as a blight, due to the dictatorship period (known as ''ventennio fascista''). You'd best avoid such topics. Some older people who lived under Benito Mussolini (the Fascist dictator who was killed by the Resistance) could easily get upset, either because they lost someone to - or fought against - the fascist regime, or because they served in it. There are also some young people who support fascist views and usually such people do not like to talk about them, so simply avoid the topic. April 25 in Italy is the &quot;Liberation Day&quot;, the national celebration of freedom from Nazi-Fascist rule.

On the other hand, communism does not carry the same violent significance for most Italians, though attitudes towards it vary; this is not unlike the situation in Germany, where Nazism is taboo but the communist regime in the East is not. Also, Italy had the largest communist party in the western world (though it had broken with the USSR over the 1968 invasion of Czechoslovakia and by the 1980s, began abandoning Marxism altogether); the traditional communist strongholds were the regions of Emilia-Romagna and Tuscany, where many (especially, but by no means exclusively, the elders) still remember the Party with fondness.

Similarly, in the South, the Mafia could be a sensitive topic, so it is probably wise not to talk about it.

====LGBT rights in Italy====

Gay, lesbian, bisexual, and transgender persons in Italy may face legal challenges not experienced by non-LGBT residents. Both male and female same-sex sexual activity is legal in Italy, but same-sex couples and households headed by same-sex couples are not eligible for the same legal protections available to opposite-sex couples.

Italian opinions have changed and people are now more supportive of LGBT rights, but tend to be more repressive than other European nations. Tolerance of others is part of the doctrine of the Roman Catholic Church, which, at the same time, holds generally negative views of gay sex. Nevertheless, there is a significant liberal tradition, particularly in the North and in Rome. Conservative Italian politicians such as former Prime Minister Silvio Berlusconi have expressed opposition to increasing gay rights. A Eurobarometer survey published in December 2006 showed that 31% of Italians surveyed support same-sex marriage and 24% recognise same-sex couple's right to adopt (EU-wide average 44% and 33%). A 2007 poll found 45% support, 47% opposition and 8% unsure on the question of  support for a civil partnership law for gays. Civil unions for same-sex couples were recognized in 2016, and public opinion on the acceptance of LGBT people as a whole remains fairly positive, with 70-80% of Italians believing homosexuality should be accepted by society. 

While more information can be found on LGBT-specific websites, a brief summary of the situation is as follows: while violence is uncommon against openly gay people, some Italians are disturbed by public displays of affection from same-sex couples and stares are very possible. Some same-sex couples prefer to avoid public attention. As is the case elsewhere, the younger generations tend to be more tolerant than older folks, but assumptions should not be made in either direction.

====Religion====
Although most Italians are nominally Roman Catholic, contemporary Italy is in general a secular society, and most Italians are rather relaxed in their religious observances. Atheism and agnosticism are also not uncommon, particularly in traditionally left-wing areas in Central and Northern Italy. While not all Italians respect Catholic religious traditions, even many atheists do, and as a visitor, you should, especially in the South. 

==Connect==
===Internet access===

====WiFi====
By law all public-access internet points must keep records of web sites viewed by customers, and even the customer's ID: expect to be refused access if you don't provide identification. Hotels providing Internet access are not required to record IDs if the connection is provided in the guest's room, although if the connection is offered in the main public hall then IDs are required.

Publicly available '''wireless access''' without user identification is illegal, so open Wi-Fi hotspots (like the ones you might expect to find in a mall or cafée) all have some form of (generally one-time) registration.

Certain internet activities are illegal. Beside the obvious (child pornography, trading in illegal products like drugs and weapons), copyright infringement is illegal even if no profit is made. However enforcement of copyright laws against P2P users is lax and cease&amp;desist letters from providers are unheard of, ''unless'' using a University's WiFi. Certain websites (mostly related to online gambling and copyrighted material) have been blocked in Italy following court rulings.

====Mobile====

The mobile phone market developed in Italy long before it did in the U.S. or other countries (as early as 1993), so reception is guaranteed in the  whole of the country, including far off the coast, the tallest mountains, and the smallest villages. 3G or HDSPA internet connectivity is available from all major Italian carriers. Beware though that internet plans are generally much more expensive than in other European countries.

Also, contracts often contain little-publicized usage limitations, e.g. a plan that is advertised as 3 GB per month but actually has a daily limit of 100 MB.

Retailers will often fail to mention these limitations and quite often are themselves ignorant that they exist, so it is advisable to double check on the carrier's website.

Also generally speaking, internet plans only include connectivity when under a specific carrier's coverage. When roaming, internet costs can be very high. Coverage of major carriers is widespread, but it would be wise to check whether your carrier covers your area.

===Telephone===
[[File:Pay phones outside Duomo, Milan.jpg|thumb|Pay phones in Milan]]
Both the fixed and mobile phone systems are available throughout Italy.

Telephone numbers of the fixed system used to have separate prefixes (area codes) and a local number. In the 1990s the numbers were unified and nowadays, when calling Italian phones you must '''always dial the full number'''. For example you start numbers for Rome with 06 even if you are calling from Rome. All land line numbers start with 0. Mobile numbers start with 3. Numbers starting with 89 are high-fee services. If you don't know somebody's phone number you can dial a variety of  phone services, the most used being 1240, 892424, 892892, but most of them have high fees.

To call abroad from Italy you have to dial &lt;code&gt;'''00''' + ''country code'' + ''local part''&lt;/code&gt; where the syntax of the ''local part'' depends on the country called.

To call Italy from abroad you have to dial &lt;code&gt;''international prefix'' + '''39''' + ''local part''&lt;/code&gt;.
Unlike calls to most countries, you should ''not'' skip the starting zero of the local part if you are calling an Italian land line.

In case of emergency call the appropriate number from the list below. Such calls are usually free and calls to 112, 113, 115, 118 can be made from payphones for free without the need of inserting coins. 112 (standard emergency number in GSM specification) can be dialed in any case for free from any mobile phone (even if your credit is empty or if you are in an area covered by a different operator)
* ''112'' Carabinieri emergency number - general emergency
* ''113'' Police emergency number - general emergency
* ''114'' Blue Phone emergency number - children-related emergency (especially various forms of violence)
* ''115'' Fire Brigade emergency number
* ''117'' Guardia di Finanza - for customs, commercial and tax issues
* ''118'' Health emergency number - use this if you need an ambulance, otherwise ask for the local Guardia Medica number and they'll send you a doctor.
* ''1515'' State Forestry Department
* ''1518'' Traffic Information
* ''1530'' Coast Guard
* ''803116'' A.C.I. (Italian Automobile Club) This provides assistance if your car breaks down (if you have a rented car then call the number they provide), This is a service provided to subscribers to ACI or to other Automobile Clubs associated to ARC Europe. If you're not associated to any of them you'll be asked to pay a fee (approx. €80).

Always carry with you a note about the address and the number of your embassy.

If you are in an emergency and do not know who to call dial 112 or 113 (out of major towns, better to call '''113''' for English-speaking operators).

A few payphones remain in train stations and airports. Some of them work only with coins, some only with phone cards and just a very few with both coins and phone cards. Only a limited number of payphones (in main airports) directly accept credit cards.
Many companies are shifting their customer service numbers to fixed-rate number (prefix 199). These numbers are at the local rate, no matter where they are called from.

According to national regulations, hotels cannot apply a surcharge on calls made from hotels (as the switchboard service should already be included as a service paid in the room cost) but, to be sure, check it before you use.

Calls between landlines are charged at either the local rate or the national rate depending on the originating and destination area codes; if they are the same then the call will be local rate. Local calls are not free.

====Mobile====
Italians use mobile phones extensively, some might say excessively. The main networks are TIM (Telecom Italia Mobile, part of Telecom Italia, formerly state controlled), Vodafone, Wind, and 3 (only UMTS cellphones).

Best advice is to buy a prepaid SIM card (€10 upwards) and  a cheap mobile phone (€19 upwards) to put it in (if you don't have a cellphone already that you can use). It will be much more practical.

Cellphones from Korea, Japan and North America will not work in Italy unless they are Tri-band.

Nearly all of Italy has GSM, GPRS and UMTS/HDSPA coverage. You need to provide a valid form of identification, such as a passport or other official identity, to be able to purchase a SIM card. Unless you already have one, you will also be required to obtain a ''Codice Fiscale'' (a tax number) - or the vendor may generate one for you from your form of identification. Subscription-based mobile telephony accounts are subject to a government tax, to which ''prepaid'' SIM cards are not subject. Sometimes hotels have mobile phones for customer to borrow or rent.

Call costs vary greatly depending on when, where, from and where to. Each provider offers a complex array of tariffs  and it is nearly impossible to make reliable cost estimates. The cost of calls differs considerably if you call a fixed-line phone or a mobile phone. Usually there is a difference in cost even for incoming calls from abroad. If you can choose, calling the other party's land line could be even 40% cheaper than mobile.

===Post===

If at all possible, wait until you leave Italy before posting postcards, greeting cards and other items to friends and family back home. The Italian post is notorious for being slow, expensive and unreliable. In border towns and cities near the borders with France, Switzerland, Austria and Slovenia it may be best to cross the border to post - postcards from Slovenia to Britain can take just 2 days compared with over a week when posted across the border in Trieste, Italy.

When you do decide to send mail from Italy, there are two services: [https://www.poste.it/ Poste Italiane] (red post boxes, available everywhere) and [https://www.globepostalservice.com Globe Postal Service (GPS)] (yellow post-boxes, available in some shops).

[https://www.poste.it/ Poste Italiane] offices can be found in every town and most villages - look for the ''PT'' symbol. When entering the post office you will usually have to take a ticket and wait for your number to appear on the screen when it's your turn. There will be different tickets for different services but for posting a parcel look for the yellow symbol with the icon of an envelope. Most post offices close at around 1pm or 2pm and only a central post office in most towns will re-open in the late afternoon.

[https://www.globepostalservice.com/ Globe Postal Service (GPS)] sells stamps in tobacco/postcard shops, which also have their dedicated post boxes. [https://www.globepostalservice.com/faq/ Rates] as of September 2018 are: €1.30 within Europe, and €2.50 for international mail. [https://www.globepostalservice.com/faq/ Delivery times] are &quot;slightly longer than national service&quot;, being: Europe: 14 days, international: 18 days. GPS has a feature where one can add videos/photos to a stamp via a QR-code, and allow tracking of the postcard.

{{geo|42.5|12.5|zoom=6}}
{{isPartOf|Europe}}
{{outlinecountry}}
{{related|Ferries in the Mediterranean}}</text>
      <sha1>sgvazo9rs4i6q46ukzavx9tj5ilanfa</sha1>
    </revision>
  </page>
"""
# parse_country(dump)
def parse_cities_list(dump):
    cities = []
    try:
        pattern = r"marker\|type=(\w+)\|name=(.+?)\|wikidata=(.+?)\}}"
        regions = re.findall(pattern, dump)
        for region in regions:
            city = {"type" : region[0],
                    "name": region[1],
                    "wikidata": region[2]
                    }
            cities.append(city)
        if len(regions) == 0:
            return cities

    except Exception as e:
        pass
    return cities


def parse_first_layer_region(dump):
    first_layer_region = {}
    first_layer_region["cities"] = []
    pattern = r"<title>(.+)</title>"
    result = re.search(pattern, dump)
    first_layer_region["title"] = result.group(1)


    pattern = r"<id>(.+)</id>"
    result = re.search(pattern, dump)
    first_layer_region["id"] = result.group(1)

    pattern = r"<text.+>.+((?s:.)+?)(==)"
    result = re.search(pattern, dump)
    first_layer_region["description"] = result.group(1)


    try:
        pattern = r"(\|region\d+name(?s:.)+?)(\n\n)"
        regions = re.findall(pattern, dump)
        first_layer_region["second_layer_region_names"] = []

        if len(regions) == 0:
            first_layer_region["second_layer_region_names"].append("Other")
            cities = parse_cities_list(dump)
            first_layer_region["cities"] = cities
            return first_layer_region

        for region in regions:
            pattern = r"name(?:\s|)=(?:\s|)(.+)"
            name = re.search(pattern, region[0])
            first_layer_region["second_layer_region_names"].append(name.group(1))

    except Exception as e:
        first_layer_region["second_layer_region_names"].append("Other")

    return first_layer_region

dump = """ <page>
    <title>Central Italy</title>
    <ns>0</ns>
    <id>6506</id>
    <revision>
      <id>3792058</id>
      <parentid>3729055</parentid>
      <timestamp>2019-06-05T10:29:45Z</timestamp>
      <contributor>
        <username>3knolls</username>
        <id>2179953</id>
      </contributor>
      <comment>/* Go next */added content</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|Pagebanner default.jpg}}
'''Central [[Italy]]''' contains several distinctive regions that have played a formidable role not only in Italian history, but in world history, as the centres of the Etruscan and [[Roman Empire|Roman]] civilizations and of the Holy See of the Catholic Church.

==Regions==
{{mapframe|42.8|12|zoom=7|width=525|height=428|staticmap=Central Italy WV map PNG.png}}
{{Regionlist

|region1name = [[Tuscany]]
|region1color = #D5DC76
|region1description =The cradle of the Rinascimento (Italian Renaissance), a region of history, culture and wine, featuring the formerly warring cities of [[Florence]], [[Siena]] and [[Pisa]] and lots of lovely countryside

|region2name = [[Marche]]
|region2color = #B383B3
|region2description = Known for its shoemaking tradition, with the finest and most luxurious Italian footwear being manufactured in this region. 

|region3name = [[Umbria]]
|region3color =  #B5D29F
|region3description =A mountainous region of winding roads, black truffles, cinghiale (wild boar) and some famous walled cities such as [[Assisi]], [[Perugia]], [[Spoleto]] and [[Gubbio]] 

|region4name = [[Lazio]]
|region4color = #D09440
|region4description =Formerly called ''Latium'', this was the heart of [[Roman Empire|ancient Rome]]

|region5name = [[Abruzzo]]
|region5color = #71B37B
|region5description = A central region of Italy composed of rolling hills and fertile plains at the base of the Apennine mountains, featuring wild beaches and ancient towns perched on hilltops}}

{{mapshape|type=geoshape|title=[[Tuscany]]|fill=#D5DC76|wikidata=Q1273}}
{{mapshape|type=geoshape|title=[[Marche]]|fill=#B383B3|wikidata=Q1279}}
{{mapshape|type=geoshape|title=[[Umbria]]|fill=#B5D29F|wikidata=Q1280}}
{{mapshape|type=geoshape|title=[[Lazio]]|fill=#D09440|wikidata=Q1282}}
{{mapshape|type=geoshape|title=[[Abruzzo]]|fill=#71B37B|wikidata=Q1284}}

==Cities==
* {{marker|type=city|name=[[Rome]]|wikidata=Q220}} — called the &quot;Eternal City&quot;, this modern capital of Italy was the seat of ancient Rome's power and remains the world headquarters of the Catholic Church. This great walking city features the Vatican, the Roman Forum, the Colosseum, the Campidoglio and hundreds of great churches. 
* {{marker|type=city|name=[[Ancona]]|wikidata=Q3415}}
* {{marker|type=city|name=[[Florence]]|wikidata=Q2044}} — there is so much culture and history packed into this city that there is a name for the cultural overload some visitors experience here: &quot;Stendhal syndrome&quot;!
* {{marker|type=city|name=[[Latina]]|wikidata=Q13410}} — the capital of [[Latina (province)|Latina Province]] of Lazio, it was inaugurated in 1932 under Mussolini and is mostly notable for some Fascist architecture
* {{marker|type=city|name=[[L'Aquila]]|wikidata=Q3476}}
* {{marker|type=city|name=[[Livorno]]|wikidata=Q6761}}
* {{marker|type=city|name=[[Perugia]]|wikidata=Q3437}} — a charming medium-sized walled, cobblestoned city with some notable artistic attractions, schools and the Perugina chocolate factory
* {{marker|type=city|name=[[Pescara]]|wikidata=Q2704}} — birthplace of Gabriele D'Annunzio, this modern city is rich in culture, art and traditions
* {{marker|type=city|name=[[Pisa]]|wikidata=Q13375}} — the city of the Campo dei Miracoli, which includes the famous Leaning Tower

==Other destinations==
* {{marker|type=vicinity|name=[[Cupramontana]]|wikidata=Q123981}} - Capital of the white &quot;Verdicchio&quot; wine
* {{marker|type=vicinity|name=[[Maremma]]|wikidata=Q1233184}}

==Understand==
This region of Italy was settled very early. Quite a number of the more beautiful towns in what are now Tuscany, Umbria and Lazio started their existence as Etruscan hill cities. Later, the ancient Romans, from their base in Rome, expanded into the Etruscan lands and conquered these cities.

As part of [[Medieval and Renaissance Italy]], the Tuscan cities of [[Florence]], [[Siena]] and [[Pisa]] vied for power and a monopoly over European trade with Asia. Most of the rest of this area was under the control of the Pope as part of the Papal States, except for most of [[Abruzzo]], which was part of the Kingdom of Naples and then the Kingdom of the Two Sicilies, initially under the control of France and then for hundreds of years prior to Italian unification, under the control of Spain.

In historical terms, Florence is second only to Rome in the history of this part of Italy, as the city of Dante, Petrarch, Donatello, Giotto, Michelangelo, and many other important figures of the Italian Gothic and Renaissance. In fact, Florence is considered to have started the Renaissance, and because its writers were so important, it is the Tuscan form of literary Italian that was taken as the standard language of the entire country.

In terms of tourism, too, the cities in this part of the country that are on nearly everyone's whirlwind &quot;Italy in one week&quot; list are Rome and Florence. However, though those cities are so full of things to see and do that you could spend months or more visiting sights there and not exhaust them, there is so much else to see, including not only the other cities mentioned or listed above but also a myriad of pleasant small towns and gorgeous countryside, country estates and gardens like those of the Villa d'Este in [[Tivoli]] and the Medici villas outside of Florence, Etruscan remains, such as the necropoli near [[Tarquinia]] and stelae on display in several archaeological museums including the ones in [[Arezzo]] and [[Volterra]], hot springs (''terme'' in Italian), pleasant mountains, and two coasts.

==Talk==
These regions of Italy have maintained their different dialects and accents since Italian unification in 1871, but if you speak Italian, you are unlikely to have much trouble understanding people throughout the area. But don't expect everyone to speak English, even in Rome. People will try their best to help you, but they will definitely appreciate any attempt to speak some Italian.

==Get in==

==Get around==

==See==

==Do==

==Eat==

==Drink==

==Stay safe==

==Go next==
* [[Northern Italy]]
* [[Southern Italy]]

{{IsPartOf|Italy}}
{{outlineregion}}

{{geo|42.9|13|zoom=8}}</text>
      <sha1>3yedujhp1kof2zca6sw9gfns27plto9</sha1>
    </revision>
  </page>"""
# parse_first_layer_region(dump)

dump = """
 <page>
    <title>Tuscany</title>
    <ns>0</ns>
    <id>36971</id>
    <revision>
      <id>3693975</id>
      <parentid>3585626</parentid>
      <timestamp>2019-01-13T12:25:50Z</timestamp>
      <contributor>
        <username>Traveler100bot</username>
        <id>160739</id>
      </contributor>
      <comment>Listings Accessibility</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|Toscana banner Copse in agricultural fields.jpg|unesco=yes}}

[http://www.turismo.intoscana.it/site/en '''Tuscany'''] ([[Italian phrasebook|Italian]]: ''Toscana'') is a region on [[Italy]]'s west coast, on the Tyrrhenian sea. It is one of the most popular places to visit in a country that is itself one of the most popular tourist destinations in the world. There are several reasons to visit Tuscany: some of the most important ones are seeing Renaissance art in [[Florence]], eating Tuscan food and tasting the excellent local wines, and after all this enjoying a day at the beach in [[Viareggio]].

==Regions==
===Provinces===
{{mapframe|43.431|11.142|zoom=8|height=560|width=510|staticmap=Map of region of Tuscany, Italy, with provinces-en.svg}}
{{mapshape}}

{{Regionlist
| region1name=[[Arezzo (province)|Arezzo]] (AR)
| region1color=#a9f0ff
| region1items=
| region1description=

| region2name=[[Florence (province)|Florence]] (FI)
| region2color=#ffa09e
| region2items=
| region2description=

| region3name=[[Grosseto (province)|Grosseto]] (GR)
| region3color=#ffd0a4
| region3items=
| region3description=

| region4name=[[Livorno (province)|Livorno]] (LI)
| region4color=#c0a2ff
| region4items=
| region4description=

| region5name=[[Lucca (province)|Lucca]] (LU)
| region5color=#ffe380
| region5items=
| region5description=

| region6name=[[Massa-Carrara (province)|Massa-Carrara]] (MS)
| region6color=#b8adff
| region6items=
| region6description=

| region7name=[[Pisa (province)|Pisa]] (PI)
| region7color=#9cff97
| region7items=
| region7description=

| region8name=[[Pistoia (province)|Pistoia]] (PT)
| region8color=#99caff
| region8items=
| region8description=

| region9name=[[Prato (province)|Prato]] (PO)
| region9color=#ccff67
| region9items=
| region9description=

| region10name=[[Siena (province)|Siena]] (SI)
| region10color=#b0bcff
| region10items=
| region10description=
}}

{{mapshape|type=geoshape|fill=#a9f0ff|title=[[Arezzo (province)|Arezzo]] (AR)|wikidata=Q16115}}
{{mapshape|type=geoshape|fill=#ffa09e|title=[[Florence (province)|Florence]] (FI)|wikidata=Q18288148}}
{{mapshape|type=geoshape|fill=#ffd0a4|title=[[Grosseto (province)|Grosseto]] (GR)|wikidata=Q16185}}
{{mapshape|type=geoshape|fill=#c0a2ff|title=[[Livorno (province)|Livorno]] (LI)|wikidata=Q16200}}
{{mapshape|type=geoshape|fill=#ffe380|title=[[Lucca (province)|Lucca]] (LU)|wikidata=Q16202}}
{{mapshape|type=geoshape|fill=#b8adff|title=[[Massa-Carrara (province)|Massa-Carrara]] (MS)|wikidata=Q16205}}
{{mapshape|type=geoshape|fill=#9cff97|title=[[Pisa (province)|Pisa]] (PI)|wikidata=Q16244}}
{{mapshape|type=geoshape|fill=#99caff|title=[[Pistoia (province)|Pistoia]] (PT)|wikidata=Q16245}}
{{mapshape|type=geoshape|fill=#ccff67|title=[[Prato (province)|Prato]] (PO)|wikidata=Q16250}}
{{mapshape|type=geoshape|fill=#b0bcff|title=[[Siena (province)|Siena]] (SI)|wikidata=Q16275}}

===Other regions===
*The wine growing region of [[Chianti]]
*The ecogreen area of [[Casentino]]
*[[Maremma]], a less populated region, in south Tuscany and North Latiun

==Cities==

*{{marker|type=city|name=[[Florence]]|lat=43.783333|long=11.25|wikidata=Q2044}} (Italian: ''Firenze'') – Capital of the region and considered the centre of the Renaissance. Also a {{UNESCO}}.

&lt;!-- capital top, alphabetise the rest --&gt;
*{{marker|type=city|name=[[Arezzo]]|lat=43.473333|long=11.87|wikidata=Q13378}}
*{{marker|type=city|name=[[Chiusi]]|lat=43.016667|long=11.95|wikidata=Q91185}}
*{{marker|type=city|name=[[Lucca]]|lat=43.841667|long=10.502778|wikidata=Q13373}}
*{{marker|type=city|name=[[Montepulciano]]|lat=43.1|long=11.783333|wikidata=Q91217}} – Hilltop town known for its wine.
*{{marker|type=city|name=[[Pienza]]|lat=43.078611|long=11.678889|wikidata=Q91341}}
*{{marker|type=city|name=[[Pisa]]|lat=43.716667|long=10.4|wikidata=Q13375}} – City known worldwide for its Leaning Tower.
*{{marker|type=city|name=[[San Gimignano]]|lat=43.468|long=11.042|wikidata=Q91413}}
*{{marker|type=city|name=[[Siena]]|lat=43.318611|long=11.330556|wikidata=Q2751}}

==Other destinations==
[[File:Tuscan Landscape 7.JPG|thumb|Except for the recent introduction of large-scale sunflower cultivation for oil, the Tuscan countryside in many instances looks quite similar to what you see in Gothic Florentine and Sienese paintings]]
There are many hot springs in Tuscany, which have been prized since [[Roman Empire|ancient Roman]] times, if not earlier.

==Understand==
Tuscany has three very diverse faces; the art cities such as [[Florence]], [[Siena]], [[Lucca]] and [[Pisa]], the countryside, and the coastal and islands region.

The small towns, villages, castles, villas and vineyards of Tuscany make a welcome change from the traffic and noise of some of the larger Tuscan cities.

==Get in==
[[File:Ponte Vecchio at dusk 1.JPG|thumb|The Ponte Vecchio, [[Florence]], at dusk]]
===By plane===
International flights commonly come in to [[Milan]] or [[Rome]], where one can rent a car and do the three-hour drive to Tuscany.

Florence and Pisa have important airports. Every major city has a railway station.

*{{marker|type=go|name=Pisa International Airport|url=http://www.pisa-airport.com/|lat=43.6985|long=10.4003}} ({{IATA|PSA}}), 1.5km (1 mile) south of Pisa city centre.
*{{marker|type=go|name=Amerigo Vespucci International Airport|url=http://www.aeroporto.firenze.it/|lat=43.8032|long=11.2003}} ({{IATA|FLR}}), four kilometres from the centre of Florence.

Delta Air Lines (US carrier) has a direct flight from New-York JFK to Pisa, offering a cheaper, alternative to flying into Florence.

===By train===
Florence, Pisa, and Grosseto are important rail destinations. Florence has two major rail stations, Santa Maria Novella (SMN) in the city centre and Campo di Marte (CdM) a bit further away.

Connections from Florence to the rest of Italy by train are generally fast and frequent and EuroStar Italia services are available. Easy connections can be found to:

* [[Milano]]
* [[Orvieto]]
* [[Rome]]
* [[Bologna]]
* [[Ravenna]]
* [[Cinque Terre]] (reachable by train to [[La Spezia]] or [[Riomaggiore]], or connecting from [[Genoa]])
* [[Assisi]]

Night train services are available from Florence to:
* [[Zurich]]
* [[Munich]]
* [[Siracusa]]
* [[Salerno]]
* [[Reggio]]
and others.

==Get around==
[[File:Adorazione dei Magi by Gentile da Fabriano - Predella.jpg|thumb|370px|Adoration of the Magi by the Florentine Gothic painter, Gentile da Fabriano, on display at the Uffizi in Florence]]
===By train===
From the central station of Florence you can easily reach most places in Tuscany, including:

* [[Siena]] (1.5 to 2 hours)
* [[Pisa]] (1 to 1.5 hours)
* [[San Gimignano]] (by train to Poggibonsi, 1 hour ride, and then a bus that runs every 30-40 minutes, 25 minute ride)
* [[Volterra]] (also reachable by bus from Poggibonsi)
* [[Lucca]]
* [[Arezzo]]

===By bus===
[http://www.busfox.com/timetable/ Toscana Mobilitá] has a useful website  for bus routes and schedules in Tuscany. The site is mostly in Italian, but is simple to use. (The Tuscan bus companies Siena Mobilitá, Tiemme, and Toscana Mobilitá seem to be affiliated.)

[http://sienamobilita.it/orari.html Siena Mobilità] {{dead link|August 2018}} has bus schedules (''orari'') for and between a number of popular towns in Tuscany including Florence (''Firenze'' in the schedule), Siena, San Gimignano, Arezzo, Cortona, Montepulciano and Chiusi among others. Local services for several cities are marked ''urbano''. The interurban services are all under the tab ''servizio extraurbano''.

Google maps identify bus stops throughout Tuscany for both local and interurban routes. If you click on the bus stop symbol, you can get a list of bus routes serving that stop. Using Google Streetview, you can often identify which side of the road the stop is situated and hence which direction of travel is served by the stop.

Bus users should purchase their bus tickets before boarding the bus. Most ''Tabacchi''-shops (tobacconists) sell bus tickets. Sometimes newsstands and bars may also sell tickets. You must tell the ticket seller your destination so that your ticket will be valid for the correct fare zones.  After boarding the bus, stamp your ticket in the machine located behind the driver.

Be aware that many routes have either reduced or no service on Saturdays, Sundays and holidays. Schedules indicate reduced service as ''festivo'' while the regular work day schedule is ''feriale''. Many bus stops have posted schedules.

Blue-coloured buses are for interurban service while orange-coloured buses are for local service. Interurban buses can serve local stops along the route.

==See==
[[File:Cathedral and Campanary - Pisa 2014 (2).JPG|thumb|Campo dei Miracoli, [[Pisa]]]]
{{style|There should be no individual listings at the regional level, only a prose overview.}}

Tuscany is world-famous for its churches, including the Duomo and Baptistery, Santa Croce, Santa Maria Novella, San Miniato al Monte and several others in Florence; the Duomo and Baptistery in Siena; and the Duomo and Baptistery in Pisa.

Tuscany is also known for its great museums, especially the Uffizi in Florence but also the Bargello and Accademia, the Musei dell'Opera del Duomo in Florence and Siena, the museum in the Palazzo Pubblico and the Pinacoteca in Siena, and the Museo Archeologico in Arezzo, among many others.

The small town of San Gimignano deserves special mention because while none of its churches or museums are very large, it contains so much beauty in such a small area. The town of Pienza is itself practically a museum in the round, as its foremost claim to fame is its architecture. There are many other beautiful small towns with great art, including Cortona.

Which segues into the other great draw of a trip to Tuscany: The beauty of the countryside. In order to understand Tuscan painting, you need to see the Tuscan countryside, which except for the relatively recent introduction of sunflower cultivation is still similar to what you can see in paintings by great Gothic painters like Giotto (Florentine), Simone Martini and Duccio (Sienese).

=== Parks ===

*  {{see
| name=The National Park of the Tusco-Emilian Apennines | alt= | url=http://www.parcoappennino.it/Eindex.php | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=extends lengthwise for about 60&amp;nbsp;km from the high valleys of the mountain torrents of Parma and Baganza up to the Passo delle Forbici, opening up to include on the Tuscan side the calcareous massif of the Pania di Corfino, and in Emilia the chain of the Alps of Succiso, of Monte Cusna, the valley of the river Secchia and the isolated range of the Pietra di Bismantova.
}}
* {{see
| name=The National Park of the Tuscan Archipelago | alt= | url=http://www.islepark.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=the Park was established in 1996 and it covers an area of over 18,000 hectares in addition to 40,000 hectares of sea. It is managed by an organization with the same name, that has its headquarters in Portoferraio (on Elba Island). The Park falls under the jurisdiction of the Province of [[Livorno]] and that of [[Grosseto]].
}}
* {{see
| name=The National Park of the Foreste Casentinesi, Monte Falterona and Campigna | alt= | url=http://www.parcoforestecasentinesi.it/pfc/index.php?option=com_inclusore_homepage&amp;lang=en&amp;jos_change_template=pfc_homepage | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=Following the Arno upstream you enter the district of Casentino surrounded by mountains to the north and the east. Here the National Park of the Foreste Casentinesi, Monte Falterona and Campigna offers a uniquely moving and unforgettable experience: that of discovering one of the oldest forests in Europe.
}}
*  {{see
| name=The Maremma Regional Park | alt= | url=http://www.parco-maremma.it/index.php?lang=en | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=the Maremma Regional Park (Parco Regionale della Maremma), also known as ''Uccellina Park'' (Parco dell’Uccellina) covers a coastal area between Principina a Mare and Talamone near [[Grosseto]], Magliano in Toscana and [[Orbetello]], right up to the [[Livorno]] – [[Rome]] train line.
}}
* {{see
| name=The Park of the Apuan Alps | alt= | url=http://www.parcapuane.toscana.it | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=
}}
* {{see
| name=The Orecchiella park | alt=brief guide of the park | url=http://www.pruneta.com/?page_id=679&amp;lang=en | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=
}}
* {{see
| name=The Park of Migliarino, San Rossore and Massaciuccoli | alt= | url=http://www.parcosanrossore.org/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=the Park of Migliarino, San Rossore and Massaciuccoli was established in 1975 and covers 24,000 hectares between [[Pisa]], [[Viareggio]], San Giuliano Terme, Vecchiano and Massarossa. What makes this park so special is what lies around its borders: the Tirrenian Sea, Lake Massaciuccoli and the rivers Arno, Serchio, Canale dei Navicelli and Morto e Burlamacca.
}}
* {{see
| name=The Montioni nature park | alt= | url=http://www.parcodimontioni.it/index.html | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=managed by the Municipale Administrations of [[Grosseto]] and [[Livorno]]. Park status from 1998. The park extends over 7000 hectares and rises to 300m at Poggio al Checco, its highest point. The territory has a large artistic and culture heritage, from ancient archeological finds to Etruscan and Roman remains which have been found under medieval constructions such as the Pievaccia, the ruins of Montioni Vecchio Castle and Montioni Thermal Baths.
}}
* {{see
| name=The Livorno Hills Park | alt= | url=http://www.parks.it/parco.monti.livornesi/index.html | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=the Livorno Hills Park encompasses a vast area between the districts of [[Livorno]], Collesalvetti and Rosignano Marittimo. It’s nickname is ‘the lost island’ due to the fact that this stretch of land was an island until it attached itself to the mainland thousands of years ago. The park has not only areas of outstanding natural beauty but also but has also been subject to interesting archeological, artistic and cultural discoveries.
}}
* {{see
| name=The Archaeological Park of Poggibonsi | alt= | url=http://www.paesaggimedievali.it/luoghi/Poggibonsi/indexparco.html {{dead link|October 2017|August 2018}} | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=the visit starts with a short documentary film that illustrates the results of twelve years of excavation and the most important archaeological, architectonical and naturalistic aspects of the Poggio Imperiale site.
}}
* {{see
| name=The Parks of the Val di Cornia | alt= | url=http://www.parchivaldicornia.it/index.php?lang=eng | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=the Parks of the Val di Cornia, in Tuscany, tell a thousand-year-old story which begins with the Etruscan people and bears witness to centuries of extraction and working on metals, proposing also splendid natural, coastal and hilly environments. The system includes 2 Archaeological Parks, Natural Parks, 3 Museums, 1 Documentation Centre, included in the area of the five municipalities at the extreme south of the province of [[Livorno]], opposite the Island of Elba.
}}
[[File:Villa medici di belcanto, villa inferiore 02.JPG|thumbnail|Medici Villas and Gardens, [[Fiesole]]]]

* {{see
| name=The Zoological Park of European Fauna in Poppi | alt= | url=http://www.parcozoopoppi.it/ | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=this is the first and only park dedicated to European Fauna open in the municipality of Poppi ([[Arezzo]]).
}}
* {{see
| name=The Pinocchio's Park | alt= | url=http://www.pinocchio.it/eng/pinocchio/index.php | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=: Pinocchio’s Park is in [[Collodi]], lovely ancient village that has remained virtually unchanged since the last century. Its charming collection of houses, nestled among the hills, leads the way to Villa Garzoni and its lovely 19th century garden, often considered among the most beautiful in Europe.
}}
* {{see
| name=Medici Villas and Gardens in Tuscany | alt= | url= | email=
| address= | lat= | long= | directions=
| phone= | tollfree= | fax=
| hours= | price=
| content=A [[UNESCO World Heritage site]] consisting of 16 major and 11 minor villas owned by the powerful Medici family in the 15th-17th centuries.
}}

==Do==
[[File:02 Sienne vue de San Clemente.jpg|thumb|[[Siena]]]]
Besides wandering in beautiful cities and looking at Renaissance art, there are many other things you can do in Tuscany. For example, you can learn to cook or just taste Tuscan food, do trekking, golf or go to a health spa.

''See also: [[Wine tourism#Italy]]''

Most of the important traditional wine producers are located along the axis formed by Florence and Siena. The most famous region is [[Chianti]] along with neighboring [[Montalcino]] and [[Montepulciano]]. The white wines are less famous than the reds, but as an exception the Vernaccia of [[San Gimignano]] is recognized as a DOCG wine. The Tuscan wine industry has evolved a lot during the last 30-40 years, and the result is what is called ''Super Tuscan'' wine, famously produced in [[Bolgheri]] but also in [[Maremma]] and many other parts of Tuscany.

Tuscany offers great biking opportunities, especially the central part. The hills and small cities give a pleasant variation, but it is rather strenuous, as  July and august can be very hot.

'''Thermal Springs''': Terme di Saturnia [[Saturnia]]

==Eat==
[[File:Duomo di Lucca vom Torre Guinigi 2009-07.jpg|thumb|The Duomo of [[Lucca]] and the hills beyond]]
Tuscan food is known for its relative simplicity and its reliance on the high-quality ingredients from its many farms.

A small selection of the rich regional Tuscan cuisine comprises:
* ribollita - bread soup with vegetables
* zuppa di verdure - green vegetable soup
* pici - thick spaghetti
* pasta e fagiolli - pasta with beans
* bistecca alla fiorentina (Florentine steak)
* desserts
** panforte, a unique dense Sienese fruit and nut cake
** cavallucci - Sienese Christmas cookies, made with almonds, candied fruit and also spices like anise and coriander that presumably date back to the time when Siena had a monopoly on trade with the East
** ricciarelli - almond paste cookies, also a speciality of Siena
** biscotti di [[Prato]], also called cantuccini - the almond biscuits most travellers to Italy are already familiar with originated in the Tuscan town of Prato and are still manufactured there

In addition, Tuscany has its own traditional [[cheese]]s, including Pecorino Toscano, a much milder cheese than the better-known Pecorino Romano and a great accompaniment to prosciutto and melon or just to eat with fresh bread, and Pecorino di Pienza, perhaps an even better appreciated local sheep cheese.

==Drink==

{{infobox|DOC, DOCG, IGT?|Tuscany has over 30 wines with a ''Denominazione di origine controllata'' certificate, some of which have also obtained the ''Denominazione di origine controllata e garantita'' certificate. The denominations witness to the strong dedication of the people of this land to vine-growing, and their deep knowledge of wine-making techniques. But some of the best Tuscan wines are labeled with the less strict ''Indicazione geografica tipica'' designation, often a sign of a more modern, &quot;international&quot; wine.}}

The question about what to drink in Tuscany is easy to answer. The region is famed for its wines, most notably the ''sangiovese'' reds ''Chianti'', ''Brunello di Montalcino'' and ''Vino Nobile di Montepulciano'' and the white ''Vernaccia di San Gimignano''. Of these, Chianti can be anything from inexpensive, drinkable plonk to, when it comes to the best examples of ''Chianti Classico'', a world class wine. The wines of Montalcino and Montepulciano are generally of a high standard, and in particular Brunello regularly receives lots of awards (something reflected on the price as well). If you are not prepared to pay a fortune for your wine but would still like something a bit nicer, both Montalcino and Montepulciano have the common man's version of their wines, ''Rosso di Montalcino'' and ''Rosso di Montepulciano''.

Of these traditional wines perhaps only Brunello has the power to accompany a big Florentine steak, ''bistecca alla fiorentina''. For something fleshier, you have to turn to the ''Super Tuscan'' wines. These commonly use ''cabernet sauvignon'' to complement or to completely replace the traditional grapes. Famous examples are ''Sassicaia'' and ''Tignanello''.

==Sleep==
[[File:San Gimignano, Piazza delle Erbe.jpg|thumb|Piazza delle Erbe, [[San Gimignano]]]]
There are loads of hotels in the cities that are major tourist attractions, including Florence and Siena, and there are also plenty of agriturismo spots and villas in the countryside. If you are seeking less expensive accommodation, you are more likely to find it closer to railway stations in cities like Florence, but some other cities' railway stations are outside the city walls, and some major destinations such as [[San Gimignano]] don't have any railway station at all. You may also try your luck at local tourism agencies, which may have a list of relatively inexpensive accommodations, such as apartments for rent by the day or week and pieno pensioni (boarding houses that provide 3 meals a day).

==Go next==

*[[Umbria]], to the east, shares Tuscany's rolling hills but is further inland and higher up; it is also less densely populated, and has an equally good but distinctive cuisine that features black truffles and mushrooms.
*[[Lazio]], to the south, was the heart of both ancient Rome and the Papal States, and though it, too, has beautiful countryside, it is above all the region of [[Rome]].
*[[Emilia-Romagna]], to the north, is another region traditionally known for its great food (especially in [[Bologna]]) and rich in history, including the extraordinary and very well-preserved Byzantine mosaics in [[Ravenna]].
*[[Liguria]], up the coast to the northwest, contains the Italian Riviera and the historic port city of [[Genoa]].
*The [[Marche]], which shares a short, mountainous border with the eastern side of Tuscany, is a lesser-known region, but one that also has quite a long history including the hill city of [[Urbino]] and also features the spectacular Grotte di Frasassi (Frasassi Caves).




{{isPartOf|Central_Italy}}

{{usableregion}}
{{geo|43.35|11.016666666667|zoom=8}}</text>
      <sha1>4f05r9gb5okitq77k1phxof61qnoez8</sha1>
    </revision>
  </page>
"""

def parse_second_layer_region(dump):
    second_layer_region = {}
    second_layer_region["cities"] = []
    pattern = r"<title>(.+)</title>"
    result = re.search(pattern, dump)
    second_layer_region["title"] = result.group(1)


    pattern = r"<id>(.+)</id>"
    result = re.search(pattern, dump)
    second_layer_region["id"] = result.group(1)

    pattern = r"<text.+>.+((?s:.)+?)(==)"
    result = re.search(pattern, dump)
    second_layer_region["description"] = result.group(1)

    try:
        pattern = r"(\| region\d+name(?s:.)+?)(\n\n)"
        regions = re.findall(pattern, dump)
        second_layer_region["third_layer_region_names"] = []

        if len(regions) == 0:
            second_layer_region["third_layer_region_names"].append("Other")
            cities = parse_cities_list(dump)
            second_layer_region["cities"] = cities
            return second_layer_region

        for region in regions:
            pattern = r"name(?:\s|)=(?:\s|)(.+)"
            name = re.search(pattern, region[0])
            second_layer_region["third_layer_region_names"].append(name.group(1))

    except Exception as e:
        second_layer_region["third_layer_region_names"].append("Other")

    return second_layer_region

#To do check name of a region third_layer_region_names
# parse_second_layer_region(dump)


dump="""
  <page>
    <title>Livorno (province)</title>
    <ns>0</ns>
    <id>19923</id>
    <revision>
      <id>3795126</id>
      <parentid>3707945</parentid>
      <timestamp>2019-06-12T15:41:16Z</timestamp>
      <contributor>
        <username>Inferno986return</username>
        <id>476466</id>
      </contributor>
      <comment>/* Stay safe */</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|WV banner Livorno province Montecristo island pier.jpg|pgname=Livorno}}
'''Livorno''' is a Province of the [[Tuscany]] Region of [[Italy]].

==Cities==
{{mapframe|width=530|height=500|43.1863|10.3862|zoom=9}}
{{mapshape}}
*{{marker|type=city|name=[[Livorno]]|lat=43.55|long=10.316667|wikidata=Q6761}} – Capital of the Province
*{{marker|type=city|name=[[Castiglioncello]]|lat=43.405386|long=10.410297|wikidata=Q1244388}}
*{{marker|type=city|name=[[Rosignano Marittimo]]|lat=43.4|long=10.466667|wikidata=Q157871}}

==Other destinations==
*The island of {{marker|type=vicinity|name=[[Elba]]|lat=42.761833|long=10.240833|wikidata=Q45328}}.

==Understand==

==Get in==

==Get around==

==See==

==Do==

==Eat==

==Drink==

==Stay safe==
{{movetocity}}
* '''[http://www.agriturismodesantis.it Agriturismo De Santis]''' Via Boldini, 5 Castiglioncello (Li). &quot;Agriturismo De Santis&quot;, lies in the heart of the Etruscan coast, close to the most famous Tuscan cities of art. Surrounded by olive groves, orchards, vineyards and wooded hills it enjoys a magnificent panorama of the surrounding countryside and the sea and has a large garden with swimming pool. The few bedrooms, each with its own bathroom, are all furnished in Tuscan style. Mountain bikes are available for relaxing excursions in the surrounding countryside.
For booking: +39 347 6240444 - info@agriturismodesantis.it.

* '''[http://www.poggioallagnello.it Holiday Resort Poggio all'Agnello]''' Località Baratti(Li). &quot;Poggio all'Agnello&quot; is a new holiday resort on the Tuscany coast.It features 3 swimming-pools, restaurant, bar and over 171 apartmens for rent set in a large park with pic-nic areas. It also features a private beach on the Baratti Gulf, near Elba Island. Suitable for families, young people and holiday groups.
* '''[http://www.campastrellosport.it Campastrello Sport Hotel &amp; Residence]''' Via Campastrello, 1 - Castagneto Carducci (LI). Campastrello Sport Residence Hotel in Tuscany is located by the seaside 3 km from the Tuscan Riviera in the small town of Castagneto Carducci. Set in 5 hectares of private parkland, it features a swimming-pool, restaurant, play courts (tennis, soccer, etc.), hotel rooms and furnished apartments for holiday rentals.
* '''[http://www.lacerreta.it/en/ La Cerreta Farmhouse]''' Via Campagna Sud, 143 - Località Pian delle Vigne - 57020 - Sassetta (LI). La Cerreta is a biodynamic farmhouse located in Sassetta (LI), in the countryside of central Tuscany, about 20 km from the coast. Accommodation is provided to guests in four country holiday houses. A restaurant is available in the farmhouse. The food served is nearly entirely produced at La Cerreta (90 to 95%): meat, pasta, wine and olive oil, vegetables and fruits, cheese, ham, salami, marmalade, honey and bread.

==Go next==


{{IsPartOf|Tuscany}}
{{outlineregion}}

{{geo|43.19|10.316666|zoom=9}}</text>
      <sha1>3ud2x8r6t3i8ulo4e32alj6s3kklk65</sha1>
    </revision>
  </page>
"""
dump="""<page>
    <title>Arezzo (province)</title>
    <ns>0</ns>
    <id>1525</id>
    <revision>
      <id>3746717</id>
      <parentid>3694019</parentid>
      <timestamp>2019-03-19T01:40:43Z</timestamp>
      <contributor>
        <username>DaGizza</username>
        <id>162256</id>
      </contributor>
      <comment>ce</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|WV banner Arezzo Province Croce Pratomagno.jpg|pgname=Arezzo}}
'''[https://www.discovertuscany.com/arezzo/ Arezzo]''' is a province of the [[Tuscany]] region in [[Italy]].

==Regions==
{{Regionlist
|region1name = [[Casentino]]
|region1color={{StdColor|t1}}
|region1items=
|region1description=

|region2name = [[Val di Chiana]]
|region2color={{StdColor|t2}}
|region2items=
|region2description=

}}
{{mapshape|type=geoshape|fill={{StdColor|t1}}|title=[[Casentino]]|wikidata=Q1047110}}
{{mapshape|type=geoshape|fill={{StdColor|t2}}|title=[[Val di Chiana]]|wikidata=Q1071597}}
==Cities==
{{mapframe|43.5293|11.9312|zoom=9}}
{{mapshape}}
*{{marker|type=city|name=[[Arezzo]]|lat=43.47333|long=11.87|wikidata=Q13378}} – Capital of the Province
*{{marker|type=city|name=Bibbiena|lat=43.7|long=11.82|wikidata=Q52066}}
*{{marker|type=city|name=[[Castiglion Fiorentino]]|lat=43.3438889|long=11.9188889|wikidata=Q52074}}
*{{marker|type=city|name=[[Cavriglia]]|lat=43.5167|long=11.4833|wikidata=Q52075}}
*{{marker|type=city|name=[[Cortona]]|lat=43.275556|long=11.988056|wikidata=Q52080}} - founded by the Etruscans, who called it Curtun in their language. The city was also important during Roman times.
*{{marker|type=city|name=[[Lucignano]]|lat=43.266667|long=11.75|wikidata=Q52084}}
*{{marker|type=city|name=[[Montevarchi]]|lat=43.528611|long=11.57|wikidata=Q52089}}
*{{marker|type=city|name=[[Poppi]]|lat=43.716667|long=11.766667|wikidata=Q52095}}
*{{marker|type=city|name=[[Pergine Valdarno]]|lat=43.466667|long=11.683333|wikidata=Q52092}}
*{{marker|type=city|name=[[Stia]]|lat=43.804128|long=11.708641|wikidata=Q52100}}
*{{marker|type=city|name=[[Terranuova Bracciolini]]|lat=43.55|long=11.583333|wikidata=Q52104}}

==Understand==

==Get in==

==Get around==

==See==

==Do==

==Eat==

==Drink==

==Stay safe==

==Go next==

{{IsPartOf|Tuscany}}
{{outlineregion}}

{{geo|43.473|11.875|zoom=10}}</text>
      <sha1>duye0pb8g8jqmelv91pwz1l5tvku3nh</sha1>
    </revision>
  </page>"""

def parse_third_layer_region(dump):
    third_layer_region = {}
    third_layer_region["cities"] = []
    pattern = r"<title>(.+)</title>"
    result = re.search(pattern, dump)
    third_layer_region["title"] = result.group(1)


    pattern = r"<id>(.+)</id>"
    result = re.search(pattern, dump)
    third_layer_region["id"] = result.group(1)

    pattern = r"<text.+>.+((?s:.)+?)(==)"
    result = re.search(pattern, dump)
    third_layer_region["description"] = result.group(1)

    try:
        pattern = r"(\|\s|region\d+name(?s:.)+?)(\n\n)"
        regions = re.findall(pattern, dump)
        third_layer_region["third_layer_region_names"] = []

        if len(regions) == 0:
            third_layer_region["third_layer_region_names"].append("Other")
            cities = parse_cities_list(dump)
            third_layer_region["cities"] = cities
            return third_layer_region


        for region in regions:
            pattern = r"name(?:\s|)=(?:\s|)(.+)"
            name = re.search(pattern, region[0])
            third_layer_region["third_layer_region_names"].append(name.group(1))

    except Exception as e:
        third_layer_region["third_layer_region_names"].append("Other")


    return third_layer_region

# parse_third_layer_region(dump)


dump="""<page>
    <title>Casentino</title>
    <ns>0</ns>
    <id>6164</id>
    <revision>
      <id>3763641</id>
      <parentid>3582550</parentid>
      <timestamp>2019-04-17T23:03:53Z</timestamp>
      <contributor>
        <username>Matroc</username>
        <id>248572</id>
      </contributor>
      <minor />
      <comment>/* Cities */ add wikidata ids to city markers</comment>
      <model>wikitext</model>
      <format>text/x-wiki</format>
      <text xml:space="preserve">{{pagebanner|Poppi banner.jpg}}
'''Casentino''' is a valley in the north of the Province of [[Arezzo (province)|Arezzo]], in [[Tuscany]].

==Cities==
{{mapframe}}


[[Image:IMG 0496BibbienaTower.jpg|thumb|Bibbiena Tower]]

*{{marker|type=city|name=[[Bibbiena]]|wikidata=Q52066}}
*{{marker|type=city|name=[[Capolona]]|wikidata=Q52068}}
*{{marker|type=city|name=[[Castel Focognano]]|wikidata=Q52070}}
*{{marker|type=city|name=[[Castel San Niccolò]]|wikidata=Q52071}}
*{{marker|type=city|name=[[Chiusi della Verna]]|wikidata=Q52077}}
*{{marker|type=city|name=[[Chitignano]]|wikidata=Q52076}}
*{{marker|type=city|name=[[Montemignaio]]|wikidata=Q52087}}
*{{marker|type=city|name=[[Pratovecchio]]|wikidata=Q52096}}
*{{marker|type=city|name=[[Ortignano Raggiolo]]|wikidata=Q52091}}
*{{marker|type=city|name=[[Poppi]]|wikidata=Q52095}}
*{{marker|type=city|name=[[Stia]]|wikidata=Q52100}}
*{{marker|type=city|name=[[Strada in Casentino]]|wikidata=Q18486142}}
*{{marker|type=city|name=[[Subbiano]]|wikidata=Q52102}} - near [[Arezzo]]
*{{marker|type=city|name=[[Talla]]|wikidata=Q52103}}

==Other destinations==

==Understand==
Casentino is in Tuscany where the Arno river is born (then goes on to Florence and Pisa): the valley is shaped like a basket, with mountains all around. You can arrive here from Florence or from Arezzo. From Florence (about one hour by car) you can take the Passo della Consuma starting Pontassieve; from Arezzo (about half an hour by car) you can arrive directly following the Arno river. Here the peak of Monte Falco reaches 1658 m (5440 ft). Casentino is a deep-green land of Castles, romanesque Churches, Sanctuaries. ..such as Poppi Castle, a Manor of Conti Guidi Family, that is actually well conserved; Romena Castle, Porciano Castle, Chitignano Castle etc... Large stretches of woods, dominated by silver firs and beeches are found inside the 'Foreste Casentinesi' National Park. The National Park &quot;Foreste Casentinesi&quot; lies on the northern Appennine crest between Tuscany and Romagna, where deer, wild boar, eagle and even the wolf use to live. The Park covers an area of 36.000 hectars, mainly covered with woods of firs, oaks, beechs and chestnunts. Istoric roads, climbing Appennines recall closeknit ties between the valley and Florence, Romagna, Arezzo.

==Get in==
Closest airports are Florence, but Pisa, Bologna and Rome are also suitable. 

By car from Florence airport: follow directions to Pontassieve, then to the Consuma Pass and continue down to Bibbiena/Poppi. (About 1,1/2hours). Otherwise take the A1 motorway south exiting at Arezzo then head towards Bibbiena/Poppi (about 1 and 1/2 hours). 

By car from Pisa airport: take the Firenze Mare motorway to Florence exit at Firenze Sud and take the road for Pontassieve and Consuma Pass or continue on A1 motorway towards Rome exiting at Arezzo. 

From Arezzo there is also the local railway LFI that arrives in all the towns of the valley. 

The best way to reach all the discovering corners is the car, but you can reach the valley even by train (Arezzo-Stia) or by bus (From Florence the Sita Bus service)

==Get around==

==See==

Everywhere in Casentino valley you will find invaluable signs of history and art. All villages scattered in the valley have either a castle, a square, a church, or walls which are the magnificent heritage that the Middle Ages and Renassance left in these lands.Some of the castles lie in ruins, but some are magnificent, like Poppi Castle. The Castle of the Guidi Family in Poppi Village was built in the XIII century. Everywhere you can find masterpieces of the Della Robbia school and of famous painters like Sandro Botticelli, Cola da Camerino, Domenico del Ghirlandaio and Bicci di Lorenzo. The landscape is great, breathtaking. The villages and sites are not overcrowded, actually, and that makes siteseeingh enjoyable especially if you are travelling with children for your family holidays

Some of the castles lie in ruines, but some are magnificent, like Poppi Castle: the Castle of the Guidi Family in Poppi Village was built in the XIII century. After the end of Conti Guidi Family, it was the place where Florence's Vicars lived. It has meny similarities with Palazzo Vecchio in Florence It shows a facade with mullioned windows with 2 lights and a high tower, it is surrounded by walls and a large moat. The castle is well conserved and contains the Rilliana Historic library (incunabola and manuscripts) a small museum about the famous Campaldino battle (1289) and a Chapel with Taddeo Gaddi's frescoes. The castle is open all the year long with an entrance fee (4 euros in 2004). Being the castle owned by the Poppi Community, it is even possible to celebrate a civil marriage into the castle main room.

The National Park &quot;Foreste Casentinesi&quot; lies on the northern Appennine crest between Tuscany and Romagna. It covers an area of 36.000 hectars. Here the peak of Monte Falco reaches 1658 m (5440 ft). Here River Arno flows towards Florence. More than 80% of the park is covered with woodland: silver fir woods near Camaldoli monastry, century old beeches covering La Verna mountain near S.Francis Monastry, big chestnunt trees, mixed woods of oak, maple, elm. The park areas welcome the richest fauna in northern Appennines: roe deer, red deer, fallow deer, all them may be spotted while feeding in the park meadows and clearings. Wolves find in the park an ideal habitat. More than 80 resident bird species, and eagles too, nest in the woods. Foreste Casentinesi National Park includes the Monastry of  Camaldoli was estabilished in 1012 (S. Romualdo, Camaldolesian Congregation). Foreste Casentinesi National Park includes also the Monastry of La Verna: is the Monastry where St. Francis spent the last years of his life and received his Stigmata in 1224.

==Do==

==Eat==

==Drink==

==Stay safe==

==Go next==

{{outlineregion}}

{{geo|43.7000|11.8167|zoom=11}}

{{IsPartOf|Arezzo (province)}}</text>
      <sha1>mvrrq19azdat7w9kyh0bsivde8yy6h6</sha1>
    </revision>
  </page>"""

def parse_fourth_layer_region(dump):
    try:
        fourth_layer_region = {}

        fourth_layer_region["cities"] = []
        pattern = r"<title>(.+)</title>"
        result = re.search(pattern, dump)
        fourth_layer_region["title"] = result.group(1)


        pattern = r"<id>(.+)</id>"
        result = re.search(pattern, dump)
        fourth_layer_region["id"] = result.group(1)

        pattern = r"<text.+>.+((?s:.)+?)(==)"
        result = re.search(pattern, dump)
        fourth_layer_region["description"] = result.group(1)

        cities = parse_cities_list(dump)
        fourth_layer_region["cities"] = cities
        # return third_layer_region


    except Exception as e:
        return fourth_layer_region
        pass


    return fourth_layer_region

# parse_fourth_layer_region(dump)


MAIN_DUMP = get_dump("main.xml")
continent = parse_continent("Europe")


for i in range(len(continent["regions"]) - 1):
    region = continent["regions"][i]
    i+=1
    countries = []
    for country in region["countries"]:
        d = parse_country(country[2:-2])
        countries.append(d)

    region["countries"] = countries
logs(json.dumps(continent, indent=5))

pass



#country bugs Moldova regions
# check '[[Guernsey]]'
# '[[Isle of Man]]'