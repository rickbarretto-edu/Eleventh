use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

use tokio::fs;
use uuid::Uuid;

use super::models::{Account, Accounts};

fn db_path() -> PathBuf {
    PathBuf::from(concat!(env!("CARGO_MANIFEST_DIR"), "/data/accounts.json"))
}

pub async fn load_accounts() -> Result<Accounts, String> {
    let path = db_path();

    if !path.exists() {
        return Ok(Accounts::new());
    }

    let s = fs::read_to_string(&path)
        .await
        .map_err(|e| format!("failed to read DB file: {}", e))?;
    let map: Accounts =
        serde_json::from_str(&s).map_err(|e| format!("invalid DB JSON: {}", e))?;
    Ok(map)
}

pub async fn save_accounts(accounts: &Accounts) -> Result<(), String> {
    let path = db_path();
    let serialized = serde_json::to_string_pretty(accounts)
        .map_err(|e| format!("serialize error: {}", e))?;
    fs::write(&path, serialized)
        .await
        .map_err(|e| format!("failed to write DB file: {}", e))
}

pub fn new_account(username: String, password: String) -> Account {
    let created_at = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs().to_string())
        .unwrap_or_else(|_| "0".to_string());

    let auth = Uuid::new_v4().to_string();
    Account {
        username,
        password,
        created_at,
        auth,
    }
}
