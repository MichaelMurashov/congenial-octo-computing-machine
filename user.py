import logging
from cashvoucher import CashVoucher

logger = logging.getLogger(__name__)

class User:
	def __init__(self, id):
		self.id = id
		self.sum = 0;

	def add_purchase(self, file_path):
		cash_voucher = CashVoucher()
		cash_voucher.load(file_path)

		logger.info('Successful load cash voucher from file %s' 
			% file_path)

		self.sum += cash_voucher.parsed['totalSum'] / 100
