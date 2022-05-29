class Event():
  def __init__(self):
    self.callbacks = {}

  def bind(self, event: str, callback: callable) -> None:
    if event not in self.callbacks:
      self.callbacks[event] = [callback]
    else:
      self.callbacks[event].append(callback)

  def trigger(self, event: str, *args) -> None:
    if event in self.callbacks:
      for callback in self.callbacks[event]:
        callback(*args)

event = Event()