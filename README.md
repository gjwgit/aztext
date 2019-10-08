# Azure Text Analytics

This [MLHub](https://mlhub.ai) package provides a quick introduction
to the pre-built Text Analytics models provided through Azure's
Cognitive Services. This service extracts information from the text
supplied to it. Such information includes the language, key phrases,
sentiment (0-1 as negative to positive sentiment), and entities.

Language identification supports many languages whilst key-phrases,
sentiment, and entities are limited to a few languages.

In addition to the demonstration this package provides a collection of
commands that turn the service into useful *command line tools* for
language identification, sentiment analysis, and phrase/entity
extraction.

Text analytics is used in many scenarios, including the analysis of
customer calls into a call centre, the analysis of survey results,
monitoring social media commentary on a subject, etc.

A free Azure subscription allowing up to 5,000 transactions per month
is available from https://azure.microsoft.com/free/. Once set up visit
https://ms.portal.azure.com and Create a resource under AI and Machine
Learning called Text Analytics. Once created you can access the web
API subscription key from the portal. This will be prompted for in the
demo.

This package is part of the [Azure on
MLHub](https://github.com/Azure/mlhub) repository. Please note that
these Azure models, unlike the MLHub models in general, use *closed
source services* which have no guarantee of ongoing availability and
do not come with the freedom to modify and share.

Visit the github repository for more details:
<https://github.com/gjwgit/aztext>

The Python code is based on the [Azure Text Analytics Quick
Start](https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python)

## Usage

- To install mlhub (Ubuntu 18.04 LTS)

```console
$ pip3 install mlhub
```

- To install and configure the demo:

```console
$ ml install   aztext
$ ml configure aztext
```

## Command Line Tools

This package supports the following command line tools: analyze,
language, sentiment, phrases, entities. The *analyze* commands
performs a basic analysis across the four capabilities with the other
commands dealing with each of the four capabilities.

**Text Analysis**

The *analyze* command takes a single sentence and returns the text
analysis of the sentence, beginning with the confidence of the
identified, the language, the level of positive sentiment, the key
phrases separated by colons, and the identified entities, separated by
colons.

```console
$ ml analyze aztext "I had a wonderful experience! The rooms were wonderful and staff helpful."
1.0,en,0.96,wonderful experience:rooms:staff helpful,

$ ml analyze aztext I had a wonderful trip to Singapore and enjoyed seeing the Gardens by the Bay
1.0,en,0.96,Singapore:Gardens:wonderful trip:Bay,Gardens by the Bay:Singapore

$ ml analyze aztext  这是一个用中文写的文件
1.0,zh_chs,0.75,,

$ ml analyze aztext Aku isa mangan beling tanpa lara.
1.0,id,,,

$ ml analyze aztext Los caminos que llevan hasta Monte Rainier son espectaculares y
1.0,es,0.55,Monte Rainier:caminos,Monte Rainier

$ ml analyze aztext La carretera estaba atascada. Había mucho tráfico el día de ayer.
1.0,es,0.33,carretera:tráfico:día,

$ ml analyze aztext मैं काँच खा सकता हूँ और मुझे उससे कोई चोट नहीं पहुंचती.
1.0,hi,,,
```

Note that sentiments, key phrases, and entities are not
available for all languages.

Without an argument the command will enter an interactive loop,
prompting for a sentence, and analyzing that sentence.

**Named Entity Recognition**

The *entities* command identifies the entities from the text together
with other information, including the type of entity and a Wikipedia
link. For each entity identified the output consists of a single line
reporting the entity name, the type of entity and sub-type, the
confidence of the type of entity, the offset to the entity in the
original text, then text length of the entity, the Wikipedia
confidence, language, entity name, and URL.

```console
$ ml entities aztext I had a wonderful trip to Seattle last week and even visited the Space Needle 2 times!
Seattle,Location,,0.82,26,7,0.24,en,Seattle,https://en.wikipedia.org/wiki/Seattle
last week,DateTime,DateRange,0.80,34,9,,,,
Space Needle,Location,,0.80,65,12,0.39,en,Space Needle,https://en.wikipedia.org/wiki/Space_Needle
Space Needle,Organization,,0.94,65,12,,,,
2,Quantity,Number,0.80,78,1,,,,
```
As part of a command line we could count the number of unique entities
in the text:
```console
$ ml entities aztext I had a wonderful trip to Seattle last week and even visited the Space Needle 2 times! |
  cut -d, -f1 |
  sort -u |
  wc -l
4
```

How many unique locations are identified in the text:
```console
$ ml entities aztext I had a wonderful trip to Seattle last week and even visited the Space Needle 2 times! |
  awk -F, '$2=="Location"{print}' |
  cut -d, -f1 |
  sort -u |
  wc -l
2
```

**Key Phrase Extraction**

The *phrase* command extracts the key phrases from the supplied text.


**Text Sentiment Analysis**

The *sentiment* command determines how positive the text is on a scale
from 0 (negative) through 0.5 (neutral) to 1 (positive).

```console
$ ml sentiment aztext The weather here is cold and dreary
0.17

$ ml sentiment aztext had a great trip and all went really well
0.97
```

**Linked Entities Markup**

The *links* command will return the text as is but with entities that
have Wikipedia pages marked up with HTML to link to the appropriate
page. This is particularly useful in writing web pages within which
you want to have links to Wikipedia.

```console
$ python3 links.py <<END
The Internet (interconnected networks) is the
backbone of all communications and most services used today. Home,
local and international networks provide access to resources beyond
the local desktop computer, laptop, smartphone, or thing (as in the
internet of things). Most computers (including smartphones) connect
either through Ethernet (named in recognition of the nebulous aether
world out there) whereby the connection is by wire, or through WiFi
(as in HiFi but for computers) to connect wirelessly. On connecting to
the Internet a unique address, called the IP address (Internet
Protocol), is assigned to the computer.
END
```
This will generate HTML marked up text that will be rendered as:

<ul>
<a href="https://en.wikipedia.org/wiki/Internet" target="_blank">The
Internet</a> (interconnected networks) is the backbone of all
communications and most services used today. <a
href="https://en.wikipedia.org/wiki/Home_directory"
target="_blank">Home</a>, local and international networks provide
access to resources beyond the local desktop computer, laptop,
smartphone, or thing (as in the internet of things). Most computers
(including smartphones) connect either through <a
href="https://en.wikipedia.org/wiki/Ethernet"
target="_blank">Ethernet</a> (named in recognition of the nebulous
aether world out there) whereby the connection is by wire, or through
<a href="https://en.wikipedia.org/wiki/Wi-Fi" target="_blank">WiFi</a>
(as in <a href="https://en.wikipedia.org/wiki/High_fidelity"
target="_blank">HiFi</a> but for computers) to connect wirelessly. On
connecting to the Internet a unique address, called the <a
href="https://en.wikipedia.org/wiki/IP_address" target="_blank">IP
address</a> (Internet <a
href="https://en.wikipedia.org/wiki/Communication_protocol"
target="_blank">Protocol</a>), is assigned to the computer.
</ul>

# Demonstration

```console
$ ml demo aztext 

==================== 
Azure Text Analytics
====================

Welcome to a demo of the pre-built models for Text Analytics provided
through Azure's Cognitive Services. This service extracts information
from text that we supply to it, providing information such as the
language, key phrases, sentiment (0-1 as negative to positive), and
entities.

The following file has been found and is assumed to contain
an Azure Text Analytics subscription key and region. We will load 
the file and use this information.

/home/gjw/.mlhub/aztext/private.py

Press Enter to continue: 

====================
Language Information
====================

We will first demonstrate the automated identification of language. Below
are a few "documents" in different languages which are passed on to the 
cloud for processing using the following language API URL:

https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/languages

Press Enter to continue: 

1 This line is some text as a sample document written in English.
  This is English (en) with score of 1.0.

2 Este es un document escrito en Español.
  This is Spanish (es) with score of 1.0.

3 这是一个用中文写的文件
  This is Chinese_Simplified (zh_chs) with score of 1.0.

4 Nor for itself hath any care.
  This is English (en) with score of 1.0.

5 Nor for itself es un escrito 这是.
  This is Spanish (es) with score of 0.75.
  NOTE: the text is rather jumbled hence a lower score.

6 Τη γλώσσα μου έδωσαν ελληνική
  This is Greek (el) with score of 1.0.

7 मैं काँच खा सकता हूँ और मुझे उससे कोई चोट नहीं पहुंचती.
  This is Hindi (hi) with score of 1.0.

8 Aku isa mangan beling tanpa lara.
  This is Indonesian (id) with score of 1.0.
  NOTE: a little tricky as it is actually Javanese.

9 ฉันกินกระจกได้ แต่มันไม่ทำให้ฉันเจ็บ
  This is Thai (th) with score of 1.0.

10 Ich canne glas eten and hit hirtiþ me nouȝt.
  This is English (en) with score of 1.0.
  NOTE: yes it is actually Ye Olde English.

That's the end of the language identification. Press Enter to continue: 

==================
Sentiment Analysis
==================

Now we look at an analysis of the sentiment of the document/text. This is
done so by passing the text of the document on to the sentiment API URL
shown below for processing in the cloud. The results are returned as a number
between 0 and 1 with 0 being the most negative and 1 being the most positive.

https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment

Press Enter to continue: 

1 I had a wonderful experience! The rooms were wonderful and the staff
  were helpful.
  This has a sentiment rating of 0.97.

2 I had a terrible time at the hotel. The staff was rude and the food
  was awful.
  This has a sentiment rating of 0.00.

3 Los caminos que llevan hasta Monte Rainier son espectaculares y
  hermosos.
  This has a sentiment rating of 0.75.

4 La carretera estaba atascada. Había mucho tráfico el día de ayer.
  This has a sentiment rating of 0.33.

That's the end of the sentiment examples. Press Enter to continue: 

===========
Key Phrases
===========

We are often interested, for further analysis, in the key phrases of a 
document. Here we extract what are considered to be the key phrases of
the document. Again, the text is passed on to the cloud through the API
at the URL below.

https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases

Press Enter to continue: 

1 I had a wonderful experience! The rooms were wonderful and staff
  helpful.
  The key phrases here are: ['wonderful experience', 'rooms', 'staff helpful'].

2 I had a terrible time at the hotel. The staff was rude and the food
  was awful.
  The key phrases here are: ['food', 'terrible time', 'hotel', 'staff'].

3 Los caminos que llevan hasta Monte Rainier son espectaculares y
  hermosos.
  The key phrases here are: ['Monte Rainier', 'caminos'].

4 La carretera estaba atascada. Había mucho tráfico el día de ayer.
  The key phrases here are: ['carretera', 'tráfico', 'día'].

That's the end of the key phrases. Press Enter to continue: 

========
Entities
========

Our final demonstration identifies the entities refered to in the document.
As a bonus the API generates a link to Wikipedia for more information! As 
above, the text is passed on to the cloud through the API at the URL below.

https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/entities

Press Enter to continue: 

1 Jeff bought three dozen eggs because there was a 50% discount.
  Jeffster!:	https://en.wikipedia.org/wiki/Jeffster!.
  Egg:	https://en.wikipedia.org/wiki/Egg.

2 The Great Depression began in 1929. By 1933, the GDP in America fell
  by 25%.
  Great Depression:	https://en.wikipedia.org/wiki/Great_Depression.
  United States:	https://en.wikipedia.org/wiki/United_States.
  Gross domestic product:	https://en.wikipedia.org/wiki/Gross_domestic_product.

3 I had a wonderful trip to Singapore and enjoyed seeing the Gardens by
  the Bay!
  Gardens by the Bay:	https://en.wikipedia.org/wiki/Gardens_by_the_Bay.
  Singapore:	https://en.wikipedia.org/wiki/Singapore.

Press Enter to finish: 
```
