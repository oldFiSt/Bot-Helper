__all__ = ("router", )

from  aiogram import Router

from .base_commands import router as base_command_router
from .user_commands import router as user_command_router
from .common import  router as common_router

router = Router(name=__name__)

router.include_router(base_command_router)
router.include_router(user_command_router)
router.include_router(common_router)