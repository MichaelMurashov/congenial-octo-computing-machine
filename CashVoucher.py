import json

class CashVoucher:
	def __init__(self):
		self.parsed = ""

	def load(self, file_path):
		file = open(file_path, encoding='utf-8')
		self.parsed = json.load(file)
		file.close()

	def isEmpty(self):
		if self.parsed == "":
			return 1
		else:
			return 0
