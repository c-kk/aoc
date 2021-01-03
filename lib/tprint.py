class Block:
	""" Utility to repeatedly print on the same space in terminal
		
		It remembers the used height and will clear the height before printing a new string.	
	"""
	y = 0

	def print(self, string):
		y = self.y
		print('\033[A\033[K' * y, end='')

		print(string)
		new_y = string.count('\n') + 1

		missing_height = y - new_y
		if missing_height > 0:
			print('\033[K\n' * missing_height, end='')

		self.y = max(y, new_y)