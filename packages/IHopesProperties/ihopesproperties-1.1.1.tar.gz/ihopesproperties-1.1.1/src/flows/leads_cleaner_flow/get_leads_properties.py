from typing import List, Dict

from asana import TasksApi

from flows.leads_cleaner_flow.leads_task import LeadsTask
from my_asana.authenticate import get_tasks_api
from my_asana.consts import LEADS_PROPERTIES_SECTION, PROPERTY_TASK_TEMPLATE_ID


def get_leads_properties() -> List[LeadsTask]:
    tasks_api: TasksApi = get_tasks_api()
    raw_tasks: List[Dict[str, str]] = list(tasks_api.get_tasks_for_section(
        section_gid=LEADS_PROPERTIES_SECTION,
        async_req=False,
        opts={})
    )

    leads_tasks: List[LeadsTask] = \
        [LeadsTask(address=raw_task['name'], gid=raw_task['gid']) for raw_task in raw_tasks \
         if raw_task['gid'] != PROPERTY_TASK_TEMPLATE_ID]
    print(f'Found {len(leads_tasks)} leads properties')

    return leads_tasks
