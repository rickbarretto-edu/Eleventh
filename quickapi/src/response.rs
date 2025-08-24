pub struct Response {
    pub status: u16,
    pub reason: String,
    pub body: String,
    pub content_type: String,
}

impl Response {
    pub fn new(body: &str) -> Self {
        Self {
            status: 200,
            reason: "OK".to_string(),
            body: body.to_string(),
            content_type: "text/plain".to_string(),
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

    pub fn json(body: &serde_json::Value) -> Self {
        Self {
            status: 200,
            reason: "OK".to_string(),
            body: body.to_string(),
            content_type: "application/json".to_string(),
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
