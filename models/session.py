from cassandra.cqlengine import columns
from models.base import Base

class StartSession(Base):    

    player_id = columns.Text(partition_key=True, primary_key=True)
    session_id = columns.Text(primary_key=True)
    ts = columns.DateTime()

    def get_data(self):
        return {
            'player_id': self.player_id,
            'session_id': self.session_id,
            'ts': str(self.ts)
        }

class EndSession(Base):    

    player_id = columns.Text(partition_key=True, primary_key=True)
    session_id = columns.Text(primary_key=True)
    ts = columns.DateTime()

    def get_data(self):
        return {
            'player_id': self.player_id,
            'session_id': self.session_id,
            'ts': str(self.ts)
        }       

class CompletedSession(Base):    

    player_id = columns.Text(primary_key=True, partition_key=True)
    session_id = columns.Text(primary_key=True)
    ts = columns.DateTime(primary_key=True, clustering_order="DESC")

    def get_data(self):
        
        return {
            'player_id': self.player_id,
            'session_id': self.session_id,
            'ts': str(self.ts)
        }