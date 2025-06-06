import re
from marshmallow import Schema, fields, validates, ValidationError, validates_schema, post_load
from web3 import Web3
from app.models.token import TokenBalance
from app.schemas.base import BaseSchema, HistorySchema

class TokenABTSchema(Schema):
    address = fields.String(required=True)
    balance = fields.Float()
    last_transaction = fields.DateTime(allow_none=True)

    @validates("address")
    def validate_address(self, value):
        """Проверка корректности Ethereum адреса"""
        if not Web3.is_address(value):
            raise ValidationError("Невалидный адрес Ethereum")

class TokenABSchema(Schema):
    address = fields.String(required=True)
    balance = fields.Float()

    @validates("address")
    def validate_address(self, value):
        """Проверка корректности Ethereum адреса"""
        if not Web3.is_address(value):
            raise ValidationError("Невалидный адрес Ethereum")

class TokenFullSchema(Schema):
    address = fields.String(required=True)
    balance = fields.Float()
    symbol = fields.String()
    name = fields.String()
    total_supply = fields.Float()
    last_transaction = fields.DateTime(allow_none=True,)
    last_updated = fields.DateTime()

    @validates("address")
    def validate_address(self, value):
        """Проверка корректности Ethereum адреса"""
        if not Web3.is_address(value):
            raise ValidationError("Невалидный адрес Ethereum")


class BatchBalanceSchema(Schema):
    addresses = fields.List(fields.String(), required=True)

    @validates("addresses")
    def validate_addresses(self, value):
        if not value:
            raise ValidationError("Список адресов не может быть пустым")
        for addr in value:
            if not Web3.is_address(addr):
                raise ValidationError(f"Невалидный адрес: {addr}")


class TokenBalanceSchema(Schema):
    address = fields.String(required=True)
    balance = fields.Float(required=True)

class BalanceSchema(Schema):
    balance = fields.Float(required=True)

class BalancesSchema(Schema):
    balances = fields.List(fields.Float(), required=True)