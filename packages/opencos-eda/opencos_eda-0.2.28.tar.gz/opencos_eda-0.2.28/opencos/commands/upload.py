'''opencos.commands.upload - Base class command handler for: eda upload ...

Intended to be overriden by Tool based classes (such as CommandUploadVivado, etc)
'''

import os

from opencos.eda_base import CommandDesign, Tool

class CommandUpload(CommandDesign):
    '''Base class command handler for: eda upload ...'''

    CHECK_REQUIRES = [Tool]

    command_name = 'upload'

    def __init__(self, config: dict):
        CommandDesign.__init__(self, config=config)

    def process_tokens(
            self, tokens: list, process_all: bool = True, pwd: str = os.getcwd()
    ) -> list:

        unparsed = CommandDesign.process_tokens(
            self, tokens=tokens, process_all=process_all, pwd=pwd
        )
        self.create_work_dir()
        self.run_dep_commands()
        self.do_it()
        return unparsed
