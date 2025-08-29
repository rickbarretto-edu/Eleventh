use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct Account {
    pub username: String,
    pub password: String,
    pub created_at: String,
    pub auth: String,
}

pub type Accounts = std::collections::HashMap<String, Account>;
