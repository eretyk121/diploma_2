import json
import time
import requests
from pprint import pprint
import pandas as pd
import pickle
ID = 'soldatenkov121'
# TOKEN = '63bd9b357f079b30e4ea43a61b75cf79a83479878af900188b02bae5fec5177ee4d4e142b8e73d9312a34'
TOKEN = 'ea12a1489c617cba5cb105900782a1d9964f29d237fd0a543d3e66f293bb031b7672ea3a8267aad8489e6'
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

    # def find_friends_of_friends(self, id):
    #     friends_list = []
    #     friends_of_friends = []
    #     gender = self.get_info(id)['response'][0]['sex']
    #     city = self.get_info(id)['response'][0]['city']['id']
    #     bdate = int(self.get_info(id)['response'][0]['bdate'].split('.')[2])
    #     params = self.get_params()
    #     params['user_id'] = id
    #     # params['fields'] = 'sex, bdate, city'
    #     response = requests.get('https://api.vk.com/method/friends.get', params)
    #     resp_json = response.json()
    #     friends_list = resp_json['response']['items']
    #     # try:
    #     for friend in friends_list:
    #         params['user_id'] = friend
    #         params['fields'] = 'sex, bdate, city'
    #         params['order'] = 'hints'
    #         params['count'] = 50
    #         response_2 = requests.get('https://api.vk.com/method/friends.get', params)
    #         resp_json_2 = response_2.json()
    #         # friends_of_friends.append(resp_json_2)
    #         try:
    #             for one in resp_json_2['response']['items']:
    #                 if one['sex'] != gender:
    #                     try:
    #                         if int(one['bdate'].split('.')[-1]) in range(bdate - 3, bdate + 3):
    #                             friends_of_friends.append(one['id'])
    #                     except KeyError:
    #                         pass
    #                     # if one['city']['id'] == city:
    #                     #     friends_of_friends.append(one['id'])
    #         except:
    #             pass
    #     # except:
    #     #     pass
    #     # print(len(friends_list))
    #     return friends_of_friends

    def get_friends(self, id):
        friends_list = []
        params = self.get_params()
        params['user_id'] = id
        # params['fields'] = 'sex, bdate, city'
        response = requests.get('https://api.vk.com/method/friends.get', params)
        resp_json = response.json()
        print(resp_json)
        # friends_list = resp_json['response']['items']
        # return friends_list

    # def search_peolple(self, info):
    #     params = self.get_params()
    #     params['count'] = 500
    #     params['fields'] = 'id, first_name, last_name, interests, ' \
    #                        'movies, music, books, relation, sex, bdate'
    #     if info['sex'] == 2:
    #         params['sex'] = 1
    #     elif info['sex'] == 1:
    #         params['sex'] = 2
    #     elif info['sex'] == 0:
    #         print('Поиск невозможен, пол не выбран')
    #     params['status'] = 1,6
    #     params['city'] = info['city']
    #     response = requests.get('https://api.vk.com/method/users.search', params)
    #     resp_json = response.json()
    #     return resp_json
    # def find_for_age(self, dict_people, bdate):
    #     list_id = []
    #     for one in dict_people['response']['items']:
    #         try:
    #             if int(one['bdate'].split('.')[-1]) in range(bdate - 3, bdate + 3):
    #                 list_id.append(one['id'])
    #         except KeyError:
    #             pass
    #     return list_id

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

    # def find_common_friends(self, list_people):
    #     list_common_friends = []
    #     params = self.get_params()
    #     params['fields'] = 'common_count'
    #     for men in list_people:
    #         params['user_id'] = men
    #         time.sleep(0.3)
    #         response = requests.get(
    #             'https://api.vk.com/method/users.get',
    #             params
    #         )
    #         resp_json = response.json()
    #         # print(resp_json)
    #         list_common_friends.append({resp_json['response'][0]['id']: resp_json['response'][0]['common_count']})
    #     print(list_common_friends)
            # print(my_groups)
        #     for group in men_groups:
        #         if group in my_groups:
        #             # print(group)
        #             list_groups.append(group)
        #         dict_gr = {men: list_groups}
        #     # print(dict_gr)
        #     list_common_friends.append({men: len(list_groups)})
        #     # print(list_people_with_common_groups)
        #
        # # print(list_people_with_common_groups)
        # return list_common_friends

    # def get_people_groups(self, list):
    #     groups_list = []
    #     params = self.get_params()
    #     for one in list:
    #         params['user_id'] = one
    #         response = requests.get(
    #             'https://api.vk.com/method/groups.get',
    #             params
    #         )
    #         time.sleep(0.3)
    #         groups = {one: response.json()['response']['items']}
    #         # print(groups)
    #         groups_list.append(groups)
    #     return groups_list

    # def get_people_groups(self, list):
    #     groups_list = []
    #     code_list = []
    #     params = self.get_params()
    #     i = 0
    #     while i < len(list):
    #         for one in list[i:i + 5]:
    #             code_list.append('API.groups.get({"user_id":"' + str(one) + '"})')
    #         string_code = str(code_list).replace("'", "")
    #         code = f'return {string_code}'
    #         response = requests.get('https://api.vk.com/method/execute?code=' + code + ';', params)
    #         resp_json = response.json()
    #         for users in resp_json.values():
    #             for user in users:
    #                 print({one: user['items']})
    #         code_list.clear()
    #         if i > (len(list) - 5):
    #             i = i + (len(list) - i)
    #         else:
    #             i = i + 5
        # return groups_list

    # def get_friends_people(self, list_of_people, user):
    #     list_common_friends = []
    #     params = self.get_params()
    #     for one in list_of_people:
    #         params['source_uid'] = user
    #         params['target_uid'] = one
    #         # for one in list_of_people:
    #         #     params['user_id'] = one
    #         #     # print(one)
    #         response = requests.get('https://api.vk.com/method/friends.getMutual', params)
    #         # time.sleep(1)
    #         resp_json = response.json()
    #         try:
    #             accept = resp_json['response']
    #             if accept:
    #                 list_common_friends.append({one: accept})
    #         except:
    #             pass
    #     return list_common_friends

    # def get_group_info(self):
    #     params = self.get_params()
    #     final_list = []
    #     for id_group in id_groups_without_friends:
    #         print(f'Формирую информацию о группе {id_group}')
    #         params['group_id'] = id_group
    #         params['fields'] = 'members_count'
    #         time.sleep(1)
    #         response = requests.get(
    #             'https://api.vk.com/method/groups.getById',
    #             params
    #         )
    #         group_info = response.json()
    #         time.sleep(1)
    #         final_dic = {'group_id': group_info['response'][0]['id'],
    #                     'group_name': group_info['response'][0]['name'],
    #                     'count': group_info['response'][0]['members_count']}
    #         final_list.append(final_dic)
    #     return final_list

    # def get_members(self):
    #     params = self.get_params()
    #     params['filter'] = 'friends'
    #     group_list = []
    #     for id in groups_id:
    #         print(f'Проверяю группу {id} на отсутствие друзей')
    #         params['group_id'] = id
    #         response = requests.get(
    #             'https://api.vk.com/method/groups.getMembers',
    #             params
    #         )
    #         all_groups = response.json()
    #         if all_groups['response']['count'] == 0:
    #             group_list.append(id)
    #     return group_list

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
    # print(information)
    # search_info = {'sex': information['response'][0]['sex'],
    #                'city': information['response'][0]['city']['id']
    #                # 'bdate': 2020 - int(information['response'][0]['bdate'].split('.')[2])
    #                }

    user_id = information['response'][0]['id']
    # print(user_id)
    friends = user.get_friends(user_id)
    my_groups = user.get_groups(user_id)
    print(friends)
    # list_well_poeple = user.get_friens_of_friends(friends, user_id)
    # print(len(list_well_poeple))
    # common_friends = user.find_common_friends([48910099, 208456363, 18098504])
    # common_friends = user.find_common_friends(list_well_poeple)
    # pprint(common_friends)
    # common_groups = user.find_common_groups(list_well_poeple)
    # print(common_friends)
    # print(common_groups)

    # groups_people = user.get_people_groups(list_well_poeple)
    # print(groups_people)




    # print(len(list_men_groups))      # поиск общих групп
    # for one in list_men_groups:
    #     dict_test = {}
    #     list_groups = []
    #     for group in one:
    #         if group in my_groups:
    #             list_groups.append(group)
    #     print(list_groups)
    #     dict_test[one] = list_groups
    #     list_people_with_common_groups.append(dict_test)
    # print(list_people_with_common_groups)
    #
