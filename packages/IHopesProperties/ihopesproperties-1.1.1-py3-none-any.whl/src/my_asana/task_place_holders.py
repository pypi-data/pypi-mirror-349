from enum import Enum


def get_new_property_media(property_address: str):
    return ""


class TaskPlaceHolder(Enum):
    ARV_DOC = "ARV Doc"
    PROPERTY_LINK = "Property Link"
    PROPERTY_MEDIA = "Property Media"


# PLACE_HOLDERS_APPLIERS: Dict[TaskPlaceHolder, Callable[[str], str]] = {
#     TaskPlaceHolder.ARV_DOC: save_as_template_arv,
#     TaskPlaceHolder.PROPERTY_LINK: construct_zillow_property_url,
#     TaskPlaceHolder.PROPERTY_MEDIA: get_new_property_media
# }
