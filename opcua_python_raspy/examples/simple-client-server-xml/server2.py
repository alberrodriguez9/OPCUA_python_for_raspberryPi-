import os.path
try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()

from opcua import ua, uamethod, Server


@uamethod
def say_hello_xml(parent, happy):
    print("Calling say_hello_xml")
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return result


@uamethod
def say_hello(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return result


@uamethod
def say_hello_array(parent, happy):
    if happy:
        result = "I'm happy"
    else:
        result = "I'm not happy"
    print(result)
    return [result, "Actually I am"]


@uamethod
def switch_mtd(parent):

	print("HELLO WORLD")


class HelloServer:
    def __init__(self, endpoint, name, model_filepath):
        self.server = Server()

        #  This need to be imported at the start or else it will overwrite the data
        self.server.import_xml(model_filepath)

        self.server.set_endpoint(endpoint)
        self.server.set_server_name(name)

        objects = self.server.get_objects_node()
	
	ESP8266=self.server.get_node("ns=0;i=20005")
	print("ESP8266: ")
	print(ESP8266)	

	#death_button=ESP8266.get_children()
	watering_status=ESP8266.get_value()
	print(watering_status)
	switch_method=self.server.get_node("ns=0;i=20006")
        freeopcua_namespace = self.server.get_namespace_index("urn:freeopcua:python:server")
#        hellower = objects.get_child("0:Hellower")
#        hellower_say_hello = hellower.get_child("0:SayHello")
	self.server.link_method(switch_method, switch_mtd)
#        self.server.link_method(hellower_say_hello, say_hello_xml)

#        hellower.add_method(
#            freeopcua_namespace, "SayHello2", say_hello, [ua.VariantType.Boolean], [ua.VariantType.String])

#        hellower.add_method(
#            freeopcua_namespace, "SayHelloArray", say_hello_array, [ua.VariantType.Boolean], [ua.VariantType.String])

    def __enter__(self):
        self.server.start()
        return self.server

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.server.stop()


if __name__ == '__main__':
    script_dir = os.path.dirname(__file__)
    with HelloServer(
            "opc.tcp://0.0.0.0:4840/freeopcua/server/",
            "FreeOpcUa Example Server",
            os.path.join(script_dir, "/home/alrodriguez/Desktop/freeopcua_modeler1/model1.xml")) as server:
        embed()
