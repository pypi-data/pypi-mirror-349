# OpenVPN Management Interface Python API

[![PyPI](https://img.shields.io/pypi/v/openvpn-management-api.svg)](https://pypi.org/project/openvpn-management-api/)

## Summary

> [!IMPORTANT]
> This project is a fork of the [Jamie-/openvpn-api](https://github.com/Jamie-/openvpn-api) project. It presents support for receiving events and registering callbacks for them, which is not present in the original version. The original repository is abandoned; this is an attempt at reviving it.

A Python API for interacting with the OpenVPN management interface.

Very useful for extracting metrics and status from OpenVPN server management interfaces, and authorizing users with an external source.

This project was inspired by the work of Marcus Furlong in creating [openvpn-monitor](https://github.com/furlongm/openvpn-monitor).
It also uses [openvpn-status](https://pypi.org/project/openvpn-status/) by Jiangge Zhang for parsing the output of the OpenVPN `status` command as there's no point reinventing the wheel when an excellent solution already exists.

Release notes can be found [here on GitHub](https://github.com/HosseyNJF/openvpn-management-api/releases).

:warning: This project is not yet stable and there are no guarantees for it to work. You are welcome to [submit any bugs](https://github.com/HosseyNJF/openvpn-management-api/issues/new) you may encounter, and I'll be happy to help.

When using and developing this library, you may find the manual for the OpenVPN [management interface](https://openvpn.net/community-resources/controlling-a-running-openvpn-process/#using-the-management-interface) useful: https://openvpn.net/community-resources/management-interface/


## Requirements
This project requires Python >= 3.6.

Dependencies:
* [openvpn-status](https://pypi.org/project/openvpn-status/)

## Installation

#### Via PyPI
```
pip install openvpn-management-api
```

#### Via Source
```
git clone https://github.com/HosseyNJF/openvpn-management-api.git
cd openvpn-management-api
python setup.py install
```

## Usage

### Introduction
Create a `VPN` object for your management interface connection.

```python
import openvpn_management_api.VPN

v = openvpn_management_api.VPN('localhost', 7505)
```

Then you can either manage connection and disconnection yourself
```python
v.connect()
# Do some stuff, e.g.
print(v.release)
v.disconnect()
```
If the connection is successful, `v.connect()` will return `True`.
However, if the connection fails `v.connect()` will raise an `openvpn_management_api.errors.ConnectError` exception with the reason for the connection failure.

Or use the connection context manager
```python
with v.connection():
    # Do some stuff, e.g.
    print(v.release)
```

After initialising a VPN object, we can query specifics about it.

We can get the address we're communicating to the management interface on
```python
>>> v.mgmt_address
'localhost:7505'
```

And also see if this is via TCP/IP or a Unix socket
```python
>>> v.type
'ip'
```

or
```python
>>> v.type
'socket'
```

These are represented by the `VPNType` class as `VPNType.IP` or `VPNType.UNIX_SOCKET`
```python
>>> v.type
'ip'
>>> v.type == openvpn_management_api.VPNType.IP
True
```

### Consume events

The management interface emits events on specific occasions, as specified in [this documentation](https://openvpn.net/community-resources/management-interface/), that can be consumed using this library:

```python3
def event_handler(event: ClientEvent):
    print(f"Received event: " + event.type)

v.register_callback(ClientEvent, event_handler)
```

#### Available events

Two classes of events may be emitted by the server:

##### UpDownEvent

This event is fired when the server shuts down or is started.

Available properties:

`event.type` - either "UP" or "DOWN"

##### ClientEvent

This event is fired on client activity, such as `CONNECT`, `REAUTH`, `ESTABLISHED`, `DISCONNECT`, and `ADDRESS`.

Available properties:

| Name        | Value Type                                                        |
|-------------|-------------------------------------------------------------------|
| event_type  | Enum[`CONNECT`, `REAUTH`, `ESTABLISHED`, `DISCONNECT`, `ADDRESS`] |
| client_id   | int                                                               |
| key_id      | Optional[int]                                                     |
| primary     | Optional[int]                                                     |
| address     | Optional[str]                                                     |
| environment | Dict[str, str]                                                    |

#### Known limitations

- Callbacks should be kept as lightweight as possible and not perform any heavy or time-consuming computation. If you need more, add the event to a queue and consume it separately.
- **Never** send an OpenVPN command inside a callback. instead, add it to your own queue and process it outside the callback .

### Daemon Interaction
All the properties that get information about the OpenVPN service you're connected to are stateful.
The first time you call one of these methods it caches the information it needs so future calls are super fast.
The information cached is unlikely to change often, unlike the status and metrics we can also fetch which are likely to change very frequently.

We can fetch the release string for the version of OpenVPN we're using
```python
>>> v.release
'OpenVPN 2.4.4 x86_64-pc-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Sep  5 2018'
```

Or just the version number
```python
>>> v.version
'2.4.4'
```

The information cached by these 2 properties can be cleared and will be repopulated on the next call
```python
v.clear_cache()
```

#### Daemon State

We can get more information about the service by looking at it's state which is returned as a State object
```python
>>> v.get_state()
<State desc='SUCCESS', mode='server'>
```

The State object contains the following things:

The daemon's current mode, `client` or `server`
```python
>>> s = v.get_state()
>>> s.mode
'server'
```

Date and time the daemon was started
```python
>>> s.up_since
datetime.datetime(2019, 6, 5, 23, 3, 21)
```

The daemon's current state
```python
>>> s.state_name
'CONNECTED'
```
Which can be any of:
* `CONNECTING` - OpenVPN's initial state.
* `WAIT` - (Client only) Waiting for initial response from server.
* `AUTH` - (Client only) Authenticating with server.
* `GET_CONFIG` - (Client only) Downloading configuration options from server.
* `ASSIGN_IP` - Assigning IP address to virtual network interface.
* `ADD_ROUTES` - Adding routes to system.
* `CONNECTED` - Initialization Sequence Completed.
* `RECONNECTING` - A restart has occurred.
* `EXITING` - A graceful exit is in progress.
* `RESOLVE` - (Client only) DNS lookup
* `TCP_CONNECT` - (Client only) Connecting to TCP server

The descriptive string - unclear from the OpenVPN documentation quite what this is, usually `SUCCESS` or the reason for disconnection if the state is `RECONNECTING` or `EXITING`
```python
>>> s.desc_string
'SUCCESS'
```

The daemon's local virtual (VPN internal) v4 address, returned as an `ipaddress.IPv4Address` for ease of sorting, it can be easily converted to a string with `str()`
```python
>>> s.local_virtual_v4_addr
IPv4Address('10.0.0.1')
>>> str(s.local_virtual_v4_addr)
'10.0.0.1'
```

If the daemon is in client mode, then `remote_addr` and `remote_port` will be populated with the address and port of the remote server
```python
>>> s.remote_addr
IPv4Address('1.2.3.4')
>>> s.remote_port
1194
```

If the daemon is in server mode, then `local_addr` and `local_port` will be populated with the address and port of the exposed server
```python
>>> s.local_addr
IPv4Address('5.6.7.8')
>>> s.local_port
1194
```

If the daemon is using IPv6 instead of, or in addition to, IPv4 then the there is also a field for the local virtual (VPN internal) v6 address
```python
>>> s.local_virtual_v6_addr
'2001:db8:85a3::8a2e:370:7334'
```

#### Daemon Status
The daemon status is parsed from the management interface by `openvpn_status` an existing Python library for parsing the output from OpenVPN's status response.
The code for which can be found in it's GitHub repo: https://github.com/tonyseek/openvpn-status

Therefore when we fetch the status from the OpenVPN daemon, it'll be returned using their models.
For more information see their docs: https://openvpn-status.readthedocs.io/en/latest/api.html

Unlike the VPN state, the status is not stateful as it's output is highly likely to change between calls.
Every time the status is requested, the management interface is queried for the latest data.

A brief example:
```python
>>> status = v.get_status()
>>> status
<openvpn_status.models.Status object at 0x7f5eb54a2d68>
>>> status.client_list
OrderedDict([('1.2.3.4:56789', <openvpn_status.models.Client object at 0x7f5eb54a2128>)])
```
