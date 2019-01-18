Azure Text Analytics
====================

This [MLHub](https://mlhub.ai) package provides a quick introduction
to the pre-built Text Analytics models provided through Azure's
Cognitive Services. This service extracts information from text that
we supply to it. Such information includes the language, key phrases,
sentiment (0-1 as negative to positive sentiment), and entities
(person, organisation, a quantity, date and time, a URL, or an email
address), as well as translation.

A free Azure subscription is available from
https://azure.microsoft.com/free/. Once set up visit
https://ms.portal.azure.com and Create a resource under AI and Machine
Learning called Text Analytics. Once created you can access the web
API subscription key from the portal. This will be prompted for in the
demo.

Please note that this is a *Closed Source* cloud-based API accessible
offering with a free tier of some 5000 transactions per month. If this
service demonstrates value then pricing begins from $2 per 1,000 text
records, reducing with volume.

Visit the github repository for more details:
<https://github.com/gjwgit/aztext>

The Python code is based on the [Azure Text Analytics Quick
Start](https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/quickstarts/python)

Usage
-----

To install and run the pre-built model:

    $ pip3 install mlhub
    $ ml install   aztext
    $ ml configure aztext
    $ ml demo      aztext

Further Information
-------------------

	