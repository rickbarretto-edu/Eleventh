use crate::Request;
use crate::Response;
use std::io::{Read, Write};
use std::net::TcpStream;

pub struct Client {
    url: String,
} 

impl Client {
    pub fn new(url: &str) -> Self {
        Self {
            url: url.to_string(),
        }
    }

    pub fn url(&self) -> &str {
        &self.url
    }

    pub fn get(&self, path: &str,) -> Response {
        let req = Request::new("GET", &format!("{}/{}", self.url, path), "");
        self.request(&req)
    }

    pub fn post(&self, path: &str, body: &str) -> Response {
        let req = Request::new("POST", &format!("{}/{}", self.url, path), body);
        self.request(&req)
    }

    fn request(&self, req: &Request) -> Response {
        let mut stream = TcpStream::connect(self.url()).expect("Failed to connect to server");
       let raw_request: String = req.to_string();

        stream.write_all(raw_request.as_bytes()).expect("Failed to send request");
        
        let mut buffer = Vec::new();
        stream.read_to_end(&mut buffer).expect("Failed to read response");

        let raw_response = String::from_utf8_lossy(&buffer);
        let response = Response::from_raw(&raw_response).expect("Failed to parse response");
        response
    }

}