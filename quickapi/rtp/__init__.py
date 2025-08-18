"""RTP - Rick Transfer Protocol

Message Exchange Example
========================

Request
-------

    POST /protocols/create RTP/1.0
    size: ...
    type: JSON

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

    <section>
        Created Protocol: <strong>Rick Transfer Protocol v1.0 (RTP/1.0)</strong>
    </section>


"""