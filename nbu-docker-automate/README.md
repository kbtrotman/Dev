Amoung the 20 other things I've done over the last 1 to 2 years, this is a framework for a netbackup API that runs
on docker or kubernetes that I began. At present, it is unfinished simply because it doesn't have a web frontend. 
I need to add a Django interface to it. It is also just the start of the entire API overlay. Right now it ports the NBU
policy add and policy delete functions to docker and has a reporting function. It does work on MS-SQL, which is a
major drawback for dockers. It needs to be ported to postgres soon. As with all things though, the focus shifted
from this to Rubrik and I began developing API overlays for Rubrik instead. I never got back to finishing this.
I've done much bigger and better NBU automation, but it's value is in an example of use on Docker/Kubernetes, not
in how extensive it is (because it's not).
