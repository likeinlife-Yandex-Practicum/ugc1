from kafka import KafkaProducer
from kafka.errors import KafkaError

producer = KafkaProducer(bootstrap_servers=['localhost:9094'])

result = producer.send('messages', b'my message from python')

try:
	result.get(timeout=10)
except KafkaError:
	print('something went wrong')
