#!/usr/bin/env python
import json
import shutil
from django.core.management import BaseCommand
from django.conf import settings
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C
#from host_server.models import Host_server

class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        print(result._result)
        if result.task_name=='collect_scanning_host':
            self.collect_host(result._result)
    def v2_runner_on_failed(self, result, ignore_errors=None):
        if ignore_errors:
            return
        res = getattr(result, '_result')
        self.error_msg = res.get('stderr', '') + res.get('msg')
        print(self.error_msg)
    def runner_on_unreachable(self, host, result):
        if result.get('unreachable'):
            self.error_msg = host + ':' + result.get('msg', '')

        print(self.error_msg)
    def v2_runner_item_on_failed(self, result):
        res = getattr(result, '_result')
        self.error_msg = res.get('stderr', '') + res.get('msg')
        print(self.error_msg)
    def collect_host(self,result):
        print()
#        Host_server.Host_server_insert_data(host_name,ip,mac,os,mem,cpu,disk,sn)

class Command(BaseCommand):
    def handle(self,*args,**options):
        context.CLIARGS = ImmutableDict(connection='local', module_path=[], forks=10, become=None,
                                        become_method=None, become_user=None, check=False, diff=False)
        loader = DataLoader()
        passwords = dict(vault_pass='secret')

        results_callback = ResultCallback()

        inventory = InventoryManager(loader=loader, sources='/opt/sumscope/devops/scripts/hosts')

        variable_manager = VariableManager(loader=loader, inventory=inventory)
        play_source =  {
                    'name': "host_Options",
                    'hosts': 'all',
                    'gather_facts': 'no',
                   'tasks': [
                     {
                       'name': 'collect_scanning_host',
                       'command': 'uptime'
                     }
                   ]
                }
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
        tqm = None
        try:
            tqm = TaskQueueManager(
                      inventory=inventory,
                      variable_manager=variable_manager,
                      loader=loader,
                      passwords=passwords,
                      stdout_callback=results_callback,
                  )
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)