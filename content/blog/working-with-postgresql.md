---
title: "Working with PostgreSQL"
description: "Our experience running large multi-terabyte PostgreSQL DBs in production with hundreds of billions of rows with minimal resources."
date: "2021-04-22T00:00:00+05:30"
author: satya10x
authors: ["satya10x"]
tags: ["databases"]
image: "/static/images/postgres.png"
---

This post is in the context of the large, data heavy PostgreSQL instances that store historical transactional data and reports, the databases that power [Console](https://zerodha.com/products/console) and its large scale number crunching and reporting. It talks about how we self-host, tune, and manage all our DB instances on bare EC2 instances. For high availability and backups, we use simple failover replicas and for backups, AWS disk snapshots.

The Console DBs store hundreds of billions of rows of different kinds of financial and transactional data, currently close to 20 TB, across four sharded nodes. Data such as daily trades, P&L, and ledger entries across our user base. While most of these rows are immutable, millions of rows are deleted and garbage collected regularly as a part of financial reconciliations.

The largest of our DBs act like warehouses into which tens of millions of new rows are inserted every day. For these DBs, 99% of the writes happen at night, when our daily “EOD” (End Of Day) processes reconcile large data dumps from stock exchanges. That after live trading hours and on holidays, user activity drops to practically nil, is a silver lining for us.

On an average trading day, the warehouse DB can serve up to 40-50,000 queries per second during peak traffic. This is despite the heavy "hot" caching layer, another Postgres instance, that we have in front of it. This is a peculiar use case where we use a Postgres DB as a hot cache to cache subsets of data queried from large Postgres DBs. It's covered in detail towards the [end of the post](#postgres-as-a-hot-cache-sql-jobber).

I would ideally like to write a series of posts deep-diving into different aspects of running PostgresDBs, but for now, this post is a quick overview of some of our learnings.

## Beginnings
For the first several years, we ran a single master-replica setup on two 32 core, 64 GB RAM EC2 instances, until our user base and the data started growing exponentially a couple of years ago. I feel we could’ve pushed this setup further but to be future proof, we moved to a multi-shard set up early last year. It is telling of Postgres’ resilience that the original setup stored and served billions of rows just fine. We have experimented continuously and made Postgres scale, sometimes pushing it to its limits. Here are some highlights.

## Data schema
Console DBs consist of mostly denormalized data of user trading activity, daily P&L records per financial instrument or symbol, and similar transactional data that we compute daily in our EOD processes. We will write a separate post on these massively concurrent crunching processes that runs every day, where time is of the essence as these processes have to finish quickly late in the night and be ready for the next trading day.

### JOINs
We realised early on that complex JOINs across tables holding billions of rows on are very difficult to scale. So, we denormalized most of our data, and data that didn’t make sense to denormalize, we created materialized views out of them to reduce ad-hoc JOIN queries. For instance, instead of a single parent table containing rows that are heavily referenced via foreign keys in many child tables, we denormalized and copied some of the parent data as columns into the child tables to avoid JOINs. So, most of our JOINs only happen over a couple entities, like a table and a view, and very rarely across more than two entities with huge numbers of rows. We also eventually dropped foreign keys in the process for significant performance gains during EOD bulk imports of tens of millions of rows.

### Logical partitioning
We logically partition most of our tables to group records by months based on their timestamps as pretty much all our data is time-stamped meaningfully. Trades that happened on a particular day, P&L for a day or a week, price of an instrument on a particular day. Dates are first-class citizens in financial databases. We arrived at monthly partitions after a lot of experimentation as it seemed to best suit the kind of data and the kind of queries our users generate. Accessing financial reports by our users generally tends to fall within the range of a month.

### Auto-increment IDs
We found storing auto-increment IDs unnecessary for the kind of data we have, billions of rows of them, saving significant amounts of the disk. This also resulted in a performance gain when bulk inserting rows.

## Tuning Postgres params

Tuning Postgres params is a regular exercise as the knobs need to be twiddled continuously as data grows, and as collective user behaviour changes (and it does!).

- **work_mem**: This is a tricky number. You generally end up balancing it based on how many sort operations you are doing, and what the `max_connections` number is. Postgres will use `work_mem` * `max_connections` memory, and `max_connections` can stay at high numbers despite connection pooling during peak traffic. If configured incorrectly, this can take up dangerous amounts of memory and tank the system.

    We ended up with a high value of around 600 MB for the kind of queries and sort and JOIN operations that we do. You can also play around with this number based upon how fast your disk I/O is. A poorly designed DB with slow query times would find a large value here detrimental as the I/O would be too slow, resulting in a lot of hanging connections and clogged memory. Do note that the default Postgres value is 4MB which is really low, and that value we've picked up for our setup is on the higher side. But that's what works for our workloads.


- **shared_buffer**: The amount of memory dedicated to Postgres for caching data, where it looks up before doing disk reads. A good way to figure out how to set this number is to run `EXPLAIN ANALYZE` on all the heavily used queries and check how many of them are hitting the configured `shared_buffer` size. If they aren’t, keep increasing the number up until maybe you've allocated more than one-third of the total available memory. Anything more might spell trouble for other parts of your DB operations. There is no need to store the entire DB in the cache, and if that's where you are headed, consider using something like Redis! 


- **effective_cache_size**: This is an interesting number and needs some extra context. Let's assume that you've 64 GB memory, out of which 30 GB is used by `shared_buffers`, and say another 10 GB is used by `work_mem` * `max_connections`. You are left with 24 GB of memory that your operating system can use for other things like the file system cache. Postgres will end up using this file system cache if it can’t find the data it is looking for in `shared_buffers`, which would be considerably slower than the Postgres cache. This is where `effective_cache_size` kicks in, where you tell Postgres that there is still 20+GB left for it to use for a temporary cache for a few queries, which would make the queries faster than just using the OS filesystem cache.


- **max_parallel_workers**: These are a helpful set of parameters to tune if your partitions are getting aggregated whenever you query data. For us, having a server with more cores for our DB made sense, as then we can have a `max max_parallel_workers` = number of cores, and then `max_parallel_workers_per_gather` to be half of that count. This count changes based upon how many processes parallelly run and need workers to be spawned. For instance, if you have set up parallel workers to do replication, then you need additional workers for that. Thus, when a user queries data across different months (logical partitions), the parallel workers for gathering run parallelly over multiple partitions and then aggregate the data, thus improving the speeds of `SELECT` queries. `EXPLAIN ANALYZE` would be your friend here to figure out how many workers you need for your workload. 


## Partitioning
Our original single-master setup was logically partitioned based on months as I mentioned earlier. We had experimented with per-day partitioning as all our rows are time-stamped per day anyway. It significantly boosted our daily bulk insert speeds as we are effectively dumping data into an empty partition every day, but it also slowed down the query speeds over date ranges by a huge margin as Postgres now had to search and join rows across multiple logical partitions.

Moving to per-month partitioning turned out to be a far better tradeoff for us as most of the user-generated queries tend to be within a month's range. Since sharding by month progressively slows down bulk insert speeds as the month goes on, we use a temporary table to bulk insert the daily data and then use that throughout the next day for user-facing queries (a significant number of queries are for that data) and sync it to the actual table asynchronously.


## Vacuuming
This is one of the most crucial aspects of maintaining a large DB. If your operation is similar to ours, where updates throughout the day are few and far in between, and bulk inserts and updates of billions of rows happen in batches, then turning off auto-vacuum is the first thing you should do, lest auto-vacuum kick in in the middle of bulk operations and lock everything down.
Instead, have a cron job that does `VACUUM ANALYZE` on your partitions that get updated the most. For large tables, this can take hours if not done frequently. The frequency depends upon the frequency and volume of mutations in your DB. For us, this is a part of our daily EOD process. 

If your DB handles a lot of writes throughout the day, then auto-vacuum needs to be configured to run after a certain meaningful number of writes and updates, without which it could keep getting triggered frequently, affecting performance. You want all your workers and I/O to be focused on serving queries as fast as possible. Constant vacuuming can result in that focus getting diverted into doing tasks for which the performance gains are minimal. 


## Indexing
It is a well-known fact that [97.42%](/blog/scaling-with-common-sense/#6-rdbms-works-almost-always) of all RDBMS problems and bottlenecks are due to poor indexing. While it is rather easy to index columns used in `WHERE` clauses, it is also easy to over-index. For large DB with a large number of writes, over-indexing can be a serious bottleneck. It is paramount to only index the necessary columns, and index the columns the way they are searched by taking advantage of partial and composite indexes. Don't define indexes for a query that you might run only once in a while. There can be cases where sequential scans are better than index scans. These trade-offs are something that you have to decide based entirely on the nature of your queries and their frequency and distribution. 


`EXPLAIN ANALYZE` is your best friend for every change you do to your DB. If a query is slow, 97.42% of the time it is either due to poor indexing or poor vacuuming. You can understand table health by querying `pg_stat_user_tables`. This tells you when a table was last vacuumed with which you can figure out if your vacuuming settings are optimal or not. You can also consider using the pg_stat_statements extension to record and analyze query usage metrics. It tells you the execution time of your queries, and how many times a particular table has been queried. For example, if a table is getting queried more than most, then you might want to assign more parallel workers to it speeding up queries. 


## Materialized views

These are super helpful when there is a subset of data that gets joined all over the DB, across multiple tables, frequently, or slow running `SELECT`s in general. You can speed up such queries by creating a materialized view out of them and using that in queries. This can also help in avoiding unnecessary indexing by materializing queries that otherwise scan the same data over and over. Materialized views are "snapshots" of queries results frozen in a virtual table and updated (asynchronously) periodically to avoid constant, ad-hoc queries.


## CTEs 

CTEs (Common Table Expressions) can help compartmentalize and re-use sub-queries in a complex query. For large, complex queries, splitting them into CTEs and re-using them can help get better query plans and performance. Also, CTEs in a query run concurrently, so that can also big a plus. We've used CTEs heavily to optimize our queries.


## Sharding: A mental tipping point
As I mentioned earlier, for the longest time, we had a simple single master setup. Last year, we reached a point where we figured that maybe running a single master setup, even though it was working smoothly, was pushing the stability of a fantastic piece of software a bit too far. Though it is difficult to say what could’ve happened had we kept going with this setup, a few problems could have been:

- Reaching a point where massively nightly bulk imports and the resultant vacuuming would’ve gotten unbearably slow. We were seeing signs of this.
- A scenario where the DB can’t recover after a crash, or after a restart (post tuning parameters-related changes) just because of the size of data, although Postgres is highly reliable and very rarely faces corruption.
- Having a single shard meant that yearly data (financial years are critical to the kind of data we store) that would get queried and used lesser and lesser, still got the same amount of resources (disk size, workers/cores) as more recently, actively used data. This means that you are trundling towards needing infinite resources just because you are unable to prioritize what subset of data you need more than the others.

Thus, we did a few experiments to figure out the most optimal way to shard our DB. Some of the constraints we had were: 

- Sharding with minimal changes to the data and query. 
Sharding older financial year data to smaller servers, as most queries happen in the date range of the current financial year. 
- Not moving out of PostgreSQL, obviously. We have no intentions of moving away from Postgres, though we are currently experimenting with systems like ClickHouse for certain subsets of immutable data, primarily for huge disk savings. 


The two possible paths were:

- **[citus_data](https://www.citusdata.com)** is a Postgres extension provided by Citus Data for setting up a Postgres cluster and sharding data across it. Its advantages are that it works seamlessly with Postgres, provides "magic" sharding out of the box, failover mechanisms, and query routing. However, it achieves this by adding a new reference ID column to every single sharded table. We didn't want to go down that path where we would have to rewrite the hundreds of queries that we have to work with this new schema. Also, mutating our massive multi-TB databases would've taken unknown amounts of time and storage, which was not acceptable to us.


- **[postgres_fdw](https://www.postgresql.org/docs/9.5/postgres-fdw.html)** (Postgres Foreign Data Wrapper) is an extension bundled with Postgres which lets you query an abstracted external data store. That is, it lets you treat an external source, a Postgres or MySQL DB, Redis, or even a CSV file as if it were a Postgres DB, provided there are fdw plugins available for those sources. We picked this and sharding our massive DBs to multiple nodes and coming back online took us less than two hours. Like I said earlier, we enjoy the silver lining of being able to do maintenance during off-market hours. It kind of went down like this:

    - We used EC2 snapshots of the primary DB server into new instances, and failover replicas for each of them. 
    - Setup a fdw connection with the primary DB and the new instances.
    - We wanted our primary instance to only have data for the current year and the other shards to have older data. Wrote a script that deleted the older monthly logical partitions on the primary instance and instead set up a foreign table (`postgres-fdw`) link with the smaller shards. Wrote another script that deleted partitions for the current year from the smaller shards. Going forward, every year after the financial year's completion, we’ll repeat this exercise. Do note that dropping partitions in Postgres is fast.


A couple of limitations of sharding with `postgres-fdw` are:
- Data is being transferred over the network, so aggregation would be a bit slower over a massive data range. However, thanks to our hot cache setup, this isn't a problem.
- Cross-node parallelization is not possible. Hopefully, a future version of Postgres can take care of this. 

We were fine with these tradeoffs as queries happening over older financial years, that is, smaller shards were few and far in between. This also allowed us to have a process that stores all older financial years in less powerful nodes. Thus with every passing financial year, we can always bump our older financial year data into a less powerful server, thus cost-saving a bit. 

## Postgres as a hot cache (`sql-jobber`)
An RDBMS acting as a hot cache for RDBMS isn’t very common, but this setup has been working quite well for us. As I mentioned early on, we have a hot cache Postgres DB that we use in Console to serve reports to users. The reality is that tens of thousands of users concurrently querying their trade or P&L history from a DB with billions of rows is very hard to scale. Even if the queries are fast, they are still not fast enough to serve tens of thousands of reports every second. Moreover, even after users pull a report, they will likely sort and filter it further. These operations easily snowball.

Early on, we considered caching query results in Redis, but it would have been complex to implementing filtering and sorting on the dozens of different kinds of reports a user can pull. Also, this would require ever-increasing quantities of RAM.

So we did some R&D and figured that we could just use another dedicated Postgres instance as a hot cache, where every query to the large master DB writes the results into a freshly created table just for that query (a “job”) in the cache DB. This ephemeral cache table has columns that are automatically derived from the columns in the results of the original query. All subsequent reads, filtering, and sorting from the user hit this cache table, and thus be extremely fast as opposed to querying the master DB.

To abstract and automate all of this, we developed [sql-jobber](https://github.com/knadh/sql-jobber) in house, an open-source distributed job queue that can queue heavy SQL read jobs, query large backend DBs as their capacity permit, and cache the results of every such read as an independent table in a cache DB from where the results can be shown to a user on a UI or whatever.

This also allows us to control the number of queries (load) that hit the large master DB and spread user load across any number of cache DBs. You can almost think of this as a materialized view created of each query stored in a different database. Once cached, subsequent sort and filter requests from the user can be done on the cached table. This is how we keep our massive primary DBs away from the bombardment of queries that user activity generates.

We ended up stretching Postgres to new limits here, where our cache DB ends up **with tens of millions of tables at the end of every day**, where each table is cached snapshots of results of queries that were issued to the actual data DB. We simply drop the cache DB and recreate it every night, starting with a blank hot cache slate for the next day. This has been working well, serving millions of reports to millions of users every day on Console.

A few things we tuned for the `sql-jobber` hot cache DB: 

- `max_connections` has to be high it acts as a primary server handling a large number of user queries.
- `work_mem` is kept super low, a few MBs, as there are no JOINs happening and each table contains a few hundred or thousand rows, all the data that the user requested with a particular query.
- We turn off `fsync` and write-ahead logs as we can afford to throw away the cached data if the cache DB needs to be restarted for any reason. 
- We turn off replication as there is no need for an ephemeral cache to be replicated.
- `shared_buffers` is set based on the average table size of all the tables created during a peak hour. 



## Hot takes
- It is impossible to meaningfully tune a Postgres DB and your queries if you do not understand `VACUUM ANALYZE` well.

- Poor indexing and vacuuming are almost always the biggest culprits of all RDBMS performance problems. You don't need distributed DBs, you just need better indexing (almost always).

- There is no need to go multi-shard, multi-cluster when your data is not set to cross a few TBs for the foreseeable future. Planning properly now can help cross that bridge easily in the future. We sharded our 20TB DB in two hours with zero changes to our schemas.

- Instead, you can spend valuable time improving your table schemas, queries, indexes, and writing better caching layers. Without that, you will eventually hit a point where throwing gargantuan servers at your DB won't make it scale. 

- Often, storing less but well-planned data is better than storing tons of "big data". We've put a lot of effort into figuring out the right trade-offs for us, for instance, storing incremental diff data or storing data at various date-based checkpoints to reduce the number of physical rows we have to store. For example, in the rare case where we want to get a certain trade report of a user from a long time ago, we fall back to the data at the closest checkpoint for that date and then recompute till the date needed. Though the trade-off here is spending CPU cycles in recomputing a dataset that we had computed before, it is acceptable to us compared to storing billions of rows of data that might never be used.

- As cliched as it sounds, the fastest queries are always on tables with fewer data. This sort of trade-off and decision making, where you expend more CPU cycles today to save lots of disk (and pain) in the future requires a deep understanding of your data and the nature of your business and users, not Postgres sharding or distributed DBs.

- In all our engineering decisions, we always pick tools that are not only easy to implement but are easier to manage long term. Postgres has been just that over a long period, something that I can't say about MySQL. Unfortunately, with MySQL, we've had data consistency issues, corruption, weird NULL/empty value consistencies, inexplicable memory leaks, unfixable performance issues, and more. Postgres has been rock solid ever since we adopted it in 2013 when we first started building our stack. Since then, we've upgraded from Postgres 9 → 10 → 11 → 12 without any issues. In fact, with every upgrade, we've gained performance improvements for free.

Our experience with Postgres is a testament to its developers and maintainers for building an incredible, resilient, and rock-solid RDBMS. Thanks to the exhaustive but easy-to-read documentation, we have also been able to build our expertise in-house. As full-stack developers, we put in the effort of understanding our data and the nature of our business, and Postgres helped us implement that into an easily managed, scalable system.

There is plenty more to deep dive into and share; hopefully soon. Thanks for reading!
