from ..models import Action
from typing import Coroutine

class ActionArgs():
  def __init__(self, name: str, short_id: str, schema: any, handler: Coroutine[Action, any, None]):
    self.name = name
    self.short_id = short_id
    self.schema = schema
    self.handler = handler

class ActionProxy():
  def __init__(self, target_proxy, args: ActionArgs, client):
    self.target = target_proxy
    self.args = args
    self.client = client
  

  async def save(self):
    action = Action(
      id=self.id(),
      name=self.args.name,
      schema=self.args.schema,
      target_id=self.target.id(),
      service_id=self.target.instance.args.service_id,
    )

    
    if action.id not in self.client.actions or self.client.actions[action.id].hash != action.hash:
      await self.client.set_data(action, 'Action')
      self.client.actions[action.id] = action
      self.client.handlers[action.id] = self.args.handler


  def id(self) -> str:
    return f"{self.target.instance.args.service_id}:{self.target.args.short_id}:{self.args.short_id}"
