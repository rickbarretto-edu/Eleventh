use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

use super::models::Account;

/// Wrapper around Accounts to avoid Arc::clone boilerplate
pub struct SharedAccounts(Arc<Mutex<VirtualAccounts>>);

#[derive(Clone, Debug)]
pub struct VirtualAccounts {
    map: HashMap<String, Account>,
}

impl VirtualAccounts {
    pub fn new() -> Self {
        VirtualAccounts {
            map: HashMap::new(),
        }
    }

    pub fn shared(self) -> SharedAccounts {
        SharedAccounts::new(self)
    }

    fn store_inner(&mut self, new_account: Account) -> Result<(), String> {
        if self.map.contains_key(&new_account.username) {
            return Err("Account already exists".into());
        }
        self.map.insert(new_account.username.clone(), new_account);
        Ok(())
    }

    fn by_credentials_inner(&self, username: &str, password: &str) -> Option<&Account> {
        self.map
            .get(username)
            .filter(|acc| acc.password == password)
    }
}

impl SharedAccounts {
    pub fn new(repo: VirtualAccounts) -> Self {
        SharedAccounts(Arc::new(Mutex::new(repo)))
    }

    pub async fn store(&self, new_account: Account) -> Result<(), String> {
        let mut repo = self.0.lock().await;
        repo.store_inner(new_account)
    }

    pub async fn by_credentials(&self, username: &str, password: &str) -> Option<Account> {
        let repo = self.0.lock().await;
        repo.by_credentials_inner(username, password).cloned()
    }
}

impl Clone for SharedAccounts {
    fn clone(&self) -> Self {
        SharedAccounts(self.0.clone())
    }
}
