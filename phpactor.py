from subprocess import PIPE, Popen
import json

class Phpactor:
    class Settings:
        def __init__(self, phpactorbin, project_root):
            self.phpactorbin = phpactorbin
            self.project_root = project_root

    class Rpc:
        class Request:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def to_json(self):
                return json.dumps({'action': self.action, 'parameters': self.parameters}, sort_keys=True)

        class Response:
            def __init__(self, action, parameters):
                self.action = action
                self.parameters = parameters

            def from_json(value):
                d = json.loads(value)
                return Phpactor.Rpc.Response(d['action'], d['parameters'])

            def to_json(self):
                return json.dumps({'action': self.action, 'parameters': self.parameters}, sort_keys=True)

        class GeneralError:
            def __init__(self, message):
                self.message = message

        class Client:
            def __init__(self, phpactorbin, project_root):
                self.phpactorbin = phpactorbin
                self.project_root = project_root

            def send(self, request):
                p = Popen([self.phpactorbin, 'rpc'], stdout=PIPE, stdin=PIPE, stderr=PIPE, cwd=self.project_root)
                stdout, stderr = p.communicate(request.to_json().encode())

                if stderr:
                    return None, Phpactor.Rpc.GeneralError(stderr.decode())

                return Phpactor.Rpc.Response.from_json(stdout.decode()), None

    def __init__(self, settings):
        self.rpc_client = Phpactor.Rpc.Client(settings.phpactorbin, settings.project_root)

    def send_rpc_request(self, request, before_send, on_error, on_done):
        before_send(request)

        response, err = self.rpc_client.send(request)

        if err:
            on_error(err)
            return;

        on_done(response)
