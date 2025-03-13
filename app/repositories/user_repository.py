class UserRepository:
    def __init__(self):
        self.users = {}
        self.current_id = 1

    def create(self, user_data):
        user_id = self.current_id
        user_data['id'] = user_id
        self.users[user_id] = user_data
        self.current_id += 1
        return user_data

    def get_by_id(self, user_id):
        return self.users.get(user_id)

    def update(self, user_id, user_data):
        if user_id in self.users:
            self.users[user_id].update(user_data)
            return self.users[user_id]
        return None
