#!/usr/local/bin/python
import sys
import pykka
import os

class LsActor(pykka.ThreadingActor):

	def on_receive(self, message):
		files = os.listdir(".")
		for filename in files:
			print(filename)
		while True:
			filename = raw_input('Enter desired filename: ')
			if os.path.isfile(filename):
				break
			print(filename + ' is not a file!')
		fileGetter = FileGetter.start()
		result = fileGetter.ask({'filename' : filename})
		fileGetter.stop()
		return result


class FileGetter(pykka.ThreadingActor):

	def on_receive(self, message):
		filename = message.get('filename')
		print(filename)
		f = open(filename)
		content = f.read()
		return content

class MainActor(pykka.ThreadingActor):

	def on_receive(self, message):
		lsActor = LsActor.start()
		result = lsActor.ask({})
		lsActor.stop()
		return result

mainActor = MainActor.start()
print(mainActor.ask({}))
mainActor.stop()