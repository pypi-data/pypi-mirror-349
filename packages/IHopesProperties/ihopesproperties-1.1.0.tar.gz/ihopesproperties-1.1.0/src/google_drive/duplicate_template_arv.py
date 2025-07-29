from typing import List

from googleapiclient.discovery import Resource

from google_drive.authenticator import get_google_services
from google_drive.consts import ARV_TEMPLATE_FILE_ID
from google_drive.spreadsheet_filler import write_comps_to_sheet, write_lead_property_info_to_sheet
from property import SoldProperty, ForSaleProperty


class CompsSpreadsheet:
    def __init__(self, file_id: str, file_path: str):
        self.file_id = file_id
        self.file_path = file_path

    def __str__(self):
        return f"File ID: {self.file_id}, File path: {self.file_path}"


def copy_google_sheet(service: Resource, source_file_id: str, new_file_name: str) -> CompsSpreadsheet:
    """
    Function to copy the file and rename it
    :param service:
    :param source_file_id:
    :param new_file_name:
    :return:
    """
    # Create a copy of the file
    copied_file = service.files().copy(
        fileId=source_file_id,
        body={'name': new_file_name}
    ).execute()

    print(f"File copied and renamed to: {copied_file['name']}")
    file_path: str = f'https://docs.google.com/spreadsheets/d/{copied_file["id"]}'
    return CompsSpreadsheet(
        file_id=copied_file['id'],
        file_path=file_path
    )


def save_as_template_arv(for_sale_property: ForSaleProperty, comps: List[SoldProperty]) -> str:
    """
    Save the ARV template with the lead property and comps data.
    :param for_sale_property:
    :param comps:
    :return:
    """
    drive_service: Resource = get_google_services().drive
    sheets_service: Resource = get_google_services().sheets

    # Copy the file and rename it
    comps_doc: CompsSpreadsheet = copy_google_sheet(
        service=drive_service,
        source_file_id=ARV_TEMPLATE_FILE_ID,
        new_file_name=for_sale_property.address.get_full_address()
    )

    # Write the lead property info to the sheet
    write_lead_property_info_to_sheet(
        service=sheets_service,
        sheet_id=comps_doc.file_id,
        for_sale_property=for_sale_property
    )

    # Write comps to the sheet
    write_comps_to_sheet(
        service=sheets_service,
        sheet_id=comps_doc.file_id,
        comps=comps
    )

    return comps_doc.file_path
