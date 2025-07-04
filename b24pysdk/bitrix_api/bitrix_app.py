from typing import Text


class BitrixApp:
	"""Local or market bitrix application"""

	__slots__ = ("client_id", "client_secret")

	def __init__(
			self,
			*,
			client_id: Text,
			client_secret: Text,
	):
		self.client_id = client_id
		self.client_secret = client_secret
