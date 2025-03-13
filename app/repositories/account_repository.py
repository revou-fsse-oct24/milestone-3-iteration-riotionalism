class AccountRepository:
    def __init__(self):
        self.accounts = {}
        self.current_id = 1

    def create(self, account_data):
        account_id = self.current_id
        account_data['id'] = account_id
        account_data['balance'] = account_data.get('balance', 0)
        self.accounts[account_id] = account_data
        self.current_id += 1
        return account_data

    def get_all(self):
        return list(self.accounts.values())

    def get_by_id(self, account_id):
        return self.accounts.get(account_id)

    def update(self, account_id, account_data):
        if account_id in self.accounts:
            self.accounts[account_id].update(account_data)
            return self.accounts[account_id]
        return None

    def delete(self, account_id):
        if account_id in self.accounts:
            del self.accounts[account_id]
            return True
        return False
