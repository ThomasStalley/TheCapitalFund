from pydantic import BaseModel


class AppState(BaseModel):
    session: dict
    login_click: int
    home_click: int
    name: str
    password: str
    modal_header_one_text: str
    modal_header_two_text: str
    modal_header_thr_text: str
    modal_header_two_style: dict
    modal_header_thr_style: dict
    log_in_button_text: str
    log_in_button_style: dict
