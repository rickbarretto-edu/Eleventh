use std::time::{Duration, Instant};

use crate::services::server_url;


fn ping_url() -> String {
    format!("http://{}/ping", server_url())
}

pub fn ping(timeout: usize) -> Result<Duration, String> {
    let url = ping_url();    
    let client = reqwest::blocking::Client::builder()
        .timeout(Duration::from_secs(timeout as u64))
        .build()
        .map_err(|_| "Failed to build client")?;

    let start = Instant::now();
    let result = client.get(&url).send();
    let elapsed = start.elapsed();

    match result {
        Ok(_) => Ok(elapsed),
        Err(e) => {
            if e.is_timeout() {
                Err(format!("Timed out, took more than {}s", timeout))
            } else {
                Err("Failed to send request".to_string())
            }
        }
    }

}