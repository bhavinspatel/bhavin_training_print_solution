class Test():
	@staticmethod
	def staticMethod():
		print("Hello")

	@classmethod
	def classMethod():
		print("World")

t = Test()

t.staticMethod()
t.classMethod()

Test.staticMethod()
Test.classMethod()