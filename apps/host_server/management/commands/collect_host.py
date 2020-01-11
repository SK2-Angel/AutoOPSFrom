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
from host_server.models import Host_server

class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        if result.task_name=='collect_host':
            self.collect_host(result._result)
    def collect_host(self,result):
        facts = result.get('ansible_facts', {})
        host_name=facts.get('ansible_hostname','')
        ip=facts.get('ansible_default_ipv4',{}).get('address','')
        mac=facts.get('ansible_default_ipv4',{}).get('macaddress','')
        os='{}-{}'.format(facts.get('ansible_lsb',{}).get('id',''),facts.get('ansible_lsb',{}).get('release',''))
        mem=facts.get('ansible_memtotal_mb','')
        cpu=facts.get('ansible_processor_vcpus')
        def select_disk():
            disk_name = []
            disk_size = []
            for i in facts.get('ansible_mounts', []):
                disk_name.append(i.get('device'))
                disk_size.append(round((i.get('size_total') / 1024 / 1024 / 1024), 2))
            return dict(zip(disk_name, disk_size))
        disk = select_disk()
        sn = facts.get('ansible_product_name')
        Host_server.Host_server_insert_data(host_name,ip,mac,os,mem,cpu,disk,sn)

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
                       'name': 'collect_host',
                       'setup': ''
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
