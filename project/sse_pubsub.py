import json
from app import red

def subscribe_event():
    event_stream = red.pubsub()
    event_stream.subscribe('export_status')
    for msg in event_stream.listen():
        if msg['type'] != 'subscribe':
            event, data = json.loads(msg['data'])
            yield u'event: {0}\ndata: {1}\n\n'.format(event, data)

def publish_event(data):
    """ publishing COMLETE event """
    event = 'COMPLETE'
    data = '{"src": "' + str(data) + '"}'
    red.publish('export_status', json.dumps([event, data]))