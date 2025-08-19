"""RTP - Rick Transfer Protocol

Structure
=========

Request
-------

Request must contain 4 lines of Header, an empty separating line and the body.
The header has:
1. ``<Method> <Path> <Version>``: Action and Routing.
2. ``size: <Size>``: The byte size of the body.
3. ``type: <Type>``: the kind of content the body has.
4. ``connection: <Connection>``: describes if the connection should be kept alive.
5. Empty line
6. ``<Body>``

Response
--------

Request must contain 4 lines of Header, an empty separating line and the body.
The header has:
1. ``<Version> <StatusCode> <Reason>``: Response Status.
2. ``size: <Size>``
3. ``type: <Type>``
4. ``connection: <Connection>``
5. Empty line
6. ``<Body>``

Definitions
-----------

* Method: Can be anything, the implementation is flexible enough to fit in any domain model.
* Path: Must follow the same rules from HTTP's path
* Version: RTP/<version>, like: RTP/1.0
* Size: The bytes size of the body content
* Type: The type of file the body has: use the same file extension.
* Connection: May be "close" or "keep", so the server knows if this should be kept 
    or closed right after the first response.
* StatusCode: ``int`` number, follows a subset of HTTP one.
* Reason: The description of the StatusCode. Also follows a subset of the HTTP one.
* Body: The message itself.


Message Exchange Example
========================

Request
-------

    POST /protocols/create RTP/1.0
    size: ...
    type: JSON
    connection: close

    {
        "protocol": "Rick Transfer Protocol",
        "version": "1.0",
        "abbr": "RTP",
    }

    
Response
--------

    RTP/1.0 200 OK
    size: ...
    type: HTML
    connection: close

    <section>
        Created Protocol: <strong>Rick Transfer Protocol v1.0 (RTP/1.0)</strong>
    </section>


"""

from . import request
from . import response