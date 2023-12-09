import asyncio
from typing import Union, Dict, Text, Any, Optional

from aiogram.types import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.manager.protocols import MediaAttachment
from aiogram_dialog.widgets.media import Media
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.when import WhenCondition

from config import bot



class FileIdMedia(Media):
    def __init__(
            self,
            path: Union[Text, str, None] = None,
            type: ContentType = ContentType.PHOTO,
            media_params: Dict = None,
            when: WhenCondition = None,
    ):
        super().__init__(when)
        if not (path):
            raise ValueError("Neither url nor path are provided")
        self.type = type
        if isinstance(path, str):
            path = Const(path)
        self.path = path
        self.media_params = media_params or {}

    async def _render_media(
            self, data: Any, manager: DialogManager
    ) -> Optional[MediaAttachment]:
        if self.path:
            path = await self.path.render_text(data, manager)
        else:
            path = None

        return MediaAttachment(
            path=path,
            **self.media_params,
            type=self.type
        )