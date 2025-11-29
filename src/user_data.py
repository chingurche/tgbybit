import config
from exceptions import UserIsNotFound, TagConnectionNotFound, NoUsersWithTagError
from repositories import UserRepository, TagsRepository, UserTagsRepository, ConnectionsRepository

user_repository = UserRepository(config.DB_PATH)
tags_repository = TagsRepository(config.DB_PATH)
user_tags_repository = UserTagsRepository(config.DB_PATH)
connection_repository = ConnectionsRepository(config.DB_PATH)
    
class PersonalData:
    def __init__(self, name, student_group):
        self.name = name
        self.student_group = student_group

class TagList:
    def __init__(self, user_id):
        self.tags = user_tags_repository.get_tags_of_user(user_id)
    
    @staticmethod
    def get_popular() -> str:
        tags = user_tags_repository.get_top_tags()
        output = ""
        for i in range(len(tags)):
            output += f"{i+1}. <code>{tags[i][0]}</code> — <b>{tags[i][1]}</b>\n"
        return output
    
    def get_as_merged_with(self, other) -> str:
        output = "Исполнители: "
        counter = 0
        for tag in self.tags:
            if tag in other:
                output += f"🔥<code>{tag[0]}</code>, "
                counter += 1
            else:
                output += f"<code>{tag[0]}</code>, "
        output = output[:-2] + f"\nОбщих исполнителей: <b>{counter}</b>"
        return output

    
    def get_as_mine(self) -> str:
        if len(self.tags) == 0: return "У вас не добавлено ни одного исполнителя\."

        output = "Исполнители: "
        for tag in self.tags:
            output += f"<code>{tag[0]}</code>, "
        return output[:-2]

class UserData:
    def __init__(self, user_id):
        user = user_repository.get_user(user_id)

        if user is None: raise UserIsNotFound

        _, username, student_group = user
        self.id = user_id
        self.personal_data = PersonalData(username, student_group)
        self.tag_list = TagList(user_id)

    @staticmethod
    def get_random(my_id):
        return UserData(user_repository.get_random_user_id(my_id))
    
    @staticmethod
    def update_personal_data(user_id, data : PersonalData) -> None:
        user_repository.add_or_update_user(user_id, data)

    def display_as_me(self) -> str:
        #username = f"[ты](tg://user?id={self.id})"
        display = f"Твой профиль: \n\n" \
            f"{self.personal_data.name}, {self.personal_data.student_group}\n" \
            f"{self.tag_list.get_as_mine()}"
        return display

    def display_compared_with(self, other, anonymous: bool = True) -> str:
        display = f"{self.tag_list.get_as_merged_with(other.tag_list.tags)}"
    
        if anonymous:
            display = f"<b>анонимный слушатель</b>\n" + display
        else:
            username = f"[написать](tg://user?id={self.id})"
            display = f"{self.personal_data.name}, {self.personal_data.student_group} — {username}\n" + display
        return display
    
    def send_request_from(self, other_id):
        connection_repository.create_request(other_id, self.id)

    def get_list_of_connects(self):
        return connection_repository.get_pending_for_user(self.id)


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
