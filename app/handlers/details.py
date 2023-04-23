from template import render_template
from create_bot import dp
from services import api, db
from handlers.store import detail_personal_buy_page_cb, buy_detail_cb

from aiogram.utils.callback_data import CallbackData
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def check_set_detail(API_TOKEN: str, detail_id: int) -> bool:
    on_ship = api.get_ship(API_TOKEN)["detail_copies"]
    result = False
    for i in on_ship:
        if i["id"] == detail_id:
            result = True
            break
    return result


detail_personal_upgrade_page_cb = CallbackData("personal_upgrade_page", "detail_id")
edit_detail_cb = CallbackData("edit_detatil", "action", "detail_id")


def get_numbers_keyboard(data: list, direction: str):
    numbers = InlineKeyboardMarkup(row_width=5)
    for i, detail in enumerate(data): 
        if direction == "upgrade":
            detail_id = detail["id"] 
            button = InlineKeyboardButton(
                text=str(i + 1), callback_data=detail_personal_upgrade_page_cb.new(detail_id)
            )
        elif direction == "buy": 
            detail_type_id = detail["kind"]["string_id"]
            button = InlineKeyboardButton(
                text=str(i + 1), callback_data=detail_personal_buy_page_cb.new(detail_type_id)
            )

        numbers.insert(button)
    return numbers


def get_personal_upgrade_keboard(text: str, action: str, detail_id: int):
    return InlineKeyboardMarkup().row(
        InlineKeyboardButton(
            text="LVL 🔼",
            callback_data=edit_detail_cb.new(action="upgrade", detail_id=detail_id),
        ),
        InlineKeyboardButton(
            text=text,
            callback_data=edit_detail_cb.new(action=action, detail_id=detail_id),
        ),
    )

@dp.callback_query_handler(detail_personal_upgrade_page_cb.filter())
async def detail_personal_upgrade_page(callback: types.CallbackQuery, callback_data: dict):
    if callback_data['@'] == "personal_upgrade_page":
        detail_id = int(callback_data["detail_id"])
        API_TOKEN = db.get_api_token(callback.from_user.id)

        detail = api.get_detail_copy(API_TOKEN, detail_id)

        buttons = get_personal_upgrade_keboard(text="Снять" if check_set_detail(API_TOKEN, detail_id) else "Установить", 
                                               action="put_off" if check_set_detail(API_TOKEN, detail_id) else "put_on", 
                                               detail_id=detail_id)
        await callback.message.answer(
            render_template("detail_personal_page.j2", data={"detail": detail}),
            reply_markup=buttons,
        )
        await callback.answer()


@dp.callback_query_handler(edit_detail_cb.filter(action="put_off"))
async def put_off_detail(callback: types.CallbackQuery, callback_data: dict):
    detail_id = int(callback_data["detail_id"])
    API_TOKEN = db.get_api_token(callback.from_user.id)

    detail = api.get_detail_copy(API_TOKEN, detail_id)
    required = detail["required"]

    api.detail_put_off(API_TOKEN, detail_id)
    if required:
        await callback.answer(
            "Снята обязательня деталь, корабль пока не может взлететь", show_alert=True
        )
    else:
        await callback.answer("Деталь снята")

    await callback.message.edit_reply_markup(
        get_personal_upgrade_keboard(text="Установить", action="put_on", detail_id=detail_id)
    )


@dp.callback_query_handler(edit_detail_cb.filter(action="put_on"))
async def put_on_detail(callback: types.CallbackQuery, callback_data: dict):
    detail_id = int(callback_data["detail_id"])
    API_TOKEN = db.get_api_token(callback.from_user.id)

    api.detail_put_on(API_TOKEN, detail_id)

    await callback.answer("Деталь усатновлена")
    await callback.message.edit_reply_markup(
        get_personal_upgrade_keboard(text="Снять", action="put_off", detail_id=detail_id)
    )


@dp.callback_query_handler(edit_detail_cb.filter(action="upgrade"))
async def upgrade_detail(callback: types.CallbackQuery, callback_data: dict):
    detail_id = int(callback_data["detail_id"])
    API_TOKEN = db.get_api_token(callback.from_user.id)

    cost = int(api.get_detail_copy(API_TOKEN, detail_id)["upgrade_cost"])
    currency = api.get_crew(API_TOKEN)["currency"]

    if cost > currency:
        await callback.answer(f"Недостаточно средств")
        return

    api.upgrade_detail(API_TOKEN, detail_id)

    detail = api.get_detail_copy(API_TOKEN, detail_id)

    action = "put_off" if check_set_detail(API_TOKEN, detail_id) else "put_on"

    buttons = get_personal_upgrade_keboard(
        text="Установить" if action == "put_on" else "Снять",
        action=action,
        detail_id=detail_id,
    )
    await callback.message.edit_text(
        render_template("detail_personal_page.j2", data={"detail": detail}),
        reply_markup=buttons,
    )
    await callback.answer(f"-{cost} Qk")
