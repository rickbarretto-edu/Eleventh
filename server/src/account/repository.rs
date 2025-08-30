use std::collections::HashMap;
use std::sync::Arc;


use super::models::Account;


/// Wrapper around Accounts to avoid Arc::clone boilerplate
pub struct SharedAccounts(Arc<VirtualAccounts>);

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

    pub fn shared(self) -> SharedAccounts where Self: Sized {
        SharedAccounts::new(self)
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

impl SharedAccounts {
    pub fn new(repo: VirtualAccounts) -> Self {
        SharedAccounts(Arc::new(repo))
    }
}

impl std::ops::Deref for SharedAccounts {
    type Target = VirtualAccounts;

    fn deref(&self) -> &Self::Target {
        &self.0
    }
}


impl Clone for SharedAccounts {
    fn clone(&self) -> Self {
        SharedAccounts(self.0.clone())
    }
}


