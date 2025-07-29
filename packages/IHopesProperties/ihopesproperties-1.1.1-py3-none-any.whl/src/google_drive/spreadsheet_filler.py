from typing import List

from googleapiclient.discovery import Resource

from property import SoldProperty, ForSaleProperty


def write_lead_property_info_to_sheet(service: Resource, sheet_id: str, for_sale_property: ForSaleProperty) -> None:
    """
    Writes the property information to the specified Google Sheet.
    :param service:
    :param sheet_id:
    :param for_sale_property:
    :return:
    """
    sheets = service.spreadsheets()

    # Fetch the sheet data to find where "Property Info" is located
    sheet_data = sheets.values().get(spreadsheetId=sheet_id, range='ARV & Comps').execute()
    values = sheet_data.get('values', [])

    # Prepare data for insertion
    property_data = [
        [
            for_sale_property.zillow_link,  # Property Link
            for_sale_property.address.get_full_address(),
            for_sale_property.listed_date,
            f"{for_sale_property.bedrooms}/{for_sale_property.bathrooms}",
            for_sale_property.sqft,
            for_sale_property.lot_sqft,
            for_sale_property.year_built,
            "",  # Empty column currently
            "",  # Condition (optional, if applicable)
            "",  # Special Features (optional, if applicable)
            for_sale_property.asking_price
        ]
    ]

    # Write the property data to the sheet
    range_to_update = f'ARV & Comps!A2:K3'
    sheets.values().update(
        spreadsheetId=sheet_id,
        range=range_to_update,
        valueInputOption='RAW',
        body={'values': property_data}
    ).execute()


def write_comps_to_sheet(service: Resource, sheet_id: str, comps: List[SoldProperty]) -> None:
    """
    Writes the comps data to the specified Google Sheet.
    :param service: Google Sheets API resource.
    :param sheet_id: ID of the Google Sheet.
    :param comps: List of Property objects to write.
    """
    sheets = service.spreadsheets()

    # Fetch the sheet data to find where "Comps" is located
    sheet_data = sheets.values().get(spreadsheetId=sheet_id, range='ARV & Comps').execute()
    values = sheet_data.get('values', [])

    # Locate the "Comps" row
    comps_row_index = next(
        (index for index, row in enumerate(values) if "Comps" in row), None
    )
    if comps_row_index is None:
        raise ValueError("Comps section not found in the template.")

    # Starting row for the comps data
    start_row = comps_row_index + 3  # Three rows below "Comps" for headers and since it's 0-based index

    # Prepare data for insertion
    comps_data = [
        [
            comp.zillow_link,  # Property Link
            comp.address.get_full_address(),
            comp.sold_date,  # Listing Sold Date
            f"{comp.bedrooms}/{comp.bathrooms}",
            comp.sqft,
            comp.lot_sqft,  # Lot Sqf
            comp.year_built,  # Year Built (optional, if applicable)
            comp.dist_from_lead,  # distance from lead property
            "",  # Condition (optional, if applicable)
            "",  # Special Features (optional, if applicable)
            comp.sold_price
        ]
        for comp in comps
    ]

    # Write the comps data to the sheet
    range_to_update = f'ARV & Comps!A{start_row}:K{start_row + len(comps_data) - 1}'
    sheets.values().update(
        spreadsheetId=sheet_id,
        range=range_to_update,
        valueInputOption='RAW',
        body={'values': comps_data}
    ).execute()
