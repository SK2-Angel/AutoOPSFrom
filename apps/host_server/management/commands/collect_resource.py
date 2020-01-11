# encoding: utf-8

import os
import json
import shutil
from django.core.management import BaseCommand
from django.conf import settings
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible import context
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.module_utils.common.collections import ImmutableDict
import ansible.constants as C
from host_server.models import Host_server_cpu_mem,Monitor_server_cpu_mem


class ResultCallback(CallbackBase):
    def __init__(self):
        super(ResultCallback, self).__init__()
        self._cache_host = {}

    def v2_runner_on_ok(self, result, **kwargs):
        if result.task_name == 'collect_host':
            facts = result._result.get('ansible_facts', {})
            ip = facts.get('ansible_default_ipv4', {}).get('address', '')
            self._cache_host[result._host.name] = ip
        elif result.task_name == 'copyfile':
            pass
        elif result.task_name == 'collect_resource':
            ip = self._cache_host.get(result._host.name)
            result_datas=result._result
            result_temp=result_datas.get('stdout_lines',[])
            cpu=result_temp[0].split('%')[0]
            mem=result_temp[1].split()[3].split('%')[0]
            disk_datas=result_temp[2].split('%')
            disk={}
            disk['disk']=disk_datas
            Host_server_cpu_mem.Host_server_cpu_mem_insert(ip,cpu,mem,disk)
            Monitor_server_cpu_mem.Monitor_server_cpu_mem_insert(ip,cpu,mem)


class Command(BaseCommand):

    def handle(self, *args, **options):
        context.CLIARGS = ImmutableDict(connection='local', module_path=[], forks=10, become=None,
                                        become_method=None, become_user=None, check=False, diff=False)
        loader = DataLoader()
        passwords = {}
        results_callback = ResultCallback()
        inventory = InventoryManager(loader=loader, sources=('/opt/sumscope/devops/scripts/hosts'))
        variable_manager = VariableManager(loader=loader, inventory=inventory)
        play_source = {
            'name': "cpu_mem",
            'hosts': 'all',
            'gather_facts': 'no',
            'tasks': [
                {
                    'name': 'collect_host',
                    'setup': ''
                },
                {
                    'name': 'copyfile',
                    'copy': 'src={0} dest={1}'.format('/opt/sumscope/devops/scripts/host_cpu_mem_disk.sh',
                                                      '/home/host_cpu_mem_disk.sh')

                },
                {
                    'name': 'collect_resource',
                    'command': '/bin/bash {0}'.format('/home/host_cpu_mem_disk.sh')

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




