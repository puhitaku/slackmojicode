# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import interpreter, parser, converter
from rtmbot.core import Plugin


class SlackMojicodePlugin(Plugin):
    user_id = ""

    def process_hello(self, data):
        res = self.slack_client.api_call("auth.test", token=self.slack_client.token)
        self.user_id = res['user_id']

    def process_message(self, data):
        intr = interpreter.Interpreter()

        if data['text'].startswith('<@{}> run'.format(self.user_id)):
            script = data['text'].replace('<@{}> run'.format(self.user_id), '')
            script = script.strip()
            script = script.replace('&lt;', '<')
            script = script.replace('&gt;', '>')
            out = ""
            print script

            try:
                intr.compile_interpret(parser.parse(script))
                out_list = intr.get_stdout()
                if len(out_list) > 0:
                    out = '\n```{}```'.format('\n'.join(out_list))
                else:
                    out = 'No output'
            except Exception as e:
                out += "\n\nError has occured while excecuting SlackMojicode:\n```{}: {}```" \
                    .format(type(e), e)
                raise e

            self.outputs.append([data['channel'], '\n' + out])

        if data['text'].startswith('<@{}> convert'.format(self.user_id)):
            script = data['text'].replace('<@{}> convert'.format(self.user_id), '')
            script = script.strip()
            script = script.replace('&lt;', '<')
            script = script.replace('&gt;', '>')
            script = converter.convert(script)

            self.outputs.append([data['channel'], script])
