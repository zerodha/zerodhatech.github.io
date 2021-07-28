---
title: "Scaling with common sense"
description: "A disorderly assortment of common sense ideas for scaling applicaions that we follow at Zerodha. TLDR: Simple scales. Scale application before infra. Keep networking and IO minimal."
date: "2020-06-14T14:00:00+05:30"
author: knadh
authors: ["knadh"]
tags: ["philosophy", "scaling"]
image: "/static/images/grafana-store.png"
---

"Scaling" is not a specific technique but an entire spectrum that stretches all the way from "Google scale" to the K8s cluster [Karan](/authors/karan) runs on a Raspberry Pi plugged into a 12V shaver outlet in his bathroom to encrypt his DNS queries for peak privacy, while he asks Alexa to dim the lights and play his favorite non-mainstream indie music.

It is a collection of practices unique and intimate to every organisation, and is the product of an infinite number of variables; the numerous domain-specific problems, the structure of the organisation, the nature of the people involved and their biases, countless engineering decisions and trade-offs, technical debt and history, ad infinitum.

That said, there are several, mostly trivial, common sense techniques and rules of thumb that help pluck the low-hanging fruits of typical scaling problems. This is specifically in the context of running software systems that serve concurrent user traffic and demand. I have been getting a number of *"how do I scale my service?"* queries lately, and hence, this assortment of conceptual and technical notes from practice and production at Zerodha, in no particular order. These should be consumed with a healthy and rational awareness of context and trade-offs.

## 1. Comparisons are almost always meaningless.
An application that serves 1000 requests per second of static data is not the same as one that serves data from a database. Querying a database with a billion time series data points is not equal to doing a full text search on a billion rows, or even a fraction of that. So, request rates or database sizes, or any such 1:1 comparisons across organisations are pretty meaningless. They only make sense within their specific environments.

For that reason, tutorials and articles that demonstrate great scale under narrow constraints (*"How we opened 10 million concurrent WebSocket connections with a potato battery" … while transmitting zero data*), while are good to satisfy academic curiosity, should not be treated as general purpose user manuals. Internal context and awareness is more useful to scaling than external validation.

## 2. Scaling starts with well built software.
A poorly written Python web service may be able to handle 1000 requests / second using $100 worth of resources, while a well written one may be able to handle the same rate with $25 worth of resources. Although the outcomes quantified strictly by numbers seem equal, they are not.

Scaling starts bottom-up with good code and good software. One moves on to scaling resources horizontally or vertically after exhausting all easy optimisations in application code. This goes a long way.

## 3. Eat healthy and exercise daily.
… is the non-tech equivalent of "premature optimisation is bad". Everyone has heard it, appreciates it, but finds it difficult to practise. In the beginning, focus on writing good-enough software. Then refactor and improve as time progresses. Trying to build for "web scale" on day one can turn out to be painful as the careful premature optimisations get thrown out of the window as the business and user requirements change unpredictably. Also, not every piece of all software has to be low latency and high throughput to begin with. On the other end of the spectrum is being lazy ignoring common sense principles leaving them for later.

## 4. KISS, don't be afraid, and boring > cool.
"Keep it Stupid Simple" is a paradoxical adage. It is conceptually so simple that it creates the irrational fear that complexity implies sophistication and simplicity implies primitiveness. The fear of missing out on "cool" and advanced technologies.

It is absolutely fine to write a couple bash scripts to rsync files to a remote server to get something up and running. It does not have to be containerised and deployed on a K8s cluster on day one. If an application can be kept up and running forever in this manner with no additional overhead, why not?

Complex technologies solve specific organisational problems more than generic technical problems. We started using Kubernetes recently, primarily to make application deployments uniform just as the process had started to grow complex, and not really to attain any sort of performance or scaling benefits. Such frameworks and abstractions come with their own cost to pay, and probably would not be a sensible trade-off in a small organisation. "Micro service hells" are a widespread symptom of this problem.

The feeling that one is not "advanced" (cool) enough because they are not using a certain technology or methodology must be a prime reason for over-engineered, over-complicated, and expensive infrastructure setups. Boring is generally battle-tested and well-understood sans novelty. At the end of the day, what matters is quality software that can be run with as little headache as possible, not the frameworks or methodologies they're deployed on.


## 5. The bottleneck is almost always the database.
97.42%* of all scaling bottlenecks stem from databases, and not from using `dict`s over `OrderedDict`s, strings over byte arrays, or nested function calls, which is what premature optimisation is. In the face of a database bottleneck, every other optimisation in an application pretty much immediately becomes immaterial.

