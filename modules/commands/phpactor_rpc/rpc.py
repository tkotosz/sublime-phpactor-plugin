import sublime
import sublime_plugin
from ...phpactor_client import *

class PhpactorRpcCommand(sublime_plugin.TextCommand):
    def run(self, edit, action, parameters):
        phpactor = Phpactor(self.view.window())
        rpcRequest = Phpactor.Rpc.Request(action, parameters)
        phpactor.send_rpc_request(rpcRequest)
