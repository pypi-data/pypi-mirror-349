from typing import List

from asana.rest import ApiException

from google_drive.duplicate_template_arv import save_as_template_arv
from my_asana.authenticate import get_tasks_api
from my_asana.consts import PROPERTY_TASK_TEMPLATE_ID, LEADS_PROPERTIES_SECTION, LEADS_PROJECT_ID
from my_asana.task_place_holders import TaskPlaceHolder, get_new_property_media
from my_asana.utils import add_task_to_section
from property import SoldProperty, ForSaleProperty
from zillow.property_getter import construct_zillow_basic_property_url


def generate_new_property_task(for_sale_property: ForSaleProperty, comps: List[SoldProperty]) -> str:
    # Create API instance
    property_address: str = for_sale_property.address.get_full_address()

    try:
        # Get the source task
        tasks_api = get_tasks_api()
        template_task = tasks_api.get_task(PROPERTY_TASK_TEMPLATE_ID, opts=[])
        template_description = template_task['notes']

        for place_holder in TaskPlaceHolder:
            if place_holder.value in template_description:
                print(f"Found placeholder: {place_holder.value}")
                if place_holder is TaskPlaceHolder.ARV_DOC:
                    updated_description: str = save_as_template_arv(for_sale_property, comps)
                elif place_holder is TaskPlaceHolder.PROPERTY_LINK:
                    updated_description: str = construct_zillow_basic_property_url(property_address)
                elif place_holder is TaskPlaceHolder.PROPERTY_MEDIA:
                    updated_description: str = get_new_property_media(property_address)
                else:
                    raise ValueError(f"Unknown placeholder: {place_holder.value}")

                template_description = template_description.replace(
                    f'{place_holder.value}:',
                    f"{place_holder.value}: {updated_description}"
                )
            else:
                print(f"Placeholder not found: {place_holder.value}. Having an issue here.")

        # Create a new task
        new_task_body = {
            "data": {
                "name": property_address,
                "notes": template_description,
                "projects": LEADS_PROJECT_ID,  # Copy the same project association
            }
        }

        new_task = tasks_api.create_task(new_task_body, opts=[])
        add_task_to_section(task_id=new_task["gid"], section_id=LEADS_PROPERTIES_SECTION)
        print("New task created successfully!")
        print("New Task ID:", new_task['gid'])
        #print("New Task Description:", new_task['notes'])
        task_link: str = f"https://app.asana.com/0/{LEADS_PROJECT_ID}/{new_task['gid']}/f"
        print(f'Task link for {property_address}: {task_link}')
        return task_link

    except ApiException as e:
        print("Error occurred:", e)
