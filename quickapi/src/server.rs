use std::collections::HashMap;
use std::sync::Arc;

use regex::Regex;

use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

use crate::request::Request;
use crate::response::Response;

type Handler = Box<dyn Fn(Request, HashMap<String, String>) -> Response + Send + Sync>;

pub struct Route {
    pub pattern: Regex,
    pub param_names: Vec<String>,
    pub handler: Arc<dyn Fn(Request, HashMap<String, String>) -> Response + Send + Sync>,
}

impl Clone for Route {
    fn clone(&self) -> Self {
        Self {
            pattern: self.pattern.clone(),
            param_names: self.param_names.clone(),
            handler: Arc::clone(&self.handler),
        }
    }
}

pub struct Server {
    routes: Vec<Route>,
}

impl Server {
    pub fn new() -> Self {
        Self { routes: Vec::new() }
    }

    pub fn route<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        // Convert path like /users/{id} -> regex
        let mut param_names = Vec::new();
        let regex_str = regex::escape(path)
            .replace(r"\{", "{")
            .replace(r"\}", "}")
            .replace("{", "(?P<")
            .replace("}", ">[^/]+)")
            .replace(r"\?", "?"); // allow query params

        let regex = Regex::new(&format!("^{}$", regex_str)).unwrap();

        for cap in Regex::new(r"\(\?P<([^>]+)>[^)]+\)").unwrap().captures_iter(&regex_str) {
            param_names.push(cap[1].to_string());
        }

        let route = Route {
            pattern: regex,
            param_names,
            handler: Arc::new(handler),
        };
        self.routes.push(route);
    }

    pub async fn run(&self, addr: &str) {
        let listener = TcpListener::bind(addr).await
            .expect("Failed to bind TCP listener");

        println!("Listening on {}", addr);

        loop {
            match listener.accept().await {
                Ok((socket, _)) => self.handle_connection(socket),
                Err(e) => {
                    eprintln!("Failed to accept connection: {}. Skipped!", e);
                    continue;
                }
            }
        }
    }

    fn handle_connection(&self, mut socket: tokio::net::TcpStream) {
        let routes = self.routes.clone();

        tokio::spawn(async move {
            let mut buf: Vec<u8> = vec![0; 1024];

            let n: usize = match socket.read(&mut buf).await {
                Ok(n) => n,
                Err(_) => {
                    let resp = Response::new("400 Bad Request").with_status(400, "Bad Request");
                    let _ = socket.write_all(resp.to_string().as_bytes()).await;
                    return;
                }
            };

            let request_raw = String::from_utf8_lossy(&buf[..n]);

            let request = match Request::from_raw(&request_raw) {
                Ok(request) => request,
                Err(_) => {
                    let response = Response::new("400 Bad Request").with_status(400, "Bad Request");
                    let _ = socket.write_all(response.to_string().as_bytes()).await;
                    return;
                }
            };
    
            let mut matched: bool = false;
            for route in &routes {
                if let Some(caps) = route.pattern.captures(&request.path) {

                    let mut params: HashMap<String, String> = HashMap::new();
                    for name in &route.param_names {
                        if let Some(m) = caps.name(name) {
                            params.insert(name.clone(), m.as_str().to_string());
                        }
                    }

                    let response: Response = (route.handler)(request, params);
                    let resp_text: String = response.to_string();
                    
                    socket.write_all(resp_text.as_bytes()).await.unwrap();
                    matched = true;
                    break;
                }
            }
    
            if !matched {
                let resp: Response = Response::new("404 Not Found");
                socket.write_all(resp.to_string().as_bytes()).await.unwrap();
            }
        });
    }
}
