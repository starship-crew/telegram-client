from data.db_session import create_session
from data.bot_user import User
import config


def save_new_user(telegram_id: int, API_TOKEN: str) -> None:
    db_sess = create_session()
    user = User(
            telegram_id=telegram_id, 
            api_token=API_TOKEN
            )
    db_sess.add(user)
    db_sess.commit()


def get_api_token(telegram_id: int) -> str or None:
    db_sess = create_session()
    token = db_sess.query(User).filter(User.telegram_id == telegram_id
                                          ).first().api_token

    return token
