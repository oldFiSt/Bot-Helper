from aiogram import Router

from .info_cb_handlers import router as info_cb_router
from .action_cb_hd import router as action_cb_router

router = Router(name=__name__)

router.include_router(info_cb_router)
router.include_router(action_cb_router)