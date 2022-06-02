


from datetime import datetime, timedelta



    
def encode_timestamp(timestamp):
    return timestamp.isoformat()

def decode_timestamp(timestamp):
    return datetime.fromisoformat(timestamp)


def future(**kwargs):
    """ Adds datetime.now + timedelta(**kwargs) """
    now = datetime.utcnow()
    time = timedelta(**kwargs)
    return now + time





