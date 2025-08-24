pub struct Response {
    pub status: u16,
    pub reason: String,
    pub body: String,
    pub content_type: String,
}

impl Response {
    pub fn ok(body: &str, content_type: &str) -> Self {
        Self {
            status: 200,
            reason: "OK".to_string(),
            body: body.to_string(),
            content_type: content_type.to_string(),
        }
    }

    pub fn bad_request() -> Self {
        Self {
            status: 400,
            reason: "Bad Request".to_string(),
            body: "400 Bad Request".to_string(),
            content_type: "text/plain".to_string(),
        }
    }

    pub fn not_found() -> Self {
        Self {
            status: 404,
            reason: "Not Found".to_string(),
            body: "404 Not Found".to_string(),
            content_type: "text/plain".to_string(),
        }
    }

    pub fn plain(body: &str) -> Self {
        Self::ok(body, "text/plain")
    }

    pub fn html(body: &str) -> Self {
        Self::ok(body, "text/html")
    }

    pub fn xml(body: &str) -> Self {
        Self::ok(body, "application/xml")
    }

    pub fn json(body: &serde_json::Value) -> Self {
        Self {
            status: 200,
            reason: "OK".to_string(),
            body: body.to_string(),
            content_type: "application/json".to_string(),
        }
    }

    pub fn with_status(self, status: u16, reason: &str) -> Self {
        Self {
            status,
            reason: reason.to_string(),
            body: self.body,
            content_type: self.content_type,
        }
    }

    pub fn to_string(&self) -> String {
        format!(
            "HTTP/1.1 {} {}\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}",
            self.status,
            self.reason,
            self.content_type,
            self.body.len(),
            self.body
        )
    }
}
