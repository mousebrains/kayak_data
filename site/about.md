## About

*Last updated: April 23, 2026*

### Origins

It started with a single paddling trip.

In the 1994–95 season, Pat Welch ran the North Fork Middle Fork of the
Willamette (NFMF) with Jim Reed. Somewhere between the take-out and the drive
home, the conversation turned to Salmon Creek — a nearby run with no gauge of
its own. Jim said it would be nice to know the level before making the drive out
there. He had worked out a rough rule of thumb that related Salmon Creek's level
to the NFMF gauge, which did report: if the NFMF read a certain number, Salmon
Creek was probably in.

That conversation was the seed.

### From a CSV to a website

Jim was an editor of the third edition of the Willamette Kayak and Canoe Club's
*Soggy Sneakers*, the club's guide to whitewater in Oregon. He had already done
the work of cataloguing runs — put-ins, take-outs, character, hazards,
recommended flow ranges — and he handed Pat a CSV file of the runs described in
the book.

Pat, meanwhile, had been harvesting USACE gauge data. A script to fetch those
gauges, Jim's table of runs, and a way to glue the two together — that was all it
took to make something genuinely useful. If you were thinking about paddling
Salmon Creek in the morning, you could finally check the night before.

The first version was a prototype written in Tcl/Tk, running on Pat's research
computer. Rough edges everywhere, but it solved the problem.

### Growth and rewrites

Over the years the scope crept outward. More rivers. More states. More agencies
— NOAA, USGS, USBR, and state water resource departments — joined the USACE
feeds the site started with. At its peak the database tracked roughly **three
thousand gauges** across the western United States.

Around 2000, the Tcl/Tk code was replaced with C++. That version carried the
site for years: slow feature additions, quiet fixes, the occasional partial
rebuild. What followed after that was less a single rewrite than a long series of
starts and stops — pieces were ported as they needed changing; other pieces
waited.

By 2026, the C++ base has been progressively transformed into the system running
today: a Python backbone on top of a SQLite database, a modular fetch pipeline
that speaks each agency's formats, and a static HTML build for the levels pages
layered over PHP for the interactive pieces. It looks, finally, like a modern web
application.

### Design philosophy: thin pipes

One goal has never changed, and it has gotten more important with time, not
less: **thin pipes**.

Pages are small. Requests are few. Nothing loads from a third-party tracker. The
levels tables are pre-rendered HTML with inlined CSS and tiny inline SVG
sparklines. The site is tuned to work on a high-bandwidth desktop, yes — but
really it is tuned to work on a 3G phone with one bar of signal at the put-in,
which is, not coincidentally, exactly the moment you most need to check it.

Every design decision runs through that filter: *does this still work over a slow
connection?* If the answer is no, it doesn't ship.

### Supporting this site

For decades this site has been supported by the
[Willamette Kayak and Canoe Club](https://wkcc.org) (WKCC). If you find it useful
and want to help keep it going, please consider joining or contributing to the
club.

Pat's time on this project is entirely voluntary.
