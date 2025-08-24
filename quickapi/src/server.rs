use std::collections::HashMap;
use std::sync::Arc;

use regex::Regex;

use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

use crate::request::Request;
use crate::response::Response;


#[derive(Clone, Debug, PartialEq, Eq)]
pub enum HttpMethod {
    GET,
    POST,
    PUT,
    DELETE,
    PATCH,
    OPTIONS,
    HEAD,
    Other(String),
}

impl HttpMethod {
    pub fn from_str(s: &str) -> Self {
        match s.to_uppercase().as_str() {
            "GET" => HttpMethod::GET,
            "POST" => HttpMethod::POST,
            "PUT" => HttpMethod::PUT,
            "DELETE" => HttpMethod::DELETE,
            "PATCH" => HttpMethod::PATCH,
            "OPTIONS" => HttpMethod::OPTIONS,
            "HEAD" => HttpMethod::HEAD,
            other => HttpMethod::Other(other.to_string()),
        }
    }
}

pub struct Route {
    pub method: HttpMethod,
    pub pattern: Regex,
    pub param_names: Vec<String>,
    pub handler: Arc<dyn Fn(Request, HashMap<String, String>) -> Response + Send + Sync>,
}

impl Clone for Route {
    fn clone(&self) -> Self {
        Self {
            method: self.method.clone(),
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

    pub fn route<F>(&mut self, method: &str, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        let method = HttpMethod::from_str(method);
        // Convert path like /users/{id} -> regex
        let mut param_names = Vec::new();
        let mut regex_str = regex::escape(path)
            .replace(r"\{", "{")
            .replace(r"\}", "}")
            .replace("{", "(?P<")
            .replace("}", ">[^/]+)")
            .replace(r"\?", "?"); // allow query params

        // Always allow optional trailing slash, regardless of original path
        if regex_str.ends_with('/') {
            // If path ends with '/', make it optional
            regex_str = format!("{}?", &regex_str);
        } else {
            // If not, allow an optional trailing slash
            regex_str = format!("{}/?", &regex_str);
        }

        let regex = Regex::new(&format!("^{}$", regex_str)).unwrap();

        for cap in Regex::new(r"\(\?P<([^>]+)>[^)]+\)").unwrap().captures_iter(&regex_str) {
            param_names.push(cap[1].to_string());
        }

        let route = Route {
            method,
            pattern: regex,
            param_names,
            handler: Arc::new(handler),
        };
        self.routes.push(route);
    }

    pub fn get<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("GET", path, handler);
    }

    pub fn post<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("POST", path, handler);
    }

    pub fn put<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("PUT", path, handler);
    }

    pub fn delete<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("DELETE", path, handler);
    }

    pub fn patch<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("PATCH", path, handler);
    }

    pub fn options<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("OPTIONS", path, handler);
    }

    pub fn head<F>(&mut self, path: &str, handler: F)
    where
        F: Fn(Request, HashMap<String, String>) -> Response + Send + Sync + 'static,
    {
        self.route("HEAD", path, handler);
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
                    let resp = Response::bad_request().build();
                    let _ = socket.write_all(resp.to_string().as_bytes()).await;
                    return;
                }
            };

            let request_raw = String::from_utf8_lossy(&buf[..n]);

            let req = match Request::from_raw(&request_raw) {
                Ok(req) => req,
                Err(_) => {
                    let resp = Response::bad_request().build();
                    let _ = socket.write_all(resp.to_string().as_bytes()).await;
                    return;
                }
            };

            let mut matched: bool = false;
            for route in &routes {
                if route.method == HttpMethod::from_str(&req.method)
                    && route.pattern.captures(&req.path).is_some() {
                    let caps = route.pattern.captures(&req.path).unwrap();
                    let mut params: HashMap<String, String> = HashMap::new();
                    for name in &route.param_names {
                        if let Some(m) = caps.name(name) {
                            params.insert(name.clone(), m.as_str().to_string());
                        }
                    }

                    let response: Response = (route.handler)(req, params);
                    let resp_text: String = response.to_string();
                    socket.write_all(resp_text.as_bytes()).await.unwrap();
                    matched = true;
                    break;
                }
            }

            if !matched {
                let resp: Response = Response::not_found().build();
                socket.write_all(resp.to_string().as_bytes()).await.unwrap();
            }
        });
    }
}
