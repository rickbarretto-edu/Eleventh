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
        let listener = TcpListener::bind(addr).await.unwrap();
        println!("Listening on {}", addr);

        loop {
            let (mut socket, _) = listener.accept().await.unwrap();
            let routes = self.routes.clone();

            tokio::spawn(async move {
                let mut buf = vec![0; 1024];
                let n = socket.read(&mut buf).await.unwrap();
                let req_text = String::from_utf8_lossy(&buf[..n]);

                let req = Request::from_raw(&req_text);

                let mut matched = false;
                for route in &routes {
                    if let Some(caps) = route.pattern.captures(&req.path) {
                        let mut params = HashMap::new();
                        for name in &route.param_names {
                            if let Some(m) = caps.name(name) {
                                params.insert(name.clone(), m.as_str().to_string());
                            }
                        }
                        let response = (route.handler)(req, params);
                        let resp_text = response.to_string();
                        socket.write_all(resp_text.as_bytes()).await.unwrap();
                        matched = true;
                        break;
                    }
                }

                if !matched {
                    let resp = Response::new("404 Not Found");
                    socket.write_all(resp.to_string().as_bytes()).await.unwrap();
                }
            });
        }
    }
}
