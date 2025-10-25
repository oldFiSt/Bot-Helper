__all__ = ("router", )
from aiogram import Router

from.commands import router as commands_router
from .callback_handlers import router as cb_handlers_router

router =  Router()

router.include_router(commands_router)
router.include_router(cb_handlers_router)