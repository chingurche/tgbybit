import config
from aiogram.types import Message
from exceptions import UserIsNotFound, TagConnectionNotFound, NoUsersWithTagError
from repositories import UserRepository, TagsRepository, UserTagsRepository
from personal_data import PersonalData

user_repository = UserRepository(config.DB_PATH)
tags_repository = TagsRepository(config.DB_PATH)
user_tags_repository = UserTagsRepository(config.DB_PATH)

class UserData:
    def __init__(self, user_id):
        user = user_repository.get_user(user_id)

        if user is None: raise UserIsNotFound

        _, username, student_group = user
        self.id = user_id
        self.personal_data = PersonalData(username, student_group)
        self.tags = user_tags_repository.get_tags_of_user(user_id)

    @staticmethod
    def get_random(my_id):
        return UserData(user_repository.get_random_user_id(my_id))
    
    @staticmethod
    def get_popular_tags():
        tags = user_tags_repository.get_top_tags()
        output = ""
        for i in range(len(tags)):
            output += f"{i+1}. {tags[i][0]} - {tags[i][1]}\n"
        return output
    
    @staticmethod
    def update_personal_data(user_id, data : PersonalData) -> None:
        user_repository.add_or_update_user(user_id, data)

    def get_list_of_users_by_tag(self, tag_name):
        tag_id = tags_repository.get_tag_id(tag_name)
        found_users = user_tags_repository.get_users_by_tag(tag_id)

        list_of_user = []
        for found_user in found_users:
            found_user_id = found_user[0]
            if self.id == found_user_id: continue
            list_of_user.append(found_user_id)
            
        if len(list_of_user) == 0: raise NoUsersWithTagError
        return list_of_user

    def add_new_tag(self, new_tag : str) -> None:
        tags_repository.add_new_tag(new_tag)
        
        tag_id = tags_repository.get_tag_id(new_tag)
        user_tags_repository.add_tag_to_user(self.id, tag_id)
    
    
    def remove_tag(self, removed_tag : str) -> None:
        tag_id = tags_repository.get_tag_id(removed_tag)
        is_removed = user_tags_repository.remove_tag_from_user(self.id, tag_id)
        if not is_removed: raise TagConnectionNotFound

    def get_string_tags(self) -> str:
        tags = self.tags
        if len(tags) == 0: return "У вас не добавлено ни одного исполнителя."

        output = "Исполнители: "
        for tag in tags:
            output += tag[0] + ", "
        return output[:-2]