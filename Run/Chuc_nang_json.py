import json

class AnimeItem:
    def __init__(self, Id_flight, Name_flight, Time_start, image, Time_stop):
        self.Id_flight = Id_flight
        self.Name_flight = Name_flight
        self.Time_start = Time_start
        self.image = image
        self.Time_stop = Time_stop
class AnimeDatabase:
    def __init__(self):
        self.anime_item_list = list()
        self.anime_dict_data = AnimeDatabase.__load_json_data()
        self.anime_title_list = self.get_title_list()

    def load_data(self):
        for anime_dict in self.anime_dict_data:
            anime = AnimeItem(Id_flight=anime_dict["Id_flight"],
                              Name_flight=anime_dict["Name_flight"],
                              Time_start=anime_dict["Time_start"],
                              image=anime_dict["image"],
                              Time_stop=anime_dict["Time_stop"])
            self.anime_item_list.append(anime)

    def get_title_list(self):
        titles = [anime["Name_flight"] for anime in self.anime_dict_data]
        return titles
    

    def add_item_from_dict(self, anime_dict):
        new_item = AnimeItem(Id_flight=anime_dict["Id_flight"],
                              Name_flight=anime_dict["Name_flight"],
                              Time_start=anime_dict["Time_start"],
                              image=anime_dict["image"],
                              Time_stop=anime_dict["Time_stop"])
        self.anime_item_list.append(new_item)
        self.anime_dict_data.append(anime_dict)
        AnimeDatabase.__write_json_data(self.anime_dict_data)

    def edit_item_from_dict(self, edit_title, anime_dict):
        anime_edit = self.get_item_by_title(edit_title)
        if anime_edit is not None:
            if "Name_flight" in anime_dict:
                anime_edit.Name_flight = anime_dict["Name_flight"]
            if "Time_start" in anime_dict:
                anime_edit.Time_start = anime_dict["Time_start"]
            if "image" in anime_dict:
                anime_edit.image = anime_dict["image"]
            if "Time_stop" in anime_dict:
                anime_edit.Time_stop = anime_dict["Time_stop"]

            self.anime_dict_data = self.item_to_data()
            AnimeDatabase.__write_json_data(self.anime_dict_data)

    def delete_item(self, delete_title):
        anime_delete = self.get_item_by_title(delete_title)
        self.anime_item_list.remove(anime_delete)
        self.anime_dict_data = self.item_to_data()
        AnimeDatabase.__write_json_data(self.anime_dict_data)
    
    def get_item_by_title(self, anime_title) -> AnimeItem:
        for anime_item in self.anime_item_list:
            if anime_item.Name_flight == anime_title:
                return anime_item

    def __write_json_data(json_data):
        with open(r"D:\BTL-Python\data_8.json", "w") as json_out:
            json.dump(json_data, json_out, indent=4)


    def __load_json_data():
        anime_dict_data = list()
        with open(r"D:\BTL-Python\data_8.json", "r", encoding="utf-8") as json_in:
            json_data = json.load(json_in)
        anime_dict_data.extend(json_data)
        return anime_dict_data

    def item_to_data(self):
        json_data = list()
        for anime in self.anime_item_list:
            json_data.append(anime.__dict__)
        return json_data