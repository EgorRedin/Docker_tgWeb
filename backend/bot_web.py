from aiogram import Router, F
from aiogram.filters.chat_member_updated import (
    ChatMemberUpdatedFilter, JOIN_TRANSITION, ChatMemberUpdated
)
from queries import AsyncORM
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()
router.chat_member.filter(F.chat.id == -1002077559787)


@router.chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=JOIN_TRANSITION
    )
)
async def user_joined(event: ChatMemberUpdated):
    user_id = event.new_chat_member.user.id
    user = await AsyncORM.get_user(user_id)
    if user is None:
        return
    if not user.earn_bonus:
        await AsyncORM.update_balance(user_id, 100000)
        await AsyncORM.update_earn_bonus(user_id)


@router.message(CommandStart())
async def start_cmd(msg: Message):
    start_kb = InlineKeyboardMarkup(inline_keyboard=
                                   [
                                        [
                                            InlineKeyboardButton(text="Перейти", web_app=WebAppInfo(
                                                url="https://duo-coin.ru"))
                                        ]
                                    ])
    await msg.answer("Переход на сайт", reply_markup=start_kb)

