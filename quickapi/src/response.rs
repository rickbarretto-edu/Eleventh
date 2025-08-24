pub struct Response {
    pub status: u16,
    pub reason: String,
    pub body: String,
    pub content_type: String,
}

pub struct ResponseBuilder {
    status: u16,
    reason: String,
    body: String,
    content_type: String,
}

fn resp_to_string(status: u16, reason: &str, content_type: &str, body: &str) -> String {
    format!(
        "HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}",
        status,
        reason,
        content_type,
        body.len(),
        body
    )
}

impl ResponseBuilder {
    pub fn plain(mut self, body: &str) -> Response {
        self.body = body.to_string();
        self.content_type = "text/plain".to_string();
        self.build()
    }

    pub fn html(mut self, body: &str) -> Response {
        self.body = body.to_string();
        self.content_type = "text/html".to_string();
        self.build()
    }

    pub fn xml(mut self, body: &str) -> Response {
        self.body = body.to_string();
        self.content_type = "application/xml".to_string();
        self.build()
    }

    pub fn json(mut self, body: &serde_json::Value) -> Response {
        self.body = body.to_string();
        self.content_type = "application/json".to_string();
        self.build()
    }

    pub fn content(mut self, body: &str, content_type: &str) -> Response {
        self.body = body.to_string();
        self.content_type = content_type.to_string();
        self.build()
    }

    pub fn build(self) -> Response {
        Response {
            status: self.status,
            reason: self.reason,
            body: self.body,
            content_type: self.content_type,
        }
    }
}

impl Response {

    pub fn custom(status: u16, reason: &str) -> ResponseBuilder {
        ResponseBuilder {
            status,
            reason: reason.into(),
            body: String::new(),
            content_type: "text/plain".into(),
        }
    }

    pub fn ok() -> ResponseBuilder {
        ResponseBuilder {
            status: 200,
            reason: "OK".into(),
            body: String::new(),
            content_type: "text/plain".into(),
        }
    }

    pub fn bad_request() -> ResponseBuilder {
        ResponseBuilder {
            status: 400,
            reason: "Bad Request".into(),
            body: "400 Bad Request".into(),
            content_type: "text/plain".into(),
        }
    }

    pub fn unauthorized() -> ResponseBuilder {
        ResponseBuilder {
            status: 401,
            reason: "Unauthorized".into(),
            body: "401 Unauthorized".into(),
            content_type: "text/plain".into(),
        }
    }

    pub fn not_found() -> ResponseBuilder {
        ResponseBuilder {
            status: 404,
            reason: "Not Found".into(),
            body: "404 Not Found".into(),
            content_type: "text/plain".into(),
        }
    }

    pub fn internal_error() -> ResponseBuilder {
        ResponseBuilder {
            status: 500,
            reason: "Internal Server Error".into(),
            body: "500 Internal Server Error".into(),
            content_type: "text/plain".into(),
        }
    }

}


impl ToString for Response {
    fn to_string(&self) -> String {
        resp_to_string(self.status, &self.reason, &self.content_type, &self.body)
    }
}

impl Into<String> for Response {
    fn into(self) -> String {
        self.to_string()
    }
}
