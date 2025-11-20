from aiogram.types import Message
from exceptions import UserIsNotFound
from repositories import UserRepository, TagsRepository, UserTagsRepository
from personal_data import PersonalData

DB_PATH = "users.db"
user_repository = UserRepository(DB_PATH)
tags_repository = TagsRepository(DB_PATH)
user_tags_repository = UserTagsRepository(DB_PATH)


class UserData:
    def __init__(self, user_id):
        user = user_repository.get_user(user_id)

        if user is None: raise UserIsNotFound

        _, username, student_group = user
        self.personal_data = PersonalData(username, student_group)
        self.tags = user_tags_repository.get_tags_of_user(user_id)

    @staticmethod
    def get_random(my_id):
        return UserData(user_repository.get_random_user_id(my_id))
    
    @staticmethod
    def update_personal_data(user_id, data : PersonalData):
        user_repository.add_or_update_user(user_id, data)

    def get_string_tags(self):
        tags = self.tags
        if len(tags) == 0: return "У вас не добавлено ни одного исполнителя."

        output = "Исполнители: "
        for tag in tags:
            output += tag + ", "
        return output[:-2]