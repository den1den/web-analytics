The original data (polblogs.gml)

Political blogosphere Feb. 2005
Data compiled by Lada Adamic and Natalie Glance

Node "value" attributes indicate political leaning according to:

  0 (left or liberal)
  1 (right or conservative)

Data on political leaning comes from blog directories as indicated.  Some blogs were labeled manually, based on incoming and outgoing links and posts around the time of the 2004 presidential election.  Directory-derived labels are prone to error; manual labels even more so.

Links between blogs were automatically extracted from a crawl of the front page of the blog.

These data should be cited as Lada A. Adamic and Natalie Glance, "The political blogosphere and the 2004 US Election", in Proceedings of the WWW-2005 Workshop on the Weblogging Ecosystem (2005).

-----------------

The preprocessed data (edges.txt and nodes.txt)

The file "edges.txt" is the graph after preprocessing. Each line in
this file is in the format

  FromNodeId ToNodeId

for instance, the line "14 118" denotes "there is link from Node 14 to Node 118".

The file "nodes.txt" contains the nodes ids and corresponding Node
attribute or label that can be 0 or 1 (liberal vs. conservative),
and each line in in the format

  NodeId NodeAttribute
