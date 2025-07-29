'''opencos.commands.sweep - command handler for: eda sweep ...

These are not intended to be overriden by child classes. They do not inherit Tool classes.
'''

import os
import re

from opencos import util
from opencos.eda_base import CommandDesign, CommandParallel, get_eda_exec

class CommandSweep(CommandDesign, CommandParallel):
    '''Command handler for: eda sweep ...'''

    command_name = 'sweep'

    def __init__(self, config:dict):
        CommandDesign.__init__(self, config=config)
        CommandParallel.__init__(self, config=config)
        self.sweep_target = ''
        self.single_command = ''


    def check_args(self) -> None:
        '''Returns None, checks self.args (use after args parsed)'''
        if self.args['parallel'] < 1 or self.args['parallel'] > 256:
            self.error(f"Arg {self.args['parallel']=} must be between 1 and 256")

    def _append_sweep_args(self, arg_tokens: list) -> None:
        '''Modifies list arg_tokens, bit of a hack'''

        # TODO(drew): similar clunky behavior with self.config['eda_orignal_args'] that
        # CommandMulti has we need to pass global args to each sweep job, which we can
        # do via arg_tokens (list)
        # TODO(drew): fix this, for now it works but --color and other args do not work.
        if any(a.startswith('--config-yml') for a in self.config['eda_original_args']):
            cfg_yml_fname = self.config.get('config-yml', None)
            if cfg_yml_fname:
                arg_tokens.append(f'--config-yml={cfg_yml_fname}')
        if '--eda-safe' in self.config['eda_original_args']:
            arg_tokens.append('--eda-safe')
        if any(a.startswith('--tool') for a in self.config['eda_original_args']):
            tool = self.config.get('tool', None)
            if tool:
                arg_tokens.append('--tool=' + tool)


    def process_tokens(
            self, tokens: list, process_all: bool = True,
            pwd: str = os.getcwd()
    ) -> list:
        '''CommandSweep.process_tokens(..) is likely the entry point for: eda sweep <command> ...

        - handles remaining CLI arguments (tokens list)
        - builds sweep_axis_list to run multiple jobs for the target
        '''

        # multi is special in the way it handles tokens, due to most of them being processed by
        # a sub instance
        sweep_axis_list = []
        arg_tokens = []

        _, unparsed = self.run_argparser_on_list(
            tokens=tokens,
            parser_arg_list=[
                'parallel',
            ],
            apply_parsed_args=True
        )

        self.check_args()

        tokens = unparsed

        self.single_command = self.get_command_from_unparsed_args(tokens=tokens)

        self._append_sweep_args(arg_tokens=arg_tokens)

        while tokens:
            token = tokens.pop(0)

            # command and --parallel already processed by argparse

            m = re.match(r'(\S+)\=\(([\d\.]+)\,([\d\.]+)(,([\d\.]+))?\)', token)
            if m:
                # Form --arg=CUST "CUST=(range-start,range-stop,range-step)"
                sweep_axis = { 'key' : m.group(1),
                               'values' : [  ] }
                for v in range(
                        int(m.group(2)),
                        int(m.group(3)) + 1,
                        int(m.group(5)) if m.group(4) else 1
                ):
                    sweep_axis['values'].append(v)
                util.debug(f"Sweep axis: {sweep_axis['key']} : {sweep_axis['values']}")
                sweep_axis_list.append(sweep_axis)
                continue
            m = re.match(r'(\S+)\=\[([^\]]+)\]', token)
            if m:
                # Form --arg=CUST "CUST=[val0,val1,val2,...]"
                sweep_axis = { 'key' : m.group(1), 'values' : [] }
                for v in m.group(2).split(','):
                    v = v.replace(' ','')
                    sweep_axis['values'].append(v)
                util.debug(f"Sweep axis: {sweep_axis['key']} : {sweep_axis['values']}")
                sweep_axis_list.append(sweep_axis)
                continue
            if token.startswith('--') or token.startswith('+'):
                arg_tokens.append(token)
                continue
            if self.resolve_target(token, no_recursion=True):
                if self.sweep_target != "":
                    self.error(f"Sweep can only take one target, already got {self.sweep_target},"
                               f"now getting {token}")
                self.sweep_target = token
                continue
            self.error(f"Sweep doesn't know what to do with arg '{token}'")
        if self.single_command == "":
            self.error("Didn't get a command after 'sweep'!")

        # now we need to expand the target list
        util.debug(f"Sweep: command:    '{self.single_command}'")
        util.debug(f"Sweep: arg_tokens: '{arg_tokens}'")
        util.debug(f"Sweep: target:     '{self.sweep_target}'")

        # now create the list of jobs, support one axis
        self.jobs = []

        self.expand_sweep_axis(arg_tokens=arg_tokens, sweep_axis_list=sweep_axis_list)
        self.run_jobs(command=self.single_command)
        return tokens


    def expand_sweep_axis(
            self, arg_tokens: list, sweep_axis_list: list, sweep_string: str = ""
    ) -> None:
        '''Returns None, appends jobs to self.jobs to be run by CommandParallel.run_jobs(..)'''

        command = self.single_command
        target = self.sweep_target

        util.debug(f"Entering expand_sweep_axis: command={command}, target={target},",
                   f"arg_tokens={arg_tokens}, sweep_axis_list={sweep_axis_list}")
        if len(sweep_axis_list) == 0:
            # we aren't sweeping anything, create one job
            snapshot_name = target.replace('../','').replace('/','_') + sweep_string
            eda_path = get_eda_exec('sweep')
            self.jobs.append({
                'name' : snapshot_name,
                'index' : len(self.jobs),
                'command_list' : (
                    [eda_path, command, target, '--job_name', snapshot_name] + arg_tokens
                )
            })
            return
        sweep_axis = sweep_axis_list[0]
        for v in sweep_axis['values']:
            this_arg_tokens = []
            for a in arg_tokens:
                a_swept = re.sub(rf'\b{sweep_axis["key"]}\b', f"{v}", a)
                this_arg_tokens.append(a_swept)
            next_sweep_axis_list = []
            if len(sweep_axis_list)>1:
                next_sweep_axis_list = sweep_axis_list[1:]
            v_string = f"{v}".replace('.','p')
            self.expand_sweep_axis(
                arg_tokens=this_arg_tokens,
                sweep_axis_list=next_sweep_axis_list,
                sweep_string = sweep_string + f"_{sweep_axis['key']}_{v_string}"
            )
