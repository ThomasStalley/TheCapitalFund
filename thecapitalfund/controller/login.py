import os

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerificationError, VerifyMismatchError
from dotenv import load_dotenv

from thecapitalfund.model import members

load_dotenv()

pepper_string = os.environ.get("PEPPER")


def try_login(inputted_member_id_string: str, inputted_user_password_string: str) -> bool:
    """Get stored password, and verify it matches inputted password."""
    # check for user id:
    if not inputted_member_id_string:
        return False
    # check account is found:
    member_account = members.get_single_member_data(inputted_member_id_string)
    if not member_account:
        return False
    # check password is found:
    stored_psh_password = member_account.get("PASSWORD", None)
    if not stored_psh_password:
        return False
    # create a peppered password, to be inserted into argon password checker:
    inputted_peppered_password = inputted_user_password_string + pepper_string
    # verify the inputted psh password matches stored psh password:
    try:
        password_hasher = PasswordHasher()
        password_hasher.verify(stored_psh_password, inputted_peppered_password)
        return True
    except (VerifyMismatchError, VerificationError, InvalidHash):
        return False
