from typing import Any, Optional

from pydantic import ConfigDict

from fa_common.models import CamelModel, StorageLocation

from .enums import EmailBodyType


class ExtraContent(CamelModel):
    type: EmailBodyType = EmailBodyType.PLAIN
    body: str = ""


class CallbackMetaData(CamelModel):
    """
    storage_location: should contain the base path to
                      where the workflows are stored
    ui_res_link:      USE THIS IF YOU WISH TO EMBED a
                      LINK to THE RESULTS IN UI.
    """

    storage_location: StorageLocation | None = None
    project_id: Optional[str] = None
    project_name: Optional[str] = ""
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_name: Optional[str] = None
    ui_res_link: Optional[str] = None
    extra_content: Optional[ExtraContent] = None
    show_detailed_info: Optional[bool] = True


class Attachment(CamelModel):
    filename: str
    content: Any

    model_config = ConfigDict(arbitrary_types_allowed=True)
