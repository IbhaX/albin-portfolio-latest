import json
import asyncio
import logging
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class LogConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for streaming real-time logs to admin users."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        # Check if user is authenticated and is admin
        user = self.scope.get('user')
        
        if not user or not user.is_authenticated:
            await self.close(code=4001)
            return
        
        is_admin = await self.check_admin(user)
        if not is_admin:
            await self.close(code=4003)
            return
        
        await self.accept()
        
        # Send welcome message
        await self.send(text_data=json.dumps({
            'type': 'system',
            'message': f'Connected to IBHAX Log Stream',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }))
        
        # Add to logs group
        await self.channel_layer.group_add('admin_logs', self.channel_name)
        
        # Start streaming logs
        self.streaming = True
        asyncio.create_task(self.stream_logs())
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        self.streaming = False
        await self.channel_layer.group_discard('admin_logs', self.channel_name)
    
    async def receive(self, text_data):
        """Handle incoming messages from client."""
        try:
            data = json.loads(text_data)
            command = data.get('command')
            
            if command == 'clear':
                await self.send(text_data=json.dumps({
                    'type': 'clear',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }))
            elif command == 'ping':
                await self.send(text_data=json.dumps({
                    'type': 'pong',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }))
        except json.JSONDecodeError:
            pass
    
    async def stream_logs(self):
        """Stream Django logs in real-time."""
        # Get the custom log handler
        log_handler = DjangoWebSocketLogHandler.get_instance()
        if log_handler:
            log_handler.add_consumer(self)
        
        # Keep connection alive
        while self.streaming:
            await asyncio.sleep(1)
        
        if log_handler:
            log_handler.remove_consumer(self)
    
    async def send_log(self, log_entry):
        """Send a log entry to the client."""
        try:
            await self.send(text_data=json.dumps(log_entry))
        except Exception:
            pass
    
    async def log_message(self, event):
        """Handle log messages from channel layer."""
        await self.send(text_data=json.dumps(event['data']))
    
    @database_sync_to_async
    def check_admin(self, user):
        """Check if user is admin."""
        return user.is_staff or user.is_superuser


class DjangoWebSocketLogHandler(logging.Handler):
    """Custom logging handler that sends logs to WebSocket consumers."""
    
    _instance = None
    
    def __init__(self):
        super().__init__()
        self.consumers = set()
        self.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%H:%M:%S'
        ))
        DjangoWebSocketLogHandler._instance = self
    
    @classmethod
    def get_instance(cls):
        return cls._instance
    
    def add_consumer(self, consumer):
        self.consumers.add(consumer)
    
    def remove_consumer(self, consumer):
        self.consumers.discard(consumer)
    
    def emit(self, record):
        """Emit a log record to all connected consumers."""
        if not self.consumers:
            return
        
        try:
            log_entry = {
                'type': 'log',
                'level': record.levelname.lower(),
                'logger': record.name,
                'message': self.format(record),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            }
            
            for consumer in list(self.consumers):
                asyncio.create_task(consumer.send_log(log_entry))
        except Exception:
            pass


# Setup the log handler
def setup_websocket_logging():
    """Setup WebSocket logging handler."""
    handler = DjangoWebSocketLogHandler()
    handler.setLevel(logging.DEBUG)
    
    # Add to Django logger
    django_logger = logging.getLogger('django')
    django_logger.addHandler(handler)
    
    # Add to request logger
    request_logger = logging.getLogger('django.request')
    request_logger.addHandler(handler)
    
    # Add to server logger
    server_logger = logging.getLogger('django.server')
    server_logger.addHandler(handler)
    
    # Add to root logger for all app logs
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    
    return handler


# Initialize on module load
_log_handler = setup_websocket_logging()
