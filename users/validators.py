import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PasswordValidator:

    def __init__(self, min_length=8):
        self.min_length = min_length
        self.spc_chars = re.compile("[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]")

    def validate(self, password, user=None):

        if re.search('[0-9]', password) is None:
            raise ValidationError(_("Make sure your password has a number in it"), code='digit_not_present')

        if re.search('[A-Z]', password) is None:
            raise ValidationError(_("Make sure your password has a capital letter in it"), code='block_not_present')

        if re.search(self.spc_chars, password) is None:
            raise ValidationError(_("Make sure your password has a special character in it"), code='char_not_present')

    # def get_help_text(self, password):
    #     if len(password) < self.min_length:
    #         return _(f"Your password must have at least {self.min_length} characters.")
    #
    #     if re.search('[0-9]', password) is None:
    #         return _("Your password must have at least a number.")
    #
    #     if re.search('[A-Z]', password) is None:
    #         return _("Make sure your password has a capital letter in it")
    #
    #     if re.search(self.spc_chars, password) is None:
    #         return _("Make sure your password has a special character in it")
