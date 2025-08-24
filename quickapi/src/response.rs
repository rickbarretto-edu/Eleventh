pub struct Response {
    pub status: u16,
    pub body: String,
    pub content_type: String,
}

impl Response {
    pub fn new(body: &str) -> Self {
        Self {
            status: 200,
            body: body.to_string(),
            content_type: "text/plain".to_string(),
        }
    }

    pub fn json(body: &serde_json::Value) -> Self {
        Self {
            status: 200,
            body: body.to_string(),
            content_type: "application/json".to_string(),
        }
    }

    pub fn to_string(&self) -> String {
        format!(
            "HTTP/1.1 {} OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}",
            self.status,
            self.content_type,
            self.body.len(),
            self.body
        )
    }
}
