# No configuration needed
__version__ = '0.3'
__author__  = 'ArmedGuy'

import b3, time, threading, thread, sys
import b3.events
import b3.plugin
from b3 import functions
#--------------------------------------------------------------------------------------------------
class NamechangerPlugin(b3.plugin.Plugin):
    requiresConfigFile = False
    _adminPlugin = None
    _checkedPlayers = None
    def onLoadConfig(self):
        pass
            
    def startup(self):
        """\
        Initialize plugin settings
        """
        
        if self._adminPlugin == None:
            try:
                self._adminPlugin = self.console.getPlugin('admin')
            except:
                self.error("Could not get admin plugin!")
                return False
                

        self._adminPlugin.registerCommand(self, "namechanger", 60, self.getCmd("namechanger"), "nc")
        
    def getCmd(self, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(self, cmd):
            func = getattr(self, cmd)
            return func
        return None
        
    def cmd_namechanger(self, data, client, cmd=None):
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            delta = 1
            amount = 3
        else:
            try:
                delta = int(m[0])
                amount = int(m[1])
            except:
                delta = 1
                amount = 3
        thread.start_new_thread(self.run_namechanger_check, (client, delta, amount))
        
    def run_namechanger_check(self, client, delta, amount):
        try:
            i = 0
            self._checkedPlayers = {}
            while i < amount:
                client.message("Namechanger check %i/%i" % (i+1, amount))
                plist = self.console.getPlayerList()
                for cid,c in plist.iteritems():
                    if cid in self._checkedPlayers:
                        plrTmp = self._checkedPlayers[cid]
                        if plrTmp["ip"] != c["ip"]:
                            self._checkedPlayers[cid]["changes"] = 0
                        else:
                            if plrTmp["name"] != c["name"]:
                                self._checkedPlayers[cid]["changes"] = self._checkedPlayers[cid]["changes"] + 1
                    else:
                        self._checkedPlayers[cid] = {"name": c["name"], "ip": c["ip"], "changes": 0}
                time.sleep(delta)
                i = i + 1
            
            for pid in self._checkedPlayers:
                player = self._checkedPlayers[pid]
                self.debug("Player: %s" % str(player))
                if player["changes"] > 0:
                    client.message("id: %i, changes: %i" % (int(pid), int(player["changes"])))
        except:
            self.error("Namechanger thread exception: %s" % str(sys.exc_info()))
