
import asyncio
from pylecular.node import Node
from pylecular.transporter.base import Transporter
from pylecular.packet import Packet, Topics
import psutil


class Transit:
    def __init__(self, node_id=None, registry=None, node_catalog=None, settings=None, logger=None, lifecycle=None):
        self.node_id = node_id
        self.registry = registry
        self.node_catalog = node_catalog
        self.logger = logger
        self.transporter = Transporter.get_by_name(
            settings.transporter.split("://")[0], 
            {"connection": settings.transporter}, 
            transit=self, handler=self.__message_handler__, node_id=node_id)
        self._pending_requests = {} 
        self.lifecycle = lifecycle


    async def __message_handler__(self, packet: Packet):
        if packet.type == Topics.INFO:
            await self.info_handler(packet)
        elif packet.type == Topics.DISCOVER:
            await self.discover_handler(packet)
        elif packet.type == Topics.HEARTBEAT:
            await self.heartbeat_handler(packet)
        elif packet.type == Topics.REQUEST:
            await self.request_handler(packet)
        elif packet.type == Topics.RESPONSE:
            await self.response_handler(packet)
        elif packet.type == Topics.EVENT:
            await self.event_handler(packet)
        elif packet.type == Topics.DISCONNECT:
            await self.disconnect_handler(packet)

    async def __make_subscriptions__(self):
        await self.transporter.subscribe(Topics.INFO.value)
        await self.transporter.subscribe(Topics.INFO.value, self.node_id)
        await self.transporter.subscribe(Topics.DISCONNECT.value)
        await self.transporter.subscribe(Topics.HEARTBEAT.value)
        await self.transporter.subscribe(Topics.REQUEST.value, self.node_id)
        await self.transporter.subscribe(Topics.RESPONSE.value, self.node_id)
        await self.transporter.subscribe(Topics.EVENT.value, self.node_id)


    async def connect(self):
        await self.transporter.connect()
        await self.discover()
        await self.send_node_info()
        await self.__make_subscriptions__()

        
    async def disconnect(self):
        await self.publish(Packet(Topics.DISCONNECT, None, {}))
        for future in self._pending_requests.values():
            if not future.done():
                future.cancel()
        self._pending_requests.clear()
        await self.transporter.disconnect()

    async def publish(self, packet: Packet):
        await self.transporter.publish(packet)


    async def discover(self):
        await self.publish(Packet(Topics.DISCOVER, None, {}))


    async def beat(self):
        heartbeat = { # TODO: move to node catalog
            "cpu": psutil.cpu_percent(interval=1),

        }
        await self.publish(Packet(Topics.HEARTBEAT, None, heartbeat))

    async def send_node_info(self):
        await self.publish(Packet(Topics.INFO, None, self.node_catalog.local_node.get_info()))


    async def discover_handler(self, packet: Packet):
        await self.send_node_info()

    async def heartbeat_handler(self, packet: Packet):
        # TODO: setup heartbeat times
        pass

    async def info_handler(self, packet: Packet):
        node = Node(
            id=packet.payload.get("id"),
            **{k: v for k, v in packet.payload.items() if k != "id"})
        self.node_catalog.add_node(packet.target, node)

    async def disconnect_handler(self, packet: Packet):
        self.node_catalog.disconnect_node(packet.target)

    async def event_handler(self,packet: Packet):
        endpoint = self.registry.get_event(packet.payload.get("event"))
        if endpoint and endpoint.is_local:
            context = self.lifecycle.rebuild_context(packet.payload)
            try:
                await endpoint.handler(context)
            except Exception as e:
                self.logger.error(f"Failed to process event {endpoint.name}")
                self.logger.error(e)

    async def request_handler(self, packet: Packet):
        endpoint = self.registry.get_action(packet.payload.get("action"))
        if endpoint and endpoint.is_local:
            context = self.lifecycle.rebuild_context(packet.payload)
            try:
                result = await endpoint.handler(context)
                response = {
                    "id": context.id,
                    "data": result,
                    "success": True,
                    "meta": {}
                }
                await self.publish(Packet(Topics.RESPONSE, packet.target, response))
            except Exception as e:
                self.logger.error(f"Failed call to {endpoint.name}.", e)

    async def response_handler(self, packet: Packet):
        req_id = packet.payload.get("id")
        future = self._pending_requests.pop(req_id, None)
        if future:
            future.set_result(packet.payload)

    async def request(self, endpoint, context):
        req_id = context.id
        future = asyncio.get_running_loop().create_future()
        self._pending_requests[req_id] = future
        await self.publish(Packet(Topics.REQUEST, endpoint.node_id, context.marshall()))
        try:
            response = await asyncio.wait_for(future, 5000) # TODO: fetch timeout from settings
            return response.get("data")
        except asyncio.TimeoutError:
            self._pending_requests.pop(req_id, None)
            # Optionally log or raise a custom exception
            return None
        

    async def send_event(self, endpoint, context):
        await self.publish(Packet(Topics.EVENT, endpoint.node_id, context.marshall()))


