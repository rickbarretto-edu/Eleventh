use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Instant;
use tokio::task;
use tokio::time::Duration;

#[tokio::main]
async fn main() {
    let url = "http://127.0.0.1:8080/match/1/start/";
    let total_requests = 80_000;
    let concurrency = 10_000;

    let accepted = Arc::new(AtomicUsize::new(0));
    let rejected = Arc::new(AtomicUsize::new(0));
    let max_concurrent = Arc::new(AtomicUsize::new(0));
    let current_concurrent = Arc::new(AtomicUsize::new(0));

    let start = Instant::now();

    let mut handles = Vec::new();
    for _ in 0..total_requests {
        let url = url.to_string();
        let accepted = Arc::clone(&accepted);
        let rejected = Arc::clone(&rejected);
        let max_concurrent = Arc::clone(&max_concurrent);
        let current_concurrent = Arc::clone(&current_concurrent);

        while current_concurrent.load(Ordering::SeqCst) >= concurrency {
            tokio::time::sleep(Duration::from_millis(10)).await;
        }

        current_concurrent.fetch_add(1, Ordering::SeqCst);
        let handle = task::spawn(async move {
            let curr = current_concurrent.load(Ordering::SeqCst);
            max_concurrent.fetch_max(curr, Ordering::SeqCst);

            let client = reqwest::Client::new();
            let res = client.post(&url).send().await;

            match res {
                Ok(resp) if resp.status().is_success() => {
                    accepted.fetch_add(1, Ordering::SeqCst);
                }
                _ => {
                    rejected.fetch_add(1, Ordering::SeqCst);
                }
            }

            current_concurrent.fetch_sub(1, Ordering::SeqCst);
        });
        handles.push(handle);
    }

    for handle in handles {
        let _ = handle.await;
    }

    let duration = start.elapsed().as_secs_f64();
    let total = accepted.load(Ordering::SeqCst) + rejected.load(Ordering::SeqCst);
    let throughput = total as f64 / duration;

    println!("Accepted: {}", accepted.load(Ordering::SeqCst));
    println!("Rejected: {}", rejected.load(Ordering::SeqCst));
    println!("Max concurrency achieved: {}", max_concurrent.load(Ordering::SeqCst));
    println!("Total requests: {}", total);
    println!("Time taken: {:.2} s", duration);
    println!("Throughput: {:.2} req/s", throughput);
}
