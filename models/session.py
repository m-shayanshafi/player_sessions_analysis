import uuid
from cassandra.cqlengine import columns
from models.base import Base


class Session(Base):    

    player_id = columns.Text(primary_key=True, partition_key=True)
    session_id = columns.Text(primary_key=True)
    event = columns.Text()
    ts = columns.DateTime()

  #   def get_data(self):
  #       return {
  #           'player_id': str(self.player_id),
  #           'session_id': str(self.session_id),
  #           'event': self.event,
  #           'ts': str(self.ts)
		# }		

    def get_data(self):
        return {
            'player_id': self.player_id,
            'session_id': self.session_id,
            'event': self.event,
            'ts': str(self.ts)
        }       