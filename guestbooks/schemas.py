from app import ma
from marshmallow import fields, decorators


# GuestBook Schema
class GuestBookSchema(ma.Schema):

    id = fields.Integer(required=False, allow_none=True)
    name = fields.String(required=True)
    message = fields.String(required=True)
    subject = fields.String(required=True)


class RegisterGuestBookSchema(GuestBookSchema):

    @decorators.pre_load
    def unwrap_envelope(self, data, **kwargs):
        if data.get("name", None) is not None and data.get("name", None).strip() == "":
            data["name"] = None

        if data.get("message", None) is not None and data.get("message", None).strip() == "":
            data["message"] = None

        if data.get("subject", None) is not None and data.get("subject", None).strip() == "":
            data["subject"] = None

        return data


# Init Schema
guestbook_schema = GuestBookSchema()
register_guestbook_schema = RegisterGuestBookSchema()
