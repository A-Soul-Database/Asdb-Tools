from xmlrpc.client import ServerProxy
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
class ThreadXMLRPCServer(ThreadingMixIn,SimpleXMLRPCServer):pass
class serv:
    def receiveSignal(self,service:str,info:dict):
        """
        接收xmlrpc消息
        service: ["Liveroom_Monitor","Record_Monitor","Dynamtic_Monitor"]
        info:{
            error:0/1,
            data:{}
        }
        """
        print(f"error : {service}:{info}") if info["error"] else print(f"{service}:{info}")

print(ServerProxy("http://localhost:5005").Liveroom_Bot())
#print(ServerProxy("http://localhost:5007").RecordMonitor())
#print(ServerProxy("http://localhost:5008").Download_Bili_Video("BV1GF411q7rL"))
#print(ServerProxy("http://localhost:5010").Spider_TimeLine("BV12q4y1B7gT"))


servers = serv()
server = ThreadXMLRPCServer(("localhost", 5002),allow_none=True)
server.register_instance(servers)
print("Listening on port 5002")
server.serve_forever()