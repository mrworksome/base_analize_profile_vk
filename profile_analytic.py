
import json


class BaseAnalytic:
    def __init__(self, file_name: str):
        with open(file_name) as f:
            self.data = json.load(f)
        self.static_attr = ['sex', 'city', 'country', 'graduation', 'hometown', 'university_name',
                         'education_form', 'education_status', 'relation']
        self.list_atr_parse = ['interests', 'activities', 'movies', 'tv', 'games', 'books', 'about']
        self.stop_words = [
            'кредит', 'онлайн', 'заявка', 'банк', 'история', 'истории',
            'кредит', 'онлайн', 'заявка', 'займов', 'карту', 'карта', 'займ',
            'рассрочка', 'потребительский', 'сбербанк', 'срочно', 'бесплатно',
            'взять', 'займы', 'хоум', 'связной', 'брокер', 'залог', 'ссуда',
            'автокредит', 'получение'
        ]

    def get_parse_data(self) -> dict:
        """
        Parse attributes in json file and sort by most popular words or key
        :return:
        """
        attributes = {}
        for person in self.data:
            for key, value in person.items():
                params = {
                    'key': key,
                    'value': value,
                    'attr': attributes
                }
                if key in self.static_attr:
                    self._static_condition(**params)
                elif key in self.list_atr_parse:
                    self._list_parse_condition(**params)
                elif key == 'bdate':
                    self._bdate_condition(**params)
                elif key == 'occupation':
                    self._occupation_condition(**params)
                elif key == 'personal':
                    self._personal_condition(**params)
                elif key == 'career':
                    self._career_condition(**params)
                elif key == 'schools':
                    self._schools_condition(**params)

        return attributes

    @staticmethod
    def _static_condition(key: str, value, attr: dict, ):
        if key not in attr:
            attr.update({key: {}})

        if isinstance(value, dict):
            value = value.get('title')
        try:
            attr.get(key).update({value: attr.get(key).get(value) + 1}) if value in attr.get(key) else attr.get(key).update({value: 1})
        except:
            pass

    def _list_parse_condition(self, key: str, value, attr: dict,):
        if key not in attr:
            attr.update({key: {}})

        words = value.replace('/', ' ').replace('^', ' ').replace('─', ' ').replace('#', ' ') \
            .replace('@', ' ').replace('█', ' ').replace('*', ' ').replace(':', ' '). \
            replace('$', ' ').replace('_', ' ').replace(';', ' ').replace(',', ' '). \
            replace('-', ' ').replace('.', ' ').replace('|', ' ').replace('=', ' '). \
            replace('+', ' ').replace('`', ' ').replace('¶', ' ').replace('═', ' '). \
            replace('▓', ' ').replace('~', ' ').lower().split()

        for word in words:
            if word not in self.stop_words:
                if word.startswith('креди') or word.startswith('карт') or word.startswith \
                            ('оформ') or word.startswith('онла') or word.startswith \
                            ('заяв') or word.startswith('бан') or word.startswith('истор'):
                    continue
                if '_' not in word and word.isdigit() == False:
                    if len(word) < 4:
                        continue
                    if word not in attr.get(key):
                        attr.get(key).update({word: 1})
                    else:
                        attr.get(key).update({word: attr.get(key).get(word) + 1})

    @staticmethod
    def _bdate_condition(key: str, value, attr: dict,):
        if key not in attr:
            attr.update({key: {}})

        year_date = value.split('.')
        if len(year_date) == 3:
            year_date = int(year_date[2])
            if year_date not in attr.get(key):
                attr.get(key).update({year_date: 1})
            else:
                attr.get(key).update({year_date: attr.get(key).get(year_date) + 1})

    @staticmethod
    def _occupation_condition(key: str, value, attr: dict,):
        if key not in attr:
            attr.update({key: {}})
        value = value.get('name')
        if value not in attr.get(key):
            attr.get(key).update({value: 1})
        else:
            attr.get(key).update({value: attr.get(key).get(value) + 1})

    @staticmethod
    def _personal_condition(key: str, value, attr: dict):
        for pk, vk in value.items():
            if pk not in attr:
                attr.update({pk: {}})

            if isinstance(vk, list):
                for lang in vk:
                    if lang not in attr.get(pk):
                        attr.get(pk).update({lang: 1})
                    else:
                        attr.get(pk).update({lang: attr.get(pk).get(lang) + 1})

            if isinstance(vk, int):
                if vk not in attr.get(pk):
                    attr.get(pk).update({vk: 1})
                else:
                    attr.get(pk).update({vk: attr.get(pk).get(vk) + 1})

            if isinstance(vk, str):
                if vk not in attr.get(pk):
                    attr.get(pk).update({vk: 1})
                else:
                    attr.get(pk).update({vk: attr.get(pk).get(vk) + 1})

    @staticmethod
    def _career_condition(key: str, value, attr: dict):
        if 'company' not in attr and 'position' not in attr:
            attr.update({'company': {}})
            attr.update({'position': {}})

        for i in range(len(value)):
            company = value[i].get('company')
            position = value[i].get('position')

            if company not in attr.get('company'):
                attr.get('company').update({company: 1})
            else:
                attr.get('company').update(
                    {company: attr.get('company').get(company) + 1})

            if position not in attr.get('position'):
                attr.get('position').update({position: 1})
            else:
                attr.get('position').update(
                    {position: attr.get('position').get(position) + 1})

    @staticmethod
    def _schools_condition(key: str, value, attr: dict):
        if key not in attr:
            attr.update({key: {}})

        for i in range(len(value)):
            speciality = value[i].get('speciality')

            if speciality not in attr.get(key):
                attr.get(key).update({speciality: 1})
            else:
                attr.get(key).update({speciality: attr.get(key).get(speciality) + 1})

    @staticmethod
    def counter_keys(key: str, value, attr: dict):
        if value not in attr.get(key):
            attr.get(key).update({value: 1})
        else:
            attr.get(key).update({value: attr.get(key).get(value) + 1})

    def get_frequency_statistic(self, n: int=100):
        """
        sorted value in key frequency
        :param n: count sample
        :return:
        """
        changed_value_list = ['sex', 'relation', 'political',
                              'people_main', 'life_main', 'smoking', 'alcohol']
        attributes = self.get_parse_data()
        bc = {}
        for key in attributes:
            if key == 'bdate':
                bd_range = {}
                for year, count in attributes.get(key).items():
                    if 1970 > year:
                        bd_range.update(
                            {'old 1970': bd_range.get('old 1970') + count}) if bd_range.get(
                            'old 1970') else bd_range.update({'old 1970': count})
                    elif year <= 1975:
                        bd_range.update(
                            {'1971-1975': bd_range.get('1970-1975') + count}) if bd_range.get(
                            '1970-1975') else bd_range.update({'1970-1975': count})
                    elif year <= 1980:
                        bd_range.update(
                            {'1976-1980': bd_range.get('1976-1980') + count}) if bd_range.get(
                            '1976-1980') else bd_range.update({'1976-1980': count})
                    elif year <= 1985:
                        bd_range.update(
                            {'1981-1985': bd_range.get('1981-1985') + count}) if bd_range.get(
                            '1981-1985') else bd_range.update({'1981-1985': count})
                    elif year <= 1990:
                        bd_range.update(
                            {'1986-1990': bd_range.get('1986-1990') + count}) if bd_range.get(
                            '1986-1990') else bd_range.update({'1986-1990': count})
                    elif year <= 1995:
                        bd_range.update(
                            {'1991-1995': bd_range.get('1991-1995') + count}) if bd_range.get(
                            '1991-1995') else bd_range.update({'1991-1995': count})
                    elif year <= 2000:
                        bd_range.update(
                            {'1996-2000': bd_range.get('1996-2000') + count}) if bd_range.get(
                            '1996-2000') else bd_range.update({'1996-2000': count})
                    elif year < 2010:
                        bd_range.update(
                            {'young 2010': bd_range.get('young 2010') + count}) if bd_range.get(
                            'young 2010') else bd_range.update({'young 2010': count})

                bd_range = sorted(bd_range.items(), key=lambda x: x[1], reverse=True)
                bc.update({key: bd_range})
            elif key in changed_value_list:
                if key not in bc:
                    bc.update({key: {}})
                if key == 'sex':
                    attributes.get(key)['female'] = attributes.get(key).pop(1)
                    attributes.get(key)['male'] = attributes.get(key).pop(2)
                    attributes.get(key)['not specified'] = attributes.get(key).pop(0)

                elif key == 'relation':
                    attributes.get(key)['Не указано'] = attributes.get(key).pop(0)
                    attributes.get(key)['Не женат'] = attributes.get(key).pop(1)
                    attributes.get(key)['Встречаюсь'] = attributes.get(key).pop(2)
                    attributes.get(key)['Помолвлен'] = attributes.get(key).pop(3)
                    attributes.get(key)['Женат'] = attributes.get(key).pop(4)
                    attributes.get(key)['В гражданском браке'] = attributes.get(key).pop(8)
                    attributes.get(key)['Влюблён'] = attributes.get(key).pop(7)
                    attributes.get(key)['Всё сложно'] = attributes.get(key).pop(5)
                    attributes.get(key)['В активном поиске'] = attributes.get(key).pop(6)

                elif key == 'political':
                    attributes.get(key)['Коммунистические'] = attributes.get(key).pop(1)
                    attributes.get(key)['Социалистические'] = attributes.get(key).pop(2)
                    attributes.get(key)['Умеренные'] = attributes.get(key).pop(3)
                    attributes.get(key)['Либеральные'] = attributes.get(key).pop(4)
                    attributes.get(key)['Консервативные'] = attributes.get(key).pop(5)
                    attributes.get(key)['Монархические'] = attributes.get(key).pop(6)
                    attributes.get(key)['Ультраконсервативные'] = attributes.get(key).pop(7)
                    attributes.get(key)['Индиферентные'] = attributes.get(key).pop(8)
                    attributes.get(key)['Либертарианские'] = attributes.get(key).pop(9)

                elif key == 'people_main':
                    attributes.get(key)['ум и креативность'] = attributes.get(key).pop(1)
                    attributes.get(key)['доброта и честность'] = attributes.get(key).pop(2)
                    attributes.get(key)['Красота и здоровье'] = attributes.get(key).pop(3)
                    attributes.get(key)['Власть и богатство'] = attributes.get(key).pop(4)
                    attributes.get(key)['Смелость и упорство'] = attributes.get(key).pop(5)
                    attributes.get(key)['Юмор и жизнелюбие'] = attributes.get(key).pop(6)

                elif key == 'life_main':
                    attributes.get(key)['семья и дети'] = attributes.get(key).pop(1)
                    attributes.get(key)['карьера и деньги'] = attributes.get(key).pop(2)
                    attributes.get(key)['развлечение и отдых'] = attributes.get(key).pop(3)
                    attributes.get(key)['наука и исследование'] = attributes.get(key).pop(4)
                    attributes.get(key)['соверщенствование мира'] = attributes.get(key).pop(5)
                    attributes.get(key)['саморазвитие'] = attributes.get(key).pop(6)
                    attributes.get(key)['красота и искусство'] = attributes.get(key).pop(7)
                    attributes.get(key)['слава и влияние'] = attributes.get(key).pop(8)

                elif key == 'alcohol' or key == 'smoking':
                    attributes.get(key)['Не указано'] = attributes.get(key).pop(0)
                    attributes.get(key)['Резко негативное'] = attributes.get(key).pop(1)
                    attributes.get(key)['Негативное'] = attributes.get(key).pop(2)
                    attributes.get(key)['Компромиссное'] = attributes.get(key).pop(3)
                    attributes.get(key)['Нейтральное'] = attributes.get(key).pop(4)
                    attributes.get(key)['Положительное'] = attributes.get(key).pop(5)

                for kk, vv in attributes.get(key).items():
                    percent_value = round(vv / len(self.data) * 100, 3)
                    bc.get(key).update({kk: percent_value})
                sorted_values = sorted(bc.get(key).items(), reverse=True, key=lambda kv: kv[1])
                bc.update({key: sorted_values[:n]})

            else:
                sorted_value = sorted(attributes.get(key).items(), key=lambda x: x[1], reverse=True)
                bc.update({key: sorted_value[:n]})

        return bc

if __name__ == '__main__':
    a = BaseAnalytic('vk_users.json')
    data = a.get_frequency_statistic()
    b = 2