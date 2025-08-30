use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::Arc;

use tokio::fs;

use super::models::Account;

pub trait Accounts {
    async fn store(&self, new_account: Account) -> Result<(), String>;
    async fn by_credentials(&self, username: &str, password: &str) -> Option<&Account>;
    
    fn shared(self) -> SharedAccounts<Self> where Self: Sized {
        SharedAccounts::new(self)
    }

}

/// Wrapper around Accounts to avoid Arc::clone boilerplate
pub struct SharedAccounts<T: Accounts>(Arc<T>);

#[derive(Clone, Debug)]
pub struct VirtualAccounts {
    map: HashMap<String, Account>,
}

pub struct PersistentAccounts {
    path: PathBuf,
    repo: VirtualAccounts,
}


impl VirtualAccounts {

    pub fn new() -> Self {
        VirtualAccounts {
            map: HashMap::new(),
        }
    }
}

impl Accounts for VirtualAccounts {

    async fn store(&self, new_account: Account) -> Result<(), String> {
        if self.map.contains_key(&new_account.username) {
            return Err("Account already exists".into());
        }
        Ok(())
    }

    async fn by_credentials(&self, username: &str, password: &str) -> Option<&Account> {
        self.map.get(username).filter(|acc| acc.password == password)
    }

}


impl PersistentAccounts {

    pub fn new(path: &str) -> Self {
        let path: PathBuf = dbg!(Self::normalized_path(&path));

        Self {
            repo: VirtualAccounts { map: Self::load_all(&path) },
            path: path,
        }
    }

    pub fn normalized_path(path: &str) -> PathBuf {
        let manifest: PathBuf = env!("CARGO_MANIFEST_DIR").into();

        let binding = PathBuf::from(path);
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

impl Accounts for PersistentAccounts {

    async fn store(&self, new_account: Account) -> Result<(), String> {
        self.repo.store(new_account).await?;
        self.save_all().await
    }

    async fn by_credentials(&self, username: &str, password: &str) -> Option<&Account> {
        self.repo.by_credentials(username, password).await
    }

}


impl Clone for SharedAccounts<VirtualAccounts> {
    fn clone(&self) -> Self {
        SharedAccounts(self.0.clone())
    }
}

impl Clone for SharedAccounts<PersistentAccounts> {
    fn clone(&self) -> Self {
        SharedAccounts(self.0.clone())
    }
}

impl <T: Accounts> SharedAccounts<T> {
    pub fn new(repo: T) -> Self {
        SharedAccounts(Arc::new(repo))
    }
}

impl<T: Accounts> std::ops::Deref for SharedAccounts<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}


