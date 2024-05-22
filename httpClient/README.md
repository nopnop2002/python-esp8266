# httpClient(REST Client)
This example uses [this](https://github.com/typicode/json-server) for the http server.   
If you use a server other than json-server, you will need to change the POST and PUT JSON data.   

# Install json-server (Fake REST Server) stable version on your host
```
sudo apt install npm
sudo npm install -g json-server@0.17.4
```

# Create db.json on your host
```
{
  "sample": [
    {
      "id": 1,
      "title": "json-server",
      "author": "typicode"
    }
  ]
}
```

# Start json-server (Fake REST Server)
If the host parameter is not specified, it can only be accessed from local host.   
When accessing from ESP32, host parameter is required.   
```
json-server --watch --host {My_IP_Address} db.json
```

![JSON_Server](https://user-images.githubusercontent.com/6020549/71557207-3320e700-2a86-11ea-9761-823007c4b370.jpg)


# Start example
```
git clone https://github.com/nopnop2002/python-esp8266
cd python-esp8266/httpClient

sudo -E python3 main.py --help
usage: main.py [-h] [--device DEVICE] [--speed SPEED] [--timeout TIMEOUT] --host HOST --port PORT [--debug]

options:
  -h, --help         show this help message and exit
  --device DEVICE    uart device file name
  --speed SPEED      uart baudrate
  --timeout TIMEOUT  uart timeout
  --host HOST        http host to connect to
  --port PORT        http port to connect to
  --debug            enable debug print

# Root privileges are required on Ubuntu/Debian
sudo -E python3 main.py --device /dev/ttyS3 --host your_host --port your_port

# buildroot does not require root privileges
python3 main.py --device /dev/ttyS3 --host your_host --port your_port

device=/dev/ttyS3
speed=115200
debug=False
host=192.168.10.41
port=3000
client.start = True
client.get = True
[
  {
    "id": 1,
    "title": "json-server",
    "author": "typicode"
  }
]
Hit Enter key to Put new record

connectServer _ret=True
sendData _ret=[OK]
closeServer _ret=True
client.post = True
client.get = True
[
  {
    "id": 1,
    "title": "json-server",
    "author": "typicode"
  },
  {
    "title": "test",
    "auther": "nopnop2002",
    "id": 2
  }
]
Hit Enter key to modify record

client.put = True
{
  "title": "test_update",
  "auther": "nopnop2002_update",
  "id": 2
}
Hit Enter key to delete record

client.delete = True
client.get = True
[
  {
    "id": 1,
    "title": "json-server",
    "author": "typicode"
  }
]
```

# Using curl
```
# Set your host & port
export HOST="192.168.10.41"
export PORT=3000

# Get
curl http://${HOST}:${PORT}/sample

# Put
curl -H "Content-Type: application/json" -d '{"title":"test"}' -X POST http://${HOST}:${PORT}/posts

# Post
curl -H "Content-Type: application/json" -d '{"title":"test update", "auther":"nopnop2003"}' -X PUT http://${HOST}:${PORT}0/sample/2

# Delete
curl -H "Content-Type: application/json" -X DELETE http://${HOST}:${PORT}/sample/2
```
