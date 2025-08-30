use std::collections::HashMap;
use std::path::PathBuf;

use tokio::fs;

use super::models::Account;

#[derive(Clone, Debug)]
pub struct Accounts {
    map: HashMap<String, Account>,
}

impl Accounts {

    pub fn new() -> Self {
        Accounts {
            map: HashMap::new(),
        }
    }

    pub fn at(path: String) -> PersistentJson {
        PersistentJson::at(path)
    }

    pub async fn store(&self, new_account: Account) -> Result<(), String> {
        if self.map.contains_key(&new_account.username) {
            return Err("Account already exists".into());
        }
        Ok(())
    }

    pub async fn by_credentials(&self, username: &str, password: &str) -> Option<&Account> {
        self.map.get(username).filter(|acc| acc.password == password)
    }
}


struct PersistentJson {
    path: PathBuf,
    repo: Accounts,
}

impl PersistentJson {

    pub fn at(path: String) -> Self {
        let path: PathBuf = Self::normalized_path(&path);

        Self {
            repo: Accounts { map: Self::load_all(&path) },
            path: path,
        }
    }

    pub async fn store(&self, new_account: Account) -> Result<(), String> {
        self.repo.store(new_account).await?;
        self.save_all().await
    }

    pub async fn by_credentials(&self, username: &str, password: &str) -> Option<&Account> {
        self.repo.by_credentials(username, password).await
    }

    pub fn normalized_path(path: &str) -> PathBuf {
        let manifest: PathBuf = env!("CARGO_MANIFEST_DIR").into();

        let binding = PathBuf::from(path.clone());
        let relative = binding
            .to_str()
            .unwrap_or("/data/accounts.json")
            .trim_start_matches('/');

        manifest.join(relative)
    }

    fn load_all(path: &PathBuf) -> HashMap<String, Account> {
        let content = std::fs::read_to_string(path)
            .map_err(|e| format!("failed to read DB file: {}", e))
            .unwrap();
        
        serde_json::from_str(&content)
            .map_err(|e| format!("invalid DB JSON: {}", e))
            .unwrap()
    }

    async fn save_all(&self) -> Result<(), String> {
        let content = serde_json::to_string_pretty(&self.repo.map)
            .map_err(|e| format!("failed to serialize accounts: {}", e))?;

        fs::write(self.path.clone(), content)
            .await
            .map_err(|e| format!("failed to write DB file: {}", e))?;

        Ok(())
    }

}


