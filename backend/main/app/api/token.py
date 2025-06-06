"""
API для
"""
from datetime import datetime
from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from marshmallow import ValidationError
from app.extensions import db
from app.models.base import BaseModel as BaseModelDB, HistoryModel
from app.models.token import TokenBalance
from app.schemas.base import BaseSchema, HistorySchema, PaginationSchema, DateRangeSchema, ErrorSchema, SuccessSchema
from app.schemas.token import TokenBalanceSchema, TokenFullSchema, BatchBalanceSchema, BalancesSchema, BalanceSchema, \
    TokenABSchema, TokenABTSchema
from app.services.token_service import TokenService

api = Namespace('token', description='Взаимодействия с токенами')
token_service = TokenService()


address_model = api.model('Address', {
    'address': fields.String(required=True, description='Ethereum address')
})

addresses_list_model = api.model('AddressesList', {
    'addresses': fields.List(fields.String, required=True, description='Список адресов')
})

@api.route('/get_balance')
class BalanceResource(Resource):
    @api.doc(params={'address': 'Адрес кошелька'})
    def get(self):
        """
        Получение баланса токена по адресу
        """
        try:
            # Валидация адреса через схему
            args = TokenABSchema().load(request.args)

            address = args['address']

            token = token_service.get_token(address)

            return BalanceSchema().dump({'balance': token.balance})

        except ValidationError as e:
            return {'message': 'Ошибка валидации', 'errors': e.messages}, 400


@api.route('/get_balance_batch')
class BatchBalanceResource(Resource):

    @api.expect(addresses_list_model)
    def post(self):
        try:
            data = request.get_json()
            validated = BatchBalanceSchema().load(data)

            result = []
            for address in validated['addresses']:
                token = token_service.get_token(address)
                result.append(token.balance)

            return BalancesSchema().dump({"balances": result})

        except ValidationError as e:
            return {'message': 'Ошибка валидации', 'errors': e.messages}, 400

@api.route('/get_top')
class TopTokenResource(Resource):
    @api.doc(params={'limit': 'Сколько токенов вернуть'})
    def get(self):
        try:
            limit = int(request.args.get('limit', 10))
            tokens = token_service.get_top_tokens(limit=limit)
            return TokenABSchema(many=True).dump(tokens)
        except Exception as e:
            return {"message": "Ошибка сервера", "error": str(e)}, 500

@api.route('/get_top_with_transactions')
class TopTokenResource(Resource):
    @api.doc(params={'limit': 'Сколько токенов вернуть'})
    def get(self):
        try:
            limit = int(request.args.get('limit', 10))
            tokens = token_service.get_top_tokens(limit=limit)
            return TokenABTSchema(many=True).dump(tokens)
        except Exception as e:
            return {"message": "Ошибка сервера", "error": str(e)}, 500


@api.route('/get_token_info')
class TopTokenResource(Resource):
    @api.doc(params={'address': 'Адрес кошелька'})
    def get(self):
        try:
            # Валидация адреса через схему
            args = TokenABSchema().load(request.args)
            address = args['address']
            token = token_service.get_token(address)
            return TokenFullSchema().dump(token)

        except ValidationError as e:
            return {'message': 'Ошибка валидации', 'errors': e.messages}, 400