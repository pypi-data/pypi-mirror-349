# aiomqttc - Asynchronous MQTT Client

An asynchronous MQTT client implementation compatible with both standard Python and MicroPython environments,
particularly optimized for ESP32 platforms.

Tested on:
- ESP32-PICO
  - MicroPython v1.23.0
  - RAM: 2MB

## Features

- Fully asynchronous operation using Python's `asyncio`
- Support for both CPython and MicroPython runtimes
- Automatic reconnection with configurable backoff strategy
- QoS 0 and QoS 1 message support
- SSL/TLS connection support
- Topic subscription and message callback handling
- Keep-alive and ping management
- Clean connection termination

## Development Setup

This project uses [`pre-commit`](https://pre-commit.com/) to enforce code quality using [Ruff](https://docs.astral.sh/ruff/).

Install it once:

```bash
pip install pre-commit
pre-commit install
```

Then, every time you commit, it will run the configured hooks.


## Installation

### For Python environments:

## Install UV if you don't have it yet

```bash
curl -sSf https://install.ultraviolet.rs | sh
```

## Clone the repository
```bash
git clone https://github.com/Tangerino/aiomqttc.git
cd aiomqttc
```

## Install the package
```bash
uv venv && uv pip install -e .
```

## Run the example
```bash
uv run main.py
2025-05-18 08:53:34.922 Stating aiomqttc example
Error reading config file: [Errno 2] No such file or directory: 'config.json'
Config file created with default values.
2025-05-18 08:53:34.923 Running... (Press Ctrl+C to exit)
2025-05-18 08:53:34.923 Connecting to broker...
2025-05-18 08:53:34.923 MQTTClient:connect. Connecting to :0
```

- ⚠️ Remember to configure the `config.json` file with your MQTT broker details.

## For MicroPython environments:

Copy `aiomqttc.py` to your device

## Configuration

The client can be configured via a JSON file. Here's an example config.json:

```json
{
  "wifi": {
    "ssid": "your_wifi_name",
    "password": "your_wifi_password"
  },
  "mqtt": {
    "broker": "broker.example.com",
    "port": 8883,
    "username": "your_username",
    "password": "your_password",
    "tls": true
  }
} 
```

## Basic usage

```python
import asyncio
from aiomqttc import MQTTClient


async def on_connect_callback(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # Subscribe to a topic
    await client.subscribe("home/+/status", qos=1)


async def message_callback(topic, message, retain):
    print(f"Received message on {topic}: {message}")


async def main():
    # Create an MQTT client
    client = MQTTClient(
        client_id="my_client",
        server="mqtt.example.com",
        port=1883,
        user="username",
        password="password",
        keepalive=60
    )

    # Set up callback for incoming messages
    client.on_connect = on_connect_callback
    client.on_message = message_callback

    # Connect to broker
    await client.connect()

    # Keep the connection alive
    try:
        while True:
            # Publish a message
            await client.publish("home/status", "online", qos=1, retain=True)
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
```

## Cross-Environment Development Benefits

One of the key advantages of aiomqttc is its ability to run identical code in both standard Python and MicroPython
environments, which offers several benefits:

### Streamlined Development Workflow
- Test on desktop, deploy to microcontrollers: Debug complex MQTT interactions on your PC before deploying to
resource-constrained devices
- Faster iteration cycles: Develop and test on CPython where debugging tools are more advanced, then deploy tested code to
MicroPython
- Consistent behavior: The same code behaves predictably across platforms, reducing environment-specific bugs

### Simplified Debugging
- Use Python's rich debugging tools in your development environment before deploying
- Test network recovery and edge cases on your development machine
- Validate MQTT communication patterns without flashing hardware repeatedly

### Advanced Use Cases
- Run the same code on ESP32 edge devices and Python-based gateways
- Create IoT systems with identical protocol handling across the entire device ecosystem
- Maintain a single codebase for all MQTT-connected components in your project

- ### Performance Optimizations
The library automatically adjusts its behavior based on the runtime environment:

- Optimizes memory usage on MicroPython platforms
- Takes advantage of more advanced asyncio features when running in CPython
- Maintains consistent API despite different underlying implementations

## API Reference
MQTTClient Class
```python
MQTTClient(client_id=None, server=None, port=1883, user=None,
           password=None, keepalive=60, ssl=False, ssl_params=None,
           verbose=0)
```
### Parameters
- client_id: Unique client identifier (auto-generated if not provided)
- server: MQTT broker hostname or IP address
- port: MQTT broker port (default: 1883)
- user: Username for authentication
- password: Password for authentication
- keepalive: Keepalive interval in seconds (default: 60)
- ssl: Enable SSL/TLS connection (default: False)
- ssl_params: SSL parameters as dictionary
- verbose: Logging verbosity (0-2)

### Methods
- async connect(timeout_sec=10): Connect to the MQTT broker
- async disconnect(): Disconnect from the broker
- async publish(topic, message, qos=1, retain=False): Publish message
- async subscribe(topic, qos=0): Subscribe to topic
- async unsubscribe(topic): Unsubscribe from topic
- reconnect_delay_set(min_delay=1, max_delay=10): Configure reconnection parameters
- get_last_error(): Get last error message

### Callbacks
- on_connect: Callback for successful connection
- on_disconnect: Callback for disconnection
- on_message: Callback for incoming messages

### License
This software is released into the public domain.
