Azure Text Analytics
====================

This [MLHub](https://mlhub.ai) package provides a quick introduction
to the pre-built Text Analytics models provided through Azure's
Cognitive Services. This service extracts information from text that
we supply to it. Such information includes the language, key phrases,
sentiment (0-1 as negative to positive sentiment), and entities.

A free Azure subscription allowing up to 5,000 transactions per month
is available from https://azure.microsoft.com/free/. Once set up visit
https://ms.portal.azure.com and Create a resource under AI and Machine
Learning called Text Analytics. Once created you can access the web
API subscription key from the portal. This will be prompted for in the
demo.

Please note that this is *closed source software* which limits your
freedoms and has no guarantee of ongoing availability.

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
    $ ml score     aztext

Do note that sentiments, key phrases, and entities are not available
for all languages.
    
Further Information
-------------------

For language translation see the azlang package.
