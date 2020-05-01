import json
import time
import requests
from pprint import pprint
import pandas as pd
TOKEN = '63bd9b357f079b30e4ea43a61b75cf79a83479878af900188b02bae5fec5177ee4d4e142b8e73d9312a34'
class User:
    def __init__(self, token):
        self.token = token
        # self.new_id = new_id

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.52'
        )

    def get_info(self, new_id):
        params = self.get_params()
        params['user_ids'] = new_id
        params['fields'] = 'id, first_name, last_name, city, interests, ' \
                           'movies, relation, sex, bdate'
        response = requests.get(
            'https://api.vk.com/method/users.get',
            params
        )
        return response.json()

    def top_photo(self, ids):
        params = self.get_params()
        result_list = []
        for id in ids:
            params['owner_id'] = id
            params['album_id'] = 'profile'
            params['extended'] = 1
            response = requests.get(
                'https://api.vk.com/method/photos.get',
                params
            )
            resp_json = response.json()
            list_top_photos = []
            urls_list = []
            try:
                for one in resp_json['response']['items']:
                    list_top_photos.append({'id': one['id'], 'likes': one['likes']['count']})
                df = pd.DataFrame(list_top_photos)
                list_top3 = df.sort_values(['likes'], ascending=False).head(3)['id'].values.tolist()
                for photo in list_top3:
                    photo = f'https://vk.com/id{id}?z=photo{id}_{photo}%2Falbum{id}_0%2Frev'
                    urls_list.append(photo)
                result_list.append({f'https://vk.com/id{id}': urls_list})
            except:
                pass
        with open('test.json', 'w', encoding='utf-8') as text:
            json.dump(result_list, text)
        return result_list

    def get_groups(self, new_id):
        params = self.get_params()
        params['user_id'] = new_id
        response = requests.get(
            'https://api.vk.com/method/groups.get',
            params
        )
        groups_id =response.json()['response']['items']
        return groups_id

    def get_friends(self, id):
        friends_list = []
        params = self.get_params()
        params['user_id'] = id
        # params['fields'] = 'sex, bdate, city'
        response = requests.get('https://api.vk.com/method/friends.get', params)
        resp_json = response.json()
        friends_list = resp_json['response']['items']
        return friends_list

    def find_common_groups(self, list_people):
        list_people_with_common_groups = []
        # list_groups = []
        for men in list_people:
            list_groups = []
            men_groups = self.get_groups(men)
            time.sleep(0.3)
            # print(men_groups)
            # print(my_groups)
            for group in men_groups:
                if group in my_groups:
                    # print(group)
                    list_groups.append(group)
                dict_gr = {men: list_groups}
            # print(dict_gr)
            list_people_with_common_groups.append([{'id': men}, {'group_count': len(list_groups)}])
            # print(list_people_with_common_groups)

        # print(list_people_with_common_groups)
        return list_people_with_common_groups

    def find_common_friends(self, list_people):
        list_common_friends = []
        code_list = []
        params = self.get_params()
        # params['fields'] = 'common_count'
        i = 0
        while i < len(list_people):
            for one in list_people[i:i + 24]:
                code_list.append('API.users.get({"user_id":"' + str(one) + '", "fields": "common_count"})')
            string_code = str(code_list).replace("'", "")
            code = f'return {string_code}'
            response = requests.get('https://api.vk.com/method/execute?code=' + code + ';', params)
            resp_json = response.json()
            for user in resp_json['response']:

                list_common_friends.append({'id': user[0]['id']}, {'count': user[0]['common_count']})
            code_list.clear()
            if i > (len(list_people) - 24):
                i = i + (len(list_people) - i)
            else:
                i = i + 24
        return list_common_friends
    
    def sorted_people(self, list_with_friends, list_with_groups):
        res_friends = []
        res_group = []
        for one in list_with_friends:
            # print(one[0]['count'])
            res_friends.append({'id': one[0]['id'], 'count': one[1]['count']})
        for one in list_with_groups:
            # print(one[0]['count'])
            res_group.append({'id': one[0]['id'], 'group_count': one[1]['group_count']})
        # print(res_group)
        df_1 = pd.DataFrame(res_group)
        df = pd.DataFrame(res_list)
        df_2 = pd.merge(df, df_1, how ='inner', on ='id')
        sorted_df = df_2.sort_values( by = ['count', 'group_count'], ascending=False)
        sorted_list = sorted_df['id'].values.tolist()
        return sorted_list

    def get_friens_of_friends(self, list, id):
        list_of_friends_of_friends = []
        code_list = []
        params = self.get_params()
        gender = self.get_info(id)['response'][0]['sex']
        city_id = self.get_info(id)['response'][0]['city']['id']
        bdate = int(self.get_info(id)['response'][0]['bdate'].split('.')[2])
        i = 0
        while i < len(list):
            for one in list[i:i+24]:
                code_list.append('API.friends.get({"user_id":"'+str(one)+'", "count": 50,'
                                    ' "order": "random","fields": "sex, bdate, city, relation"})')
            string_code = str(code_list).replace("'", "")
            code = f'return {string_code}'
            response = requests.get('https://api.vk.com/method/execute?code=' + code + ';', params)
            resp_json = response.json()
            try:
                for users in resp_json.values():
                    for user in users:
                        for one in user['items']:
                            if one['sex'] == gender or 'relation' not in one.keys():
                                continue
                            if one['relation'] not in [0, 1, 6] or 'city' not in one.keys():
                                continue
                            else:
                                if 'city' in one.keys() and one['city']['id'] == city_id:
                                    if 'bdate' in one.keys() and int(one['bdate'].split('.')[-1]) in range(bdate - 5, bdate + 5):
                                        # print(one)
                                        list_of_friends_of_friends.append(one['id'])
            except TypeError:
                pass
            except KeyError:
                pass
            code_list.clear()
            if i > (len(list) - 24):
                i = i + (len(list) - i)
            else:
                i = i + 24
            result = [x for n, x in enumerate(list_of_friends_of_friends) if x not in list_of_friends_of_friends[n + 1:]]
        return result


if __name__ == '__main__':
    user = User(TOKEN)
    information = user.get_info('soldatenkov121')
    user_id = information['response'][0]['id']
    friends = user.get_friends(user_id)
    my_groups = user.get_groups(user_id)
    list_well_poeple = user.get_friens_of_friends(friends, user_id)
    common_friends = user.find_common_friends(list_well_poeple)
    common_groups = user.find_common_groups(list_well_poeple)
    sorted_list = user.sorted_people(common_friends, common_groups)
    # print(common_friends)
    # print(common_groups)

