---
title: "Hello, World!"
description: "TLDR: 30 member tech team formed over seven years built India's largest stock broker. Unconventional setup. The long pending tech blog is finally here. Some backstory and context."
date: "2020-04-06T00:00:00+05:30"
author: knadh
authors: ["knadh"]
tags: ["philosophy", "dev-culture", "tech-team"]
image: "/static/images/product-mashup-2020-04.png"
---

[Zerodha](https://zerodha.com), now India's largest stock broker, bootstrapped and profitable, turns ten years old this year. The Zerodha tech team turns seven years old. The tech team has remained largely elusive over the course of our existence. While we have pondered starting a tech blog for more than half a decade, we have often found ourselves too busy building the fundamental blocks underlying a stock brokerage. We have also been stalled by a sense of unpreparedness to talk to the world about our very unconventional setup.

But now, equipped with the power of battle-tested hindsight, the blog is finally here, and we hope to share what we have built, how we have built, and what we have learnt over the years.

**TLDR:** 30 member tech team formed over seven years built India's largest stock broker. Unconventional setup. The long pending tech blog is finally here. Some backstory and context.

[![Products](/static/images/product-mashup-2020-04.png)](https://zerodha.com/products)

## The origin

Zerodha was founded in 2010 as a small discount broking firm in Bangalore by two brothers and life-long traders, [Nithin](https://worldsmosthandsomebroker.com) and Nikhil Kamath. In 2012, I was roped into building an investment app by an old friend from school, and by complete happenstance, we discovered Zerodha  just because their office happened to be in the same vicinity where we would hangout.

By early 2013, we had stopped working on the app and had gone our separate ways after failing to get regulatory approvals. If it were today, we would have obtained the necessary approvals as the regulators are exponentially more tech savvy today than they were in 2013. I decided to stick on, primarily due to the sheer astonishment at the state of all things tech in capital markets then (none, that is), the excitement of building software in an *untouched* area, and really though, because Nithin and I got along really well. I had been a hobbyist developer / hacker for over a decade at that point, and it felt like I could continue being that, building software, despite being in a "corporate" setting, something I had always been skeptical about. 

And build, we did. We founded the tech team in mid-2013. At that point, Zerodha  had around 75 employees. Today, the tech team is 30 members strong, and the rest of the company has grown to ~1200 people across various departments like sales, operations, support, and compliance. Stock broking, especially in India, is a complex and hard gig.

## The tech team
The tech team has two mobile developers, two designers, two frontend developers, one test engineer, one devops engineer, and one liaison who helps us keep track of communication with other sprawling departments. The rest of us, including the aforementioned members who focus on specific areas, are fullstack developers who do pretty much everything. There are no dedicated project or product managers, and developers step up to these roles and natural leaders emerge. Products and technologies are built, maintained, and owned by small teams of two to four developers, and there are several overlaps between these micro teams.

Nobody in the team has any background in finance, and apart from a handful of developers, most have no prior work experience either. Everyone has been a hacker or a hobbyist straight out of college. What colleges, neither do we ask, nor do we keep a track of.

That a 30 member tech team has built and scaled a complex financial + stock broking stack from the ground up, built a whole suite of financial software for end users that people actually appreciate in an extremely complex, constraining, and rapidly changing regulatory environment, with zero prior industry knowledge, is quite a feat. More of an anomaly than a feat. I, however, find it natural and poignant that a group of hackers in the right environment guided by the right philosophies can be incredibly creative and productive, even in a place as unfashionable and uncool as the Indian stock broking industry. What used to be the norm—small groups of hackers building good software—has now transmogrified into being the exception.

## Scale
Zerodha became the largest stock broker in India in January 2019, trumping stock brokerages operated by mega-banks. We achieved this slowly and organically. We have never raised external funding, have zero debt, and have been profitable YoY. We do not have a marketing team, have not advertised anywhere, and have let our services and products speak for themselves, building our userbase, brand, and trust over the years.

Today:

- 15-20% of all daily retail trade and investment volumes across all Indian stock exchanges pass through our apps.
- We have ~1 million daily active users placing millions of trades in realtime across various Indian exchanges, totalling to over $3 billion in volumes. In early March when Charles Schwab (US) [reported](https://www.aboutschwab.com/cfo-commentary) a new record of 2.7 million trades in a day, we did 7+ million trades. Of course, the comparison is on the scale of activity, and not on the quantum (USD vs. INR) of trades. In the last financial year that just ended, we executed more than 1 billion trades.
- Our systems process hundreds of thousands of requests per second during peak market hours. We broadcast ~16 million market ticks per second to hundreds of thousands of concurrent users. Thanks to careful byte-by-byte optimisations, the bandwidth bills are negligible.
- We construct and serve detailed portfolio reports, breakdowns, and visualisations instantly from our Postgres nodes that store hundreds of billions of rows of investment records.

## Stack
Here is a quick, broad, overview of our stack, before we start getting into deep-dive posts in the near future.

- All of our performance-critical, high throughput services are written in Go. We have not received any unsolicited advice asking us to rewrite everything in Rust or Nim (yet).
- Data-heavy backoffice systems where realtime performance is not a bottleneck, are written in Python. Django and Flask for certain web apps.
- Bit of C++ and Java for special cases.
- Countless complex business, financial, account, people processes and backoffice applications are built atop [ERPNext](https://erpnext.com). Thank universe for ERPNext.
- VueJS for web app applications. Gave up on Angular and rewrote all applications.
- Flutter for iOS and Android mobile applications. Gave up on native Android/Java, Swift, and React Native and rewrote everything in Flutter. Granted, there is still one React Native app.
- Self-managed Postgres instances with hundreds of billions of rows. MySQL instances with billions of rows as owing to certain dependencies.
- Self-managed Redis instances in high throughput hotpaths. There are few pieces of software that are so unbelievably automagical.
- Haproxy and Nginx for proxying, load balancing, and routing.
- Kafka for realtime events and as an organisation-wide message bus.
- Self-hosted Gitlab, RunDeck, RocketChat, Metabase, Phabricator, Postal etc.
- Have started experimenting with K8s recently to make service deployments uniform.
- Minimal "AI/ML" for image and document recognition as an aid to operations.
- Sentry, Grafana, and Prometheus for infra-wide systems and app metrics and monitoring.
- ELK stack for logs, where storing terabytes of searchable logs for several years is a regulatory requirement.
- Hybrid infra. Physical racks where numerous exchange leased lines terminate + AWS. Sometimes, these leased lines go down when the civic body in Mumbai digs up roads.

## Guiding principles and philosophies
These are some of the broad guiding principles that have happened to work for us.

- Neither large teams for the sake of "growth", nor *10x ninja* developers, are meaningful. What matters is that a group of good developers, no matter how small, are able to work well together.
- Rigid methodologies tend to fail. People, teams, requirements, and environments are infinitely different and dynamic. A methodology unique to an environment and a team has to be modeled, in the same vein as "*right tool for the right job*".
- Tech stacks should follow "*right tool for the right job*" and should evolve organically. One probably does not need a cluster of K8s clusters (or K8s or Docker at all), or an end-to-end CI/CD platform powered AI and Blockchain on day one, or ever. Every choice made in adopting a technology has serious long term ramifications.
- Keep the code and stack as non-fancy and simple as possible. Heavy on common sense and light on coolness. For example, avoid microservice hells and monolith monsters with the right trade-off.
- FOSS-first. FOSS-only, really. We use and produce FOSS (and this year, we're starting a FOSS fund).
- Don't be afraid to self-host. We self-host the company's employee intranet and HR systems, support ticketing and CRM, internal forum and chat systems, financial backoffice and accounting applications, monitoring and logging infrastructure, mail servers, databases, proxies; pretty much everything. Everything with role-based access controls and granular permissions behind OAuth + 2FA. For developers, password-less certificate based SSH logins. All FOSS.
- A tech team should be run with a developer-centric approach, and not a business or management-centric one.
- Technical decisions, even the ones with business implications, should be made by technical people. Otherwise, in comes the feature-creep, bloat, technical debt, and burnouts.
- Absolutely every decision—people, technology, operational, product—is a trade-off. Every trade-off should strike a balance between the right technical and business facets, developer and management teams, and products and end users. Making the right trade-off is an art.
- Be extremely wary of technical debt. Know when to scrap and rewrite systems. We have scrapped and rewritten the majority of our stack, including our critical trading platforms, multiple times, improving them significantly with each iteration. These are tough decisions; extremely important trade-offs. Of course, non-interference from non-technical management is incredible luck. 
- Always experiment. Experiments have turned out to be major product successes for us.
- Structure the organisation and organisational processes like standalone, inter-operable units of a well architected software system. On the 12th of March 2020, owing to the COVID-19 emergency, we were able to go fully remote overnight for all ~1200 employees across all departments. There was minimum hassle, thanks to how we had structured and architected the whole organisation's workflows, systems, and interactions like a well designed, modular, software system.
- This approach also helped us open up the organisation as a set of APIs creating a ["Broking as a Platform"](https://kite.trade) system, enabling several startups to enter the investment-tech space by plugging into us, in turn, helping us kick start a [fintech fund](https://rainmatter.com) that has now invested in over a dozen startups.
- Build organic, meaningful relationships with non-tech teams within the organisation. We work with small non-tech teams within the organisation (subsets of support and finance) to critique and validate products, gather feedback and data, and to do QA from a finance perspective.
- Be extremely particular about quality and consistency. That extra 50 KB of Javascript, or that 100 KB PNG on a web app, or that sudden 10ms spike in mean latency, are not acceptable. No matter how negligible the cost may be, it is a matter of principle of good engineering. It is okay to pause for a bit to do things the better way.
- Good design is paramount. Building software for humans with no consideration for human interactions and sensibilities is criminal. Keep UIs and interactions simple, typography crisp, clutter minimal, and spacing calm. We keep iterating for as long as it takes to strike the right balance between "aesthetically pleasing" and "easily usable".
- Consider technology costs as engineering challenges. Always optimise where possible and don't spend what is not absolutely necessary. Frugality and moderation should be second nature to hackers.
- Not every line of code that is written is going to be ingenious or innovative, and much of the work can be often tedious. That is how the real world works and is a fact that every developer should accept and internalise.
- A developer should dabble in everything (frontend, backend, testing and QA/QC, infrastructure, devops), and build focus gradually and naturally. 
- Don't be afraid to do feature-freezes to build tech the better way. It is okay to slow down to build cleanly, as what is built now will have serious implications in the future. The "time-to-market" fervour is often overhyped and short-sighted. This has never been an impediment to us. In fact, following this approach has allowed us to build and take a large number of things to market at an incredible pace.
- Trust developers and tolerate (even terrible) mistakes. The key is in learning by trial and error and not repeating the same mistakes. Not everyone is a *10x hotshot ninja*, and that is okay. Everybody has their own critical role to play. Be patient and let talent grow. If someone fails to respect this and keeps repeating the same mistakes, then they probably won't cut it. Fortunately, we have had very few instances of this.
- It is important for developers to find work meaningful to remain creative and productive. Everybody in the team has various systems that they have built and own, maintain, control, and are responsible for. In addition, we have an ESOPs program that increments a team members' ownership of the company as they mature and grow in their roles—ESOPs whose value is derived from actual profits. This is in addition to a share of the fintech startup investments. This obviously did not become possible on day one (we never took external funding). We have gotten here gradually, thanks to how the team and the business have evolved.
- All discussions are open to everyone; casual, technical, or political.
- Having fun is extremely important. If there is an opportunity to make things fun, irrespective of how "serious" the status quo of an environment is, things should just be made fun. What matters at the end of the day is the quality of work. "Non-stop memes and burns a day, help keep the stress and tedium away". We have been playing Counter Strike Condition Zero (1.6) LAN matches on Steam every evening without fail for over five years now. Never gets old, except for getting shot in the head mercilessly by n00bs.
- Our work, products, failures, and even successes, are to be made fun of. Nothing is sanctimonious. There's a meme in everything. This has helped us cope with the ire from downtimes we have faced in the past, stemming from elements outside of our stack and control. 
- Realise that nothing is absolute and everything is absurd (see the COVID-19 world). There are no rules to building a healthy and successful team. Common sense + effort + fun + luck.
- Accept and appreciate luck. The countless tiny decisions and trade-offs that have resulted in a successful outcome, is luck as much as it is code. Of course, the odds are proportional to the amount of work and passion invested. That we ended up in the right environment (no tech vs. management divide. Thanks [Nithin](https://worldsmosthandsomebroker.com).), that our products worked, that we are in a position to do what we love, earn a living, and have fun, is luck.
- Again, absolutely nothing is absolute, and everything is a trade-off.

In all honesty, as a hobbyist developer with no prior experience working in a corporate structure or managing a team, I did not have anything to go by except for the hacker-first approach, and great luck in finding like-minded hackers who can meme-burn all day long, while continuously learning and producing quality work.


## What's next?
I am excited by the prospects of this blog. It has been long overdue. We are eager to use Zerodha as a case study to illustrate that it is possible to build not just good software, but large enterprises ("Unicorns"), with small teams of hackers, even in the unlikeliest of industries. Hopefully, members of the tech team will start finding time to make semi-regular appearances on this blog with their own experiences and technical insights.

*9th April 2020: Minor edits.*
