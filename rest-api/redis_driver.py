from redisai import Client
from uuid import uuid4

class RedisDriver():
    def __init__(self,):
        # This is the client we will use to make requests to Redis
        self.client = Client(host = 'redis', debug = True)

    def predict(self, input_arr):
        # Create an input tensor key
        # This is where we would store the input model
        input_tensor_key = self.__get_input_key_name()
        
        # Create an output tensor key.
        # This is the key where the output from teh ML model is stored
        output_tensor_key = self.__get_output_key_name()

        # Create the input tensor
        self.client.tensorset(input_tensor_key, tensor = input_arr)

        # Execute the model
        # Executing the model stores the output in the output tensor
        self.client.modelexecute("mobilenet", inputs = input_tensor_key, outputs = output_tensor_key)

        # Extract the details from the output tensor
        scores = self.client.tensorget(output_tensor_key, as_numpy = True)

        return scores
        
    def __get_input_key_name(self):
        return f"input-{str(uuid4())}"

    def __get_output_key_name(self):
        return f"output-{str(uuid4())}"

redis_driver = None

def initialize():
    global redis_driver

    redis_driver = RedisDriver()

def get_instance():
    global redis_driver

    return redis_driver