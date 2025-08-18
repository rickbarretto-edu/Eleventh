"""RTP - Rick Transfer Protocol

Message Exchange Example
========================

Request
-------

    POST /protocols/create RTP
    size: ...
    type: JSON

    {
        "protocol": "Rick Transfer Protocol",
        "abbr": "RTP",
    }

    
Response
--------

    RTP 200 OK
    size: ...
    type: HTML

    <section>
        Created Protocol: <strong>Rick Transfer Protocol (RTP)</strong>
    </section>


"""