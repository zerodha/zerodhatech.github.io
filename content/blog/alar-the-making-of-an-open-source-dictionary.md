---
title: "Alar: The making of an open source dictionary"
description: "The story of a massive Kannada dictionary created by V. Krishna single handedly over four decades, and its accidental discovery and open sourcing at an unlikely place, a stock brokerage."
date: "2020-09-22T00:00:00+05:30"
author: knadh
authors: ["knadh"]
tags: ["philosophy", "data", "foss"]
image: "/static/images/alar.png"
---

ನಮಸ್ಕಾರ (Namaskāra)! This is not a post on fintech, or even technology for that matter. This is the story of a product of tenacity, selflessness, and passion; a product that will transcend and outlive most technology we know of. This is the story of a massive dictionary that will become the window to a language spoken by tens of millions of people for generations to come, a resource its author has donated to posterity. This is the story of V. Krishna, [*Alar*](https://alar.ink), his Kannada-English dictionary, and its accidental discovery and open sourcing at an unlikely place, a stock brokerage, Zerodha. This post is also a personal note, something I have not attempted in a long time.

### Prologue
I have been running [Olam](https://olam.in), an English-Malayalam and Malayalam-Malayalam dictionary, since 2010. It was built out of the frustration of not having an easily accessible online Malayalam dictionary, of the frustration at dictionary websites that insulted the reader's intelligence with poor usability, terrible ad-ridden spamminess, and no respect for language. Olam's website has stayed exactly the same for 10 years. It has an input box that responds to dictionary lookups in under \~50ms, exactly as it did in 2010. It is actively used by millions of Malayalam speakers.

The first version of the Olam corpus was seeded with unattributed word lists I scraped together from random parts of the web, and several thousand entries I entered myself. Since then, the English-Malayalam dictionary has been expanding slowly with crowdsourced entries.

The entire Olam corpus is [open source](https://olam.in/open) (licensed under [OdBL](https://opendatacommons.org/licenses/odbl/summary/)), or open data, rather. While the English-Malayalam corpus is crowdsourced, the Malayalam-Malayalam corpus (now known as the *Datuk Corpus*) was created out of the mammoth digitisation project the late ["Datuk" K. J. Joseph](https://www.asianetnews.com/pravasam/datuk-kj-joseph-passes-away-pm1xdr) undertook in the late 90s, when he single-handledly digitised an out-of-copyright Malayalam-Malayalam dictionary along with many other books and posted them online at the expense of copious amounts of time out of his retirement. He was a Malayali settled in Malaysia, a prominent active social worker and educator. The Malaysian government conferred the title "Datuk" upon him in recognition of his exemplary services in the country, which then ended up being his nickname too. I do not know of the origin of the dictionary Datuk digtised, but it is poignant to think that the original author's work lives on after a century.

I discovered the RTF file Datuk had posted a decade prior on an inactive Yahoo groups page around the time I was working on Olam. Needless to say, I was stumped by the scope of this project, and immediately started working on integrating it into Olam. It took more than two years of on and off work to convert the text from the original ASCII input to Unicode, and to clean, structure, and correct close to 200,000 entries. The dataset was named *Datuk Corpus*, and was published on Olam in 2013. I wrote to the Swathanthra Malayalam Computing (SMC) mailing list [announcing it](http://lists.smc.org.in/pipermail/discuss-smc.org.in/2013-May/015592.html), and we launched it with some fanfare at the SMC conference held in Thrissur, Kerala, that year. Datuk's story was covered by the press, and his work was now open and available to everyone.

Shortly thereafter, I was connected to Datuk by an old friend of his I had met at the conference, and we spoke briefly on the phone. He had seen the news clip of the dictionary's release, and was thrilled to know that his work was now accessible as he had originally intended. Open data lives on. He found it amusing that a random stranger had somehow unearthed a relic he had lost to the annals of internet history. Life is absurd like that, shaped in infinite ways by tiny, random events.

Datuk [passed away in January 2019](https://www.facebook.com/amma.org.my/posts/tribute-to-the-late-datuk-k-j-josephthe-late-datuk-k-j-joseph-was-a-prominent-ed/2157527197640248/). He was 89 years old. RIP Datuk. Your work's utility will span generations. The data you created will proliferate and continue to be useful to humanity in ways we never imagined. Such is the beauty of open data. I consider it a privilege to have been able to speak to you just that one time.

### Open data
> [Open data](https://en.wikipedia.org/wiki/Open_data) is the idea that some data should be freely available to everyone to use and republish as they wish, without restrictions from copyright, patents or other mechanisms of control.

I shudder to think of a world without Wikipedia. The open data movement shares strong parallels with the Free and Open Source Software (FOSS) movement. The gist is that certain knowledge should be freely available to everyone with no restrictions and with one goal—collective advancement of humanity.

I consider dictionaries to be on top of that list. The stepping stone to language, the underpinning of civilisation. Dictionaries should be open, free, and easily accessible to everyone, everywhere. If we cannot share something as fundamental as language without motives of profit, we ought to do some serious introspection as members of an advanced civilisation.

An open data dictionary for every Indian language, the largest collection of open source dictionaries in the world, would be an immense resource for not only India but for humanity in general. Ideally, this is the kind of project governments should do. State governments could very easily partner with local universities and undertake the creation and maintenance of open data dictionaries.

That said, at Zerodha, we would be happy to fund projects to create high quality open data dictionaries if there are scholars out there working on them.

### A Kannada dictionary
I moved from Kerala to Bengaluru in early 2012 to get access to fast internet. Bengaluru is a melting pot of people from all over India, and English is the glue that holds the "IT sector" together. I can comprehend Kannada speech reasonably well and speak rather poorly, but cannot read the script, thanks to the lack of opportunities to learn over the many years spent between home, where we speak Malayalam, and work, an English speaking environment. With the guilt of not being able to learn Kannada, and the great satisfaction of having Olam as an open data corpus, I had been looking for ways to build a Kannada dictionary right after I had moved to Bengaluru.

Sometime in 2016, I presented the idea of having an open source Kannada dictionary created from scratch to Nithin. He was immediately on board to commission the project. A perk I enjoy, the privilege of having a resourceful backer who believes in public good. Not knowing where to start, I asked around a few places but nothing materialised for the next two years, and as always, I continued to bring up this conversation once in a while.

Then, sometime in October 2018, I randomly brought up the conversation again, and Srihari, who had just joined the tech team, happened to overhear it. He vaguely remembered that someone in his family had been associated with a dictionary for a long time. This would be one of those minuscule, random events that would significantly change the timeline; the [Butterfly effect](https://en.wikipedia.org/wiki/Butterfly_effect) in action. I crossed my fingers and he soon setup a meeting with V. Krishna, the relative of his. Shortly thereafter, Srihari, Sharath (also from the tech team), and I went to [KaGaPa's](http://www.kagapa.in) office to meet V. Krishna and to find out what exactly it was that Srihari remembered about him and a dictionary. KaGaPa (Kannada Ganaka Parishat) created the popular Nudi font and input method for Kannada, an important early innovation for digital Kannada, and V. Krishna had worked with them on several projects.

V. Krishna and Narasimhamurthy, KaGaPa's secretary, spoke passionately about Kannada literature and digitisation projects in the quaint little office room, surrounded by stacks of old Kannada books and literature. It was the perfect setting. Then, the extremely soft-spoken and mild-mannered V. Krishna fired up a computer and showed us his lifelong side project, his Kannada-English dictionary. Researched and written over a period of more than 40 years, 150,000+ Kannada words and 240,000+ English definitions, all neatly typed up in a Word document, complete with parts of speech tags and phonetic notations with diacritics for Kannada words. The ambition of the project, its scholarly quality, the depth of the data, the culmination of one man's passion, perseverance, and tenacity over a lifetime, all lying in obscurity, stumbled upon by sheer coincidence. Absolutely mind blowing.

### V. Krishna

{{< figure src="/static/images/vkrishna-alar.png" alt="V. Krishna's photo" height="150" class="float-right" >}}

V. Krishna was born in 1950 in the Malanayakana Halli village in Mysore district in Karnataka. He studied in a Kannada medium school, followed by a year at a pre-university college that he was forced to drop out of before moving to Bengaluru with his family in 1968.

He found a job at the Indian Agricultural Research Institute (IARI) in 1970. At IARI, around this time, noticing him struggle with the English language, his boss casually suggested that he procure a dictionary to learn English. This conversation would turn out to be pivotal, and would set V. Krishna on a lifelong journey of language research and scholarship, an amazing case of autodidacticism.


So, he took his boss's advice and got himself an English dictionary and started studying it. Then he got himself another dictionary, and another, until he had five of them. At the same time, he took an interest in Kannada literature and started studying Kannada and English together. To help with this, he started jotting down notes, and at some point, began structuring them. A dictionary was being born. In the meanwhile, he took evening classes and obtained a commerce degree in 1976 from MES college, Malleshwaram.

Around 1980, [Kannada Sahitya Parishattu](https://en.wikipedia.org/wiki/Kannada_Sahitya_Parishat) published a Kannada - English dictionary, and unsurprisingly, V. Krishna got himself a copy. He was surprised by the sheer number of errors he spotted—more than 200 in the first 50 pages. He wrote to the editor with his findings, and impressed by it, the editor met him in person in Bengaluru, where V. Krishna presented his manuscripts to him. Surprised by its quality, he suggested that V. Krishna continue his work and turn it into a full-fledged dictionary. This was the nudge that made him realise that his notes could become an actual dictionary. The rest is of course, history.

By the late 1990s, he had completed most of the dictionary. However, juggling paper manuscripts had become cumbersome. 100 pages worth of edits and re-writes to produce 15 pages of clean data. So, in 1999, he bought a personal computer with the intention of digitising his manuscripts. A gamble, for this was a time when personal computers were an expensive rarity. He then wrote to [C-DAC](https://en.wikipedia.org/wiki/Centre_for_Development_of_Advanced_Computing) seeking help in setting up a word processor that allowed Kannada input. Someone from C-DAC showed up to install the Kannada input software, a transaction that cost him ₹10,000, a hefty sum in 1999, only for the software to not work at all.

Then, in 2001, V. Krishna came across a newspaper article on Nudi, KaGaPa's Kannada input software. He got in touch with KaGaPa, starting a long association. Equipped with Nudi, V. Krishna embarked on the final phase of his dictionary project, digitisation. He taught himself how to type in Kannada using Nudi, and for the next eight years, kept at it. In 2010, he finished digitising the manuscripts, once again, single-handedly. By then, he had been working on his dictionary for more than four decades across multiple full time jobs (State Financial Corporation, Reckitt and Coleman, Jyoti labs). He retired from active work in 2015.

I find it fascinating that Datuk and V. Krishna, both unknown to each other and worlds apart, were working on mammoth dictionary digitisation projects of two classical Dravidian languages around the same time. Both, driven by passion.

Since the mid 1990s, V. Krishna has approached numerous universities in Karnataka in hopes of getting his dictionary published and into the hands of people, only to be shown no interest or to be outright turned down. At one point, he secured a grant from the government to get the dictionary published, but it never materialised. In 2015, Karnataka Sahithya Parishath did a small publishing run and came out with three physical volumes of the dictionary spanning 4700 pages. V. Krishna remains appreciative of the publisher's attempt.

**

This is the summary of the hour long interview of V. Krishna I did over the phone on the 26th of September, 2020. Towards the end, I asked him *"Sir, would you mind telling me your age?"* and he laughingly quipped *"Why would I mind at all? I was born in 1950"*. He turns 70 this December. A lifetime dedicated to an intellectual pursuit. And just like with Datuk, I consider it a privilege to be associated with V. Krishna.

### Zerodha
At our first meeting in October 2018, V. Krishna had not only liked the idea of making his dictionary available online, but also open sourcing it. I did not have to persuade, but merely suggest.

Soon after, we invited V. Krishna and Narasimhamurthy to our office in JP Nagar. I had discussed with Nithin, the idea of providing a scholarship to V. Krishna. In his classic fashion, during the meeting, Nithin not only offered a grant to V. Krishna in appreciation of his work, but to KaGaPa for its contributions to Kannada digitisation projects. In addition, he offered V. Krishna a perpetual, unconditional monthly stipend to support his passion, working on his dictionary. Here is the kicker—he is now working on an English-Kannada dictionary and has recently completed all the *"A"* words.

And thus, Zerodha, a stock broker, became the backer and publisher of an open source dictionary, an extremely valuable language resource that is now available not only to readers, but linguists, researchers, and institutions everywhere. I am also certain that V. Krishna's dictionary is the first authoritative dictionary in the world to be open sourced by its author. A unique moment in history in itself.


### Alar

I've always liked the Malayalam word "olam" (wave). Short, two syllables, easy to pronounce, remember, spell, and type. I wanted a name with the same characteristics for V. Krishna's dictionary. There is something poetic about analogising the act of open sourcing something with that of a flower blooming. So I looked up "bloom" in the Word document he had shared, and stumbled upon "alar" (ಅಲರ್). A word that is as beautiful in its shape and pronunciation as it is in its meaning. V. Krishna liked it, and the dictionary now had a name—*Alar*.

The Word document was typed in the ASCII Nudi font with the head word, parts of speech, and definitions separated by spaces, one entry per line. This had to be parsed and structured, and the ASCII content had to be mapped and converted into Kannada Unicode. Thankfully, I found [this project](https://github.com/aravindavk/ascii2unicode/blob/master/knconverter) that helped with the latter. With additional scripting, heuristics, a lot of trial and error, and Sharath's help in mapping Kannada characters, the ASCII Word document was converted into a structured Excel sheet, making maintenance easier for V. Krishna. Over the next few months, he combed through every single entry in the dictionary again and applied corrections and improvements.

In the meanwhile, I figured that [MLPhone](https://github.com/knadh/mlphone), the phonetic indexing algorithm for Malayalam that was written to power search on Olam would pretty much work as-is for Kannada as well. The algorithm was ported to Kannada as [KNPhone](https://github.com/knadh/knphone). For any given Kannada string, it generates phonetic hashes that represents how the word sounds. For instance `ಅಂಕೆಸಂಖ್ಯೆ` (aŋkesaŋkhye) produces `A3KS3KY`. The idea is that words with minor spelling and phonetic variations will produce the same phonetic hash, thus making them indexable and searchable by how they sound and not by their spelling.

Irrespective of the lookup language of a dictionary, be it English, Kannada, or French, it boils down to looking for an input string in a database of strings. With English, this is easy with the multitude of string processing and search algorithms bundled into databases. With languages like Kannada or Malayalam, doing a Unicode substring lookup may not yield the best results, especially because of the high likelihood of spelling variations from tricky non-English input on devices. That's where a phonetic algorithm helps. For certain languages, it could be non-phonetic algorithms too. If this step of tokenisation can be abstracted, it is possible to build a dictionary engine that can work for any language, where everything is standardised—the layout, pagination, rendering, and glossaries—except for the search string tokenisation algorithm that can be plugged in. After a bit of tinkering, I wrote [dictmaker](https://github.com/knadh/dictmaker), an application for building and publishing dictionary sites and APIs for any language.

In September 2019, [https://alar.ink](https://alar.ink) went online. Then, a whole year zoomed past where I did not get an opportunity to pick up the pieces, until now. The peril of side projects. Thankfully, V. Krishna has been patient. The final piece, search suggestions, was implemented last week using [varnam](https://github.com/varnamproject). Kannada words can be searched by entering them phonetically in English. For instance, typing "hesaru" will show ಹೆಸರು as a suggestion. Of course, the real final piece would be the Alar mobile app, which Ajin from our team is porting from the mobile app that he built for [Olam](https://play.google.com/store/apps/details?id=com.olam&hl=en_IN).

So, that is the story of Alar and V. Krishna, the beauty of open data, and the incredible and infinite ways in which tiny, random events such as an overheard conversation, changes timelines, the Butterfly effect.

**Links:** [Alar dictionary](https://alar.ink), [Alar open data](https://github.com/alar-dict) (licensed under OdBL), [dictmaker](https://github.com/knadh/dictmaker).

**Updates:**

V. Krishna is finally starting to get some of the recognition he deserves.

- 9th Oct 2020. [Deccan Herald's feature on V. Krishna](https://www.deccanherald.com/metrolife/metrolife-your-bond-with-bengaluru/kannada-english-dictionary-online-after-four-decades-899393.html).
- 1st Nov 2020. Kannada magazine [Kannada Prabha's feature on V. Krishna](https://twitter.com/raveebhat/status/1322830282211225602).
- 1st Nov 2020. Kannada magazine [Prajavani's feature on V. Krishna](https://www.prajavani.net/artculture/article-features/alar-kannada-english-dictionary-by-v-krishna-karnataka-rajyostava-digital-era-775312.html).
- 1st Nov 2020. Kannada news paper [Suvarna News' feature on V. Krishna](https://kannada.asianetnews.com/state-government-jobs/alar-website-to-search-kannda-words-dpl-qj3nc3).
- 4th Nov 2020. Kannada TV channel [TV5's interview of V. Krishna](https://twitter.com/SwathiShastry/status/1323968510557450241).