import wx

EVT_RESULT_ID = 104

class MessageEvent(wx.PyEvent):
	"""Simple event to carry arbitrary result data."""
	def __init__(self, data, release):
		"""Init Message Event."""
		wx.PyEvent.__init__(self)
		self.SetEventType(EVT_RESULT_ID)
		self.data = data
		self.release = release