A complex web framework in a complex language that can handle 500,000 "hello world" requests per second, when connected to a database that can only handle 1000 queries per second, can then only handle 1000 requests per second. If this database bottleneck cannot be improved, might as well use a simpler framework with less throughput to make life easy. It is important to understand the global bottlenecks, which almost always are databases, before making fine-grained optimisations and decisions.

## 6. RDBMS works, almost always.
97.42%* of all business problems can be reduced to CRUD, represented as relational data that need ACID guarantees and reporting that can be easily expressed as SQL. Very few problems need map-reduce or schemaless storage. This has more to do with the fundamental nature of businesses and business data than any technical underpinnings.

When a Postgres node—with at least one replica for high-availability—with proper logical partitions and indexes can hold hundreds of billions of records, terabytes of data, and still perform well, there is not necessarily a need to look for a distributed database sacrificing crucial RDBMS business features at the peril of re-inventing them in application code. When that hits a bottleneck, some re-structuring of data and a cluster may solve it for good. How many applications realistically need hundreds of billions of rows of business data in the first place?

That is, it is generally simpler to model and operate business data on battle-tested RDBMS and to rely on the strength of SQL than to reinvent shoddy RDBMS features in the application wasting valuable time.


## 7. Everyone forgets to index.
Speaking of RDBMS, "my database is slow" can almost always be attributed to poor indexing, poorly constructed queries, or poorly designed schemas. It makes sense to exhaust all possible optimisations—1) the schema and data representation; 2) indexing; 3) query planning; 4) database configuration—before going shopping for a whole new database system. An SQL `EXPLAIN` of a query is a good place to start. While SQL can get complex, learning it is worth it as it can move significant amounts of redundant business logic from the application code to the RDBMS, which is what it is designed to do in the first place. ORMs may be nice abstractions for simple use cases, but can rapidly turn into painful bottlenecks. Either they generate sub-optimal queries, or force one to contort gymnastically to produce complex, optimised queries. Rather learn SQL than some esoteric ORM language.

It is surprising how many RDBMS bottlenecks can be attributed to carelessness, not excluding 1) not using composite indexes, or not writing queries with fields in the proper order to align with composites; 2) using text values instead of enums; 3) Abusing `LIKE` queries. Easy fixes.

## 8. Don't use an RDBMS. What?
While RDBMS are great, barring the dramatic effect of the title, as said earlier, they are almost always the cause of bottlenecks in a typical database backed application than the application code itself. The fewer the queries that an application makes to a database, the faster it gets.

It is notoriously hard to make WordPress handle traffic spikes as it issues dozens of queries to the database on every single page load. It probably has to because it is a generic CMS. Most business applications are unlike that. They are purpose-built and can afford to remodel queries and plan data better to reduce the number of roundtrips to the database on hotpaths, like a user clicking on a button and waiting for a result. 

