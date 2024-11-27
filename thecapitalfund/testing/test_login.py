from thecapitalfund.controller import login


def test_try_login_correct():
    assert login.try_login(inputted_member_id_string="EXAMPLE", inputted_user_password_string="PASSWRD") is True


def test_try_login_wrong_password():
    assert login.try_login(inputted_member_id_string="EXAMPLE", inputted_user_password_string="PASSWORD") is False


def test_try_login_empty_password():
    assert login.try_login(inputted_member_id_string="EXMAPLE", inputted_user_password_string="") is False


def test_try_login_empty_username():
    assert login.try_login(inputted_member_id_string="", inputted_user_password_string="PASSWRD") is False
