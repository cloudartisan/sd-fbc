#!/usr/bin/env python


"""
Checks the true amount of "free" memory.  See http://www.linuxatemyram.com/
for details.

Servers with massive amounts of disk access (typically
search/index/database servers) will often build a large disk cache.
Unfortunately, many tools check the "free" memory only and assume
the server is running out of memory, when it is still available but
currently held by buffers and cache.

Eg, in this example there's really 2.5GB available to applications.

             total       used       free     shared    buffers     cached
Mem:          7468       7413         54          0        421     2114
-/+ buffers/cache:       4878       2590
Swap:            0          0          0

The above example is from a server running Elastic Search with a huge
number of open files.  Check out this output from slabtop, sorted by
cache size:

  OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ/SLAB CACHE SIZE NAME
642369 621647  96%    0.10K  16471       39     65884K buffer_head
181776 181706  99%    0.19K   8656       21     34624K dentry
 21840  21840 100%    0.96K   1365       16     21840K ext4_inode_cache
 19138  18429  96%    0.55K   1367       14     10936K radix_tree_node
  5057   4901  96%    0.58K    389       13      3112K inode_cache
  2240   1954  87%    0.79K    112       20      1792K ext3_inode_cache
"""


import commands


class FreeBuffersCache:
    """
    Checks the true amount of "free" memory.  See
    http://www.linuxatemyram.com/ for details.
    """
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

    def run(self):
        """
        Recommended group for Server Density plugin:

        Title: FreeBuffersCache
        Key: free_buffers_cache
        """
        data = {}
        status, output = commands.getstatusoutput("free -m")
        if status != 0:
            return self.data
        for line in output.splitlines():
            line = line.strip()
            if not line:
                continue
            elif line.startswith("-/+ buffers/cache:"):
                data['free_buffers_cache'] = int(line.split()[-1])

        return data


if __name__ == "__main__":
    import logging
    logger = logging.getLogger("FreeBuffersCache")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    fbc = FreeBuffersCache(None, logger, None)
    fbc.run()