Every individual query is a network round trip to the database that involves sending the query to the database, the database planning and executing the query, and sending the data back over the network. If it is possible to combine multiple queries into a single query (nest, join, or using [CTEs](https://www.postgresqltutorial.com/postgresql-cte/)), it almost always gives a significant performance boost. Similarly, for insertions, updations, and deletions, if it's not easy to combine queries, they can probably be batched and committed in one shot, avoiding multiple network round trips.

## 9. Networking/IO is really hard. Network as little as possible.
In a complex software system, internal networking is also a manifestation of dependencies and the organisational structure. There must be a mathematical model somewhere that describes the ridiculous ways in which systems fail with every addition of a networked dependency.

Networking makes software problems worse by piling on complexities of bandwidth and congestion, routing, load balancing, service discovery, packet drops, timeouts and retries, port and descriptor exhaustions, kernel configuration, operational overheads, data serialisation and API woes, and an infinite number of other problems that nobody can ever foresee. There are of course platforms that promise to magically abstract all of this away, but there is always a cost to pay. Who watches the watchmen?

Given that these complexities are applicable when just two networked services talk to each other, that companies end up with microservice hells and complex intertwined service "meshes", for no objective reason, is astounding. It seems like a form of penance. [This](https://www.youtube.com/watch?v=y8OnoxKotPQ) is painfully real.

The common sense approach would be to have as few services and networked dependencies as possible. Have as few networked interactions, especially synchronous API calls, and roundtrips on application hotpaths as possible. It is far more productive to focus on scaling application and data than to waste time on avoidable networking complexities.

## 9.1. Connections are hard. Connect little, pool much.
Redis is so good that on a single connection, it can serve tens of thousands of requests serially, almost giving the illusion of concurrency while actually being single threaded. A network connection's capacity is only as good as the upstream's latency (time required for a single request), throughput (number of requests processed in a given window), and concurrency (number of requests that can be processed simultaneously).

Imagine a database with 10 concurrent workers that can each process one query per second. It does not matter if an application opens 100 or a 1000 connections to the database. Only 10 connections will actually be used, and only 10 queries will be processed in a second. The rest of the connections are just unnecessary resource hogs. This is a common mistake, setting large connection limits for networked systems like databases in hopes of better throughput. Always pool.

Opening and closing TCP connections have significant overheads. Making 10,000 HTTP requests to a service using 10,000 connections is slow, resource intensive, and unsustainable. Depending on the speed of the service, this throughput can be achieved with a pool keep-alive of 100 connections, or even 10. For networked systems, be it RDBMS or web services, optimal connection pool sizes should be figured out by evaluating latency and throughput.

As request volumes grow, connection pools start becoming visibly latency sensitive. We have web services that handle hundreds of thousands of requests per second using a few hundred connections in a pool as long as the request latencies are constant. However, the slightest increase in the latencies immediately render these pools useless, as the number of requests that can be served on a single connection reduces drastically causing connection pools to grow. Ironically, the latency increase upstream indicates its inability to process more requests in the first place, which means, the growing pool only makes matters worse, overloading upstream. In the meanwhile, a hundred thousand requests a second are piling up on the frontend, snowballing, and exploding all over. This is a deadlock with no out but for the upstream service to go back to processing requests at low latencies. This is obviously often fixed by restarting everything imaginable and crying profusely. Horizontally scaling may or may not help depending on where the bottleneck is, and how *bursty* the traffic spikes are. A 10x burst in traffic over a period of 10 seconds is quite common on a trading platform,

Imagine this happening in a microservice mesh of dozens of services. One wouldn't even know where to start crying, let alone start debugging. Sophisticated observation and tracing systems help, but they also require maintenance and scaling. Who watches the watchmen?

## 9.2. Latency is THE metric.
"One request per second per connection" is a nice rule of thumb for visualising capacity and designing services and networks as illustrated in the previous sections. The key here is the consistency of latency. As long as it's guaranteed that a request will always take one second and not two, it is possible to have build capacity for scale. If it is unpredictable, sometimes two seconds, and sometimes five seconds, the service is scale-dead on arrival.

Now, this is a hard problem where much of the engineering effort should be focused. This is the one metric where it may actually make sense to engineer top down. If one wants to handle 1000 requests a second, that is, 1ms latency on one request, engineer things behind that request to get it to 1ms. Or, scale horizontally by having 10 copies of the service each which has a 10ms latency, at increased complexity and expenses. It is a trade-off afterall.

Is it possible to guarantee consistent latency? It is difficult, but barring network latency, at least for certain types of database lookups (which coincidentally is 97.42%* of all service responses in the world), it is possible to get consistent O(1) and O(N) lookups offered by systems like Redis. Complex RDBMS lookups can be turned into into O(1) lookups in Redis with common-sense caching, and this can go a really long way.

## 9.3. The Internet is the Wild Wild West.
Imagine a well built, highly optimised, low latency service with high throughput that handles hundred thousand requests a second. One million concurrent users start sending requests to it from wildly varying 3G, 4G, and broadband networks over HTTP connections. The service will instantly respond to an incoming request on a connection, but the connection to the user over the internet is unpredictable. It may take 50ms or several seconds to write a response. For this period, the connection is held hostage by the user's poor network and it is happening with a million connections concurrently. This is an important factor that is easily missed.

A typical solution here is to deploy load balancer proxies (HAProxy, Nginx etc., or services like AWS ALB) setups for doing the dirty work of juggling a huge number of end user connections, maintaining a finite pool of keep-alive connections in the backend to the upstream service.

## 10. Caching is a silver bullet, almost.
RDBMS queries are expensive, multiple networked service lookups are expensive, computations are expensive, everything is expensive, until they are cached. If there is anything that comes close to a silver bullet in scaling services, it is caching. Even a poorly written application with a fast cache gets a chance to act like a well written application. Caching is indispensable and elementary to any sort of scaling, and in most cases, needs to be done aggressively.

Every bit of data that is shown on [Kite](https://zerodha.com/products/kite), our trading platform, comes from a "hot" Redis cache. Orders, positions, portfolio, absolutely everything. These are delivered as JSON responses to HTTP requests. An incoming get request does an O(1) lookup from an in-memory Redis instance, reads bytes, and dumps the bytes to the HTTP connection. There is no computational logic or JSON serialisation that happen in the hot path of most requests. Getting the data into Redis in the first place is the responsibility of an independent asynchronous service elsewhere. Disk persistence is turned off on these cache instances to get better performance boost and to not expend 2X RAM for persisting, whiling running multiple independent instances provide high availability and fault tolerance.

That an active investment platform generally only has to display data for the particular trading day is the silver lining here. RAM is cheap, Redis is pure magic, and it's trivial to have everything for the day, data for millions of users, kept in memory as a few hundred GBs worth of byte blobs. Every business has some sort of silver lining that can be hacked on.

Really though, how often does the data a user looks at on an application, change? Chances are, not very often, unlike stock prices that tick every second, for example. Even caching for a few seconds can make a big difference. Nothing beats caching in RAM, but not everything can be cached in RAM. What can be, the heaviest queries, or the most frequent responses, probably should be. If possible, cache forever, as long as invalidating the cache does not become overly complex. Generally, it's possible to cache all GET requests until a corresponding POST or PUT request on that resource internally invalidates the cache.

### 10.1. Dumb caching is best caching.
When a request looks up data in a cache and dumps it directly in the response, that's a dumb cache. The caching logic has no understanding of the semantics or structure of the data stored and just does bytes-out. Dumb caches are nice as the application logic need not concern with parsing or constructing data, which in turn may become its own bottleneck. While this may not be feasible everywhere, it is a nice way to keep things simple.


### 10.2. Some application state may not be bad.
That services should be to be stateless is a sensible gospel. That does not mean that an application can't have significant ephemeral in-memory cache.

Imagine a database table with 100K rows of data that rarely changes. A service queries one value from this table to fulfill incoming requests. What if the service, on boot, read the entire 100K rows from the database and put them in an in-memory map. Now the requests can do an in-memory map lookup, several orders of magnitude faster, with no dependency on the database. This is an ephemeral state that can be thrown away. On the rare occasion when the database changes, simply restarting the application can replenish the cache.

### 10.3. HTTP APIs can be E-Tagged (304) too.
That this is not widely is surprising to me. Client-side HTTP caching (JS, PNG, CSS …) is what underpins the large scale scaling of content delivery and bandwidth savings on the WWW. The browser caches a file, stores a hash, the E-Tag, and checks with the server if the file has changed by sending the E-Tag. If it hasn't, the server responds with 304 header with no actual data instructing the browser to use the cached version. Imagine how much slower WWW would be without this. Also, the days when browsers went bonkers when Ajax requests were E-tagged are long gone.

This works beautifully for HTTP APIs too, and we know that 97.42%* all APIs in the world are HTTP/JSON. `GET /orders` returns a JSON response. User refreshes the page, and if the response hasn't changed, why send the response all over again?

We send an E-Tag with all the HTTP API responses on Kite. The browser automatically does the rest. On the server side, there is a Redis map that maintains the E-Tags per user per resource. This tag is deleted when the cache becomes invalid, forcing a full HTTP 200 response the next time there's a request.

It is an absurdly trivial system that saves us terabytes of bandwidth every month, while significantly speeding up requests for a large number of users especially on unpredictable mobile internet. Our mobile applications implement a simple E-Tag/304 based client side response cache.

## 11. Serialisation is expensive.
Speaking of JSON responses, say, in Python, it's easy to do a `json.dumps(data)` and forget about it. However, converting a native data structure into JSON, or any other format, is an expensive CPU-bound operation. The bigger the payload, the slower it gets. While this is probably the last place where one would need to look for a bottleneck, it can be one at a certain point. If not in terms of request latency, in a garbage collected (GC) language, it can generate significant amounts of garbage creating GC pressure that can cause global slowdowns in the application.

## 12. Allocation is expensive.
Memory allocation is expensive, especially in GC languages. We write our high-throughput services in Go (simple to learn, highly productive, good for writing networked services), which is a GC language. Thanks to our services mostly being IO-bound and not heavy on memory, we are unlikely to run into any GC induced performance issues, but there are common sense principles that we use when writing Go programs. These are applicable to other languages as well. On hot paths, allocate as little as possible, re-use byte buffers, try and avoid unnecessary byte-string conversions, throw-away pointers, memory escaping from the stack to heap, and so on. Sometimes, there are easy-enough optimisations available when memory starts becoming a bottleneck, like [slots](https://book.pythontips.com/en/latest/__slots__magic.html) in place of `dicts` in Python, which are quite cool.

## 13. Multi-threading and concurrency are necessary, but hard.
Writing multi-threaded programs is hard. If a service can provide X throughput with one thread, and 2X with two threads, it is a no-brainer to do it, as long as the complexity of the multithreading logic does not outweigh the performance benefit. Otherwise, it may be easier to run the two copies of the service.

Where concurrency is possible though, the performance benefits can be massive. Writing multithreaded networking programs in Go is straightforward with goroutine (lightweight abstraction on top of threads) and channel abstractions. An HTTP service written in Go can spawn a large number of goroutines and handle a large number of concurrent connections with negligible resource usage. Something like that would be extremely difficult, if not possible, to achieve in, say, Python.

Concurrency can be used in interesting places other than just networking. For instance, we import files with tens of millions of JSON lines into databases daily. A Python script that reads the file line by line, deserializes JSON, performs computations, serialises back into JSON, and writes to the database is a perfectly fair and easy start. This worked for us for a long time until the file sizes grew to a point where the execution started demanding non-trivial amounts of time and memory. We replaced the script with a Go program that reads the file serially with one reader goroutine and feeds lines to N concurrent goroutines (one per available CPU on the system), each of which does computationally heavy operations, and writes the results concurrently into a writer goroutine that feeds it into the database. The speed-up was several orders of magnitude. An easy win with concurrency, irrespective of the language it was implemented in.

## 14. Some technologies are genuinely slow. Use fast technologies.
Python is slow. Ruby is slow. Frameworks like RoR are slow. And that's okay as long as they are used to build applications that do not need to serve low latency, high throughput requests without expensive and complex setups. If one picks a slow technology, builds a service in it expecting performance and scale, and then painstakingly tries to scale the underlying technology that is slow by design, that is a classic case of the not using the right tool for the right job. This is of course easier said than done, but is a trade-off that needs to be given serious thought. Often, picking the right tool for the job, even if it means learning something new, can pay off in a big way. I wrote our first Go service in 2014 after evaluating Python, C++, Java, NodeJS, and Erlang, for serving large number of concurrent WebSocket connections. Decided to learn Go after making the trade-off between simplicity, performance, ease of building concurrency, ease of deployment among other facts. The lightweight `ticker`, a single binary program, serves hundreds of thousands of concurrent WebSocket connections broadcasting millions of market quotes every second. Today, many of us in the team write Go, and when, say, a Python service slows down beyond the point of redemption, we find it straight forward to port it to Go. `Go` here is a placeholder and it can be any technology that fits a job.

That said, it is generally better to avoid large frameworks in applications. When push comes to shove and it is time to dive into the application looking for micro-optimisations, the framework will get in the way. It would be the framework's way or the highway. Using replaceable libraries and composing them avoids framework-lockins that impede optimisations.

## 15. Scaling horizontally, vertically, and "enterprisely".
If adding a few CPUs or extra RAM, that is, scaling vertically, scales a service for a long time, that would be the path of least pain. Of course, this is meant for sensibly built software. "Industry-leading", "enterprise-grade" applications that need 128 CPUs and 512 GB RAM to service 2000 requests a second, scale "enterprisely".

Scaling horizontally, excluding high-availability scenarios, is far more complex as all the aforementioned networking pain comes into play. One would much rather optimise software and database dependencies, scale vertically as much as possible, and then think of scaling horizontally, working out the right trade-offs between complexity and cost.

## 16. Human impediment.
Sometimes (often), a managerial bottleneck is a bigger impediment to common sense scaling than network IO—a lead who pushes a distributed NoSQL database where an SQLite file is sufficient, or a service mesh of microservices instead of a couple processes behind Nginx, or a quantum computer instead of a $5 EC2 instance. Or it could be a developer who bought into the hype of a particular technology. Non-technical decision makers with technical decision making powers, or overly biased technical people, unfortunately, are scaling problem for which there are no technical solutions.

## TLDR.
Common sense principles and practices trump complex technologies and methodologies. Don't be afraid to build simple things and scale them in simple ways. Reduce networked dependencies. `rsync` or `K8s`, pick technologies based on concrete rational reasons and not a vague idea of scale in the distant future. Don't try to "scale" like Google, or anyone else for that matter. It is always very specific to an organisation.

In April, when I wrote our [first blog post](/blog/hello-world), a 7+ million trade day was our highest ever. Since then, we have had multiple 8-9 million trade days with hundreds of thousands of additional concurrent users daily. We have been scaling with simplicity and common sense.


#### Footnote
* 97.42% is a fictional number that figuratively conveys the idea of a significant percentage. It is also the percentage of requests Karan's homebrew Pi K8s [DNS cluster](https://mrkaran.dev/posts/ndots-kubernetes/) drops despite significant optimisations. That is, 97.42% out of the 10 requests in total in a day. The rest are hot cached.
