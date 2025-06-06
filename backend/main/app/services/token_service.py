from datetime import datetime, timedelta

from app.extensions import db
from app.models.token import TokenBalance, Token
from web3 import Web3

class TokenService:
    def __init__(self):
        # RPC-провайдер Polygon
        self.w3 = Web3(Web3.HTTPProvider("https://polygon-rpc.com"))

        # Адрес токена и его ABI
        self.token_address = self.w3.to_checksum_address("0x1a9b54a3075119f1546c52ca0940551a6ce5d2d0")

        self.abi = [
            {
                "constant": True,
                "inputs": [],
                "name": "name",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "symbol",
                "outputs": [{"name": "", "type": "string"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "decimals",
                "outputs": [{"name": "", "type": "uint8"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function",
            },
            {
                "constant": True,
                "inputs": [{"name": "_owner", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "balance", "type": "uint256"}],
                "type": "function",
            },
        ]

        self.contract = self.w3.eth.contract(address=self.token_address, abi=self.abi)

        # Получаем decimals один раз при инициализации
        self.decimals = self.contract.functions.decimals().call()

    def fetch_token_info(self, address: str) -> dict:
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(address), abi=self.abi)

        try:
            try:
                symbol = contract.functions.symbol().call()
            except:
                symbol = "UNKNOWN"
            try:
                name = contract.functions.name().call()
            except:
                name = "UNKNOWN"
            try:
                total_supply = contract.functions.totalSupply().call()
            except:
                total_supply = 0.0
            try:
                balance = self.get_balance(address)
            except:
                balance = 0.0

            last_tx = datetime.utcnow()

            return {
                "symbol": symbol,
                "name": name,
                "total_supply": total_supply,
                "balance": balance,
                "last_transaction": last_tx,
            }
        except Exception as e:
            raise RuntimeError(f"Ошибка при получении данных токена: {str(e)}")

    def get_balance(self, address: str) -> TokenBalance:
        # Чексуим-адрес (в Polygon/Ethereum все адреса должны быть с проверкой регистра)
        checksum_address = self.w3.to_checksum_address(address)

        # Запрашиваем сырой баланс
        raw_balance = self.contract.functions.balanceOf(checksum_address).call()

        # Переводим в "человеческие" единицы
        normalized_balance = raw_balance / (10 ** self.decimals)

        return normalized_balance

    def update_or_create_token(self, address: str) -> Token:
        data = self.fetch_token_info(address)

        token = Token.query.filter_by(address=address).first()

        if token:
            token.balance = data["balance"]
            token.symbol = data["symbol"]
            token.name = data["name"]
            token.total_supply = data["total_supply"]
            token.last_transaction = data["last_transaction"]
        else:
            token = Token(
                address=address,
                balance=data["balance"],
                symbol=data["symbol"],
                name=data["name"],
                total_supply=data["total_supply"],
                last_transaction=data["last_transaction"]
            )
            db.session.add(token)

        db.session.commit()
        return token

    def get_token(self, address: str) -> Token:
        token = Token.query.filter_by(address=address).first()
        if token and token.updated_at and token.updated_at > datetime.utcnow() - timedelta(hours=1):
            return token
        else:
            return self.update_or_create_token(address)


    def get_top_tokens(self, limit: int = 10):
        return Token.query.order_by(Token.balance.desc()).limit(limit).all()
