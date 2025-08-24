use std::collections::HashMap;
use url::Url;

#[derive(Debug, Clone)]
pub struct Request {
    pub method: String,
    pub path: String,
    pub query: HashMap<String, String>,
    pub body: String,
}

impl Request {
    pub fn from_raw(raw: &str) -> Self {
        let lines: Vec<&str> = raw.lines().collect();

        let (method, full_path) = Self::parse_request_line(lines.get(0));
        let (path, query) = Self::parse_url(&full_path);
        let body = Self::parse_body(&lines);

        Request { method, path, query, body }
    }

    fn parse_request_line(line: Option<&&str>) -> (String, String) {
        let mut parts = line.unwrap_or(&"").split_whitespace();
        let method: String = parts.next().unwrap_or("").to_string();
        let full_path: String = parts.next().unwrap_or("/").to_string();

        (method, full_path)
    }

    fn parse_url(full_path: &str) -> (String, HashMap<String, String>) {
        let url = Url::parse(&format!("http://localhost{}", full_path)).unwrap();
        let path = url.path().to_string();

        let query = url
            .query_pairs()
            .map(|(k, v)| (k.to_string(), v.to_string()))
            .collect::<HashMap<_, _>>();

        (path, query)
    }

    fn parse_body(lines: &[&str]) -> String {
        lines.last().unwrap_or(&"").to_string()
    }

    pub fn param(&self, key: &str) -> Option<&String> {
        self.query.get(key)
    }
}
