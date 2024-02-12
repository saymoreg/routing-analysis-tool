import json
import copy


class Routing_conditionals:
    def __init__(self, check_fl):
        self.conditions = dict()
        self.task = dict()
        self.info = dict()

        self.check_fl = check_fl
        self.result = []
        self.meta_info = {'tags': []}
        self.countr_occurrences = 0
        self.count_c = 0
        self.tec_meta = False
        self.last_action = ''
        self.text_print = []
        self.text_true = ' TRUE'
        self.text_false = ' FALSE'
        self.not_field = [
            'login', 'tags_added', 'tags_changes', 'created', 'action', 'reopen_at', 'in_addition', 'action_id',
            'query_params', 'macro_ids', 'online_chat_processing_start', 'meta_changes', 'hidden_comment',
            'speed_answer_start', 'comment', 'new_line'
        ]

    def we_check_the_conditions_for_duplicates(self, list_receiving, text):
        return f'{list_receiving}' + text

    def sheet_bulkhead_list(self, list_receiving, list_or_str_necessary_meta_info, flag):
        if isinstance(list_receiving, list):
            if isinstance(list_or_str_necessary_meta_info, list):
                for i in range(len(list_receiving)):
                    if flag:
                        if list_receiving[i] in list_or_str_necessary_meta_info:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_true)
                        else:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_false)
                    else:
                        if list_receiving[i] in list_or_str_necessary_meta_info:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_false)
                        else:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_true)

                return list_receiving
            else:
                for i in range(len(list_receiving)):
                    if flag:
                        if list_receiving[i] == list_or_str_necessary_meta_info:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_true)
                        else:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_false)
                    else:
                        if list_receiving[i] == list_or_str_necessary_meta_info:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_false)
                        else:
                            list_receiving[i] = self.we_check_the_conditions_for_duplicates(list_receiving[i],
                                                                                            self.text_true)

                return list_receiving
        else:
            if isinstance(list_or_str_necessary_meta_info, list):
                if flag:
                    if list_receiving in list_or_str_necessary_meta_info:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_true)
                    else:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_false)
                else:
                    if list_receiving in list_or_str_necessary_meta_info:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_false)
                    else:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_true)

                return list_receiving
            else:
                if flag:
                    if list_receiving == list_or_str_necessary_meta_info:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_true)
                    else:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_false)
                else:
                    if list_receiving == list_or_str_necessary_meta_info:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_false)
                    else:
                        list_receiving = self.we_check_the_conditions_for_duplicates(list_receiving, self.text_true)

            return list_receiving

    def sheet_bulkhead_exists(self, receiving, list_or_str_necessary_meta_info, flag):
        if flag:
            if list_or_str_necessary_meta_info.get(receiving):
                return '#exists True: Объект нашелся в мете TRUE'
            else:
                return '#exists True: Объекта НЕТ FALSE'
        else:
            if list_or_str_necessary_meta_info.get(receiving):
                return '#exists False: Объект нашелся в мете FALSE'
            else:
                return '#exists False: Объекта НЕТ TRUE'

    def edits_to_the_condition_itself(self, result_condition, task):
        if isinstance(result_condition, list):
            for list_result_condition in result_condition:
                self.edits_to_the_condition_itself(list_result_condition, task)
        if isinstance(result_condition, dict):
            if "#or" in result_condition:
                self.edits_to_the_condition_itself(result_condition.get("#or"), task)

            if "#and" in result_condition:
                self.edits_to_the_condition_itself(result_condition.get("#and"), task)
            if "#not" in result_condition:
                self.edits_to_the_condition_itself(result_condition.get("#not"), task)

            for key, value in result_condition.copy().items():
                if key not in ("#or", "#and", "#not"):
                    if 'fields/' in key:
                        key_split = key.split('fields/')[1]
                    else:
                        key_split = key

                    if isinstance(value, dict):

                        if value.get('#nin') and value.get('#in'):
                            result_condition[key]['#nin'] = self.sheet_bulkhead_list(value.get('#nin'),
                                                                                     task.get(key_split), False)
                            result_condition[key]['#in'] = self.sheet_bulkhead_list(value.get('#in'),
                                                                                    task.get(key_split), True)

                        elif value.get('#in'):
                            result_condition[key]['#in'] = self.sheet_bulkhead_list(value.get('#in'),
                                                                                    task.get(key_split), True)

                        elif value.get('#nin'):
                            result_condition[key]['#nin'] = self.sheet_bulkhead_list(value.get('#nin'),
                                                                                     task.get(key_split), False)

                        elif value.get('#exists') == True or value.get('#exists') == False:
                            result_condition[key]['#exists'] = self.sheet_bulkhead_exists(key_split, task,
                                                                                          value.get('#exists'))

                    else:
                        if isinstance(task.get(key_split), list):
                            result_condition[key] = self.sheet_bulkhead_list(value, task.get(key_split), True)
                        else:
                            if task.get(key_split) == value:
                                result_condition[key] = self.we_check_the_conditions_for_duplicates(str(value),
                                                                                                    self.text_true)
                            else:
                                result_condition[key] = self.we_check_the_conditions_for_duplicates(str(value),
                                                                                                    self.text_false)

    def we_look_at_the_nested_conditions(self, condition, task, items=[], count=0, n=0, mool=False):

        boolean_or_and = [False, False]
        if isinstance(condition, list):
            for list_condition in condition:
                n += 1
                items[-1][2] = n
                self.result.append('-> list')
                self.we_look_at_the_nested_conditions(list_condition, task, items, mool=mool)
                self.result.append('list ->')
                boolean_or_and[0] = True

        if isinstance(condition, dict):
            if "#or" in condition:
                condition_or = condition.get("#or")
                self.countr_occurrences += 1
                items.append(['or', self.countr_occurrences, n])
                self.result.append('-> or')
                self.we_look_at_the_nested_conditions(condition_or, task, items, mool=mool)
                self.result.append('or ->')
                self.countr_occurrences -= 1
                del items[-1]

            if "#and" in condition:
                items.append(['and', self.countr_occurrences, n])
                self.countr_occurrences += 1
                condition_and = condition.get("#and")
                self.result.append('-> and')
                self.we_look_at_the_nested_conditions(condition_and, task, items, mool=mool)
                self.result.append('and ->')
                self.countr_occurrences -= 1
                del items[-1]

            if "#not" in condition:
                items.append(['not', self.countr_occurrences, n])
                self.countr_occurrences += 1
                condition_not = condition.get("#not")
                self.result.append('-> not')
                self.we_look_at_the_nested_conditions(condition_not, task, items, mool=mool)
                self.result.append('not ->')
                self.countr_occurrences -= 1
                del items[-1]

            for key, value in condition.items():
                count += 1
                if key not in ("#or", "#and", "#not"):
                    self.count_c += 1
                    re = []

                    for item in items:
                        re.append(list(item))

                    if 'fields/' in key:
                        key = key.split('fields/')[1]

                    oem = ''

                    if isinstance(value, dict):
                        if value.get('#in'):
                            if isinstance(task.get(key), list):
                                if (any(map(lambda v: v in task.get(key), value.get('#in')))):
                                    oem = 'True'
                                else:
                                    oem = 'False'
                            else:
                                if value.get('#nin'):
                                    if task.get(key) in value.get('#in') and task.get(key) not in value.get('#nin'):
                                        oem = 'True'
                                    else:
                                        oem = 'False'
                                else:
                                    if task.get(key) in value.get('#in'):
                                        oem = 'True'
                                    else:
                                        oem = 'False'

                        if value.get('#nin'):
                            if isinstance(task.get(key), list):
                                if (any(map(lambda v: v in task.get(key), value.get('#nin')))):
                                    oem = 'False'
                                else:
                                    oem = 'True'
                            else:
                                if value.get('#in'):
                                    if task.get(key) in value.get('#in') and task.get(key) not in value.get('#nin'):
                                        oem = 'True'
                                    else:
                                        oem = 'False'
                                else:
                                    if task.get(key) in value.get('#nin'):
                                        oem = 'False'
                                    else:
                                        oem = 'True'

                        if value.get('#exists') == True or value.get('#exists') == False:
                            if not value.get('#exists'):
                                if task.get(key):
                                    oem = 'False'
                                else:
                                    oem = 'True'
                            else:
                                if task.get(key):
                                    oem = 'True'
                                else:
                                    oem = 'False'

                        if value.get('#nin') and value.get('#in'):
                            if isinstance(task.get(key), list):
                                if (any(map(lambda v: v in task.get(key), value.get('#in')))) and not (
                                any(map(lambda v: v in task.get(key), value.get('#nin')))):
                                    oem = 'True'
                                else:
                                    oem = 'False'

                            else:
                                if (task.get(key) in value.get('#in')) and not (task.get(key) in value.get('#nin')):
                                    oem = 'True'
                                else:
                                    oem = 'False'
                    else:
                        if isinstance(task.get(key), list):
                            if value in task.get(key):
                                oem = 'True'
                            else:
                                oem = 'False'
                        else:
                            if task.get(key) == value:
                                oem = 'True'
                            else:
                                oem = 'False'

                    if mool:
                        self.result.append([self.count_c, self.countr_occurrences, count, re, key, key])
                    else:
                        self.result.append([self.count_c, self.countr_occurrences, count, re, key, oem])

    def spiosk_bez_not(self, spiosk):
        spiosk_new = []
        for value in spiosk:
            if value[0] in ('or', 'and'):
                spiosk_new.append(value[0])
        if spiosk_new:
            return spiosk_new[-1]
        else:
            return 'and'

    def filter(self, result, mool):
        list_count_result = []
        or_and = []
        text = ''

        for count in range(len(result)):
            if isinstance(result[count], list):
                list_count_result.append(count)

        for count in range(len(result)):
            actions = result[count]

            """
            Формирования булевой переменной
            """
            if isinstance(actions, str):
                boolean_variable = self.spiosk_bez_not(actions[3])

                if actions.split()[1] in ('or', 'and'):
                    or_and.append(actions.split()[1])
                if actions.split()[0] in ('or', 'and'):
                    del or_and[-1]

                if actions == 'list ->' and result[count + 1] == '-> list':
                    boolean_variable = result[count - 1][3][-1][0]
                if or_and:
                    boolean_variable = or_and[-1]

            else:
                if self.last_action in ['or ->', 'and ->']:
                    boolean_variable = 'and'
                else:
                    boolean_variable = self.spiosk_bez_not(actions[3])
                if count > 1:
                    if isinstance(result[count - 1], list):
                        if result[count - 1][2] < actions[2]:
                            boolean_variable = 'and'
            self.last_action = actions
            """
            Формирования скобок
            """

            if isinstance(actions, str):
                if '->' in actions.split()[0]:
                    if len(text) > 1:
                        if text[-1] == ')':
                            text += f' {boolean_variable} '
                    text += '('
                elif '->' in actions.split()[1]:
                    if 'list' == actions.split()[0]:
                        text += f') {boolean_variable} '
                    else:
                        if text[-1] == ' ' and text[-2] == 'd':
                            text = text[0:-5] + ')'
                        elif text[-1] == ' ' and text[-2] == 'r':
                            text = text[0:-4] + ')'
                        else:
                            text += ')'
            else:
                if len(text) >= 1:
                    if text[-1] == '(' and text[-2] == ')' or text[-1] == '(' and text[-2] == 't':
                        text = f') {boolean_variable} not('.join(
                            f') {boolean_variable} ('.join(text.split(')(')).split(') not('))
                if actions[3]:
                    if text[-1] == '(':
                        text += actions[-1]
                    else:
                        if text[-2] != 'd' and text[-2] != 'r' and text[-1] != ' ' or isinstance(text[-1], str):
                            text += f' {boolean_variable} ' + actions[-1]
                        else:
                            text += actions[-1]

                else:
                    if text:
                        text += f' {boolean_variable} ' + actions[-1]
                    else:
                        text += actions[-1]

            if actions == '-> not':
                text1 = f') not('.join(text.split(')('))
                if text1 == text:
                    text = text[0:-1] + 'not' + '('
                else:
                    text = text1
            text = ' and '.join(text.split(' and  and '))
        if text:
            self.text_print.append(f'Фильтр: {text}')

            if not mool:
                return eval(text)
        else:
            self.text_print.append('Пусто')

    def update_meta(self):

        for history in self.task['history']:
            if history.get('meta_changes'):
                for k in history.get('meta_changes'):
                    self.meta_info[k.get('field_name')] = k.get('value')

        save_keys = []
        for key, value in self.task['meta_info'].items():
            if self.meta_info.get(key) is not None:
                if self.meta_info[key] != value:
                    save_keys.append(key)
            else:
                save_keys.append(key)

        for key in save_keys:
            self.meta_info[key] = self.task['meta_info'][key]

        if self.tec_meta:
            for key, value in self.task.items():
                if isinstance(value, str) or value == None or isinstance(value, int):
                    self.meta_info[key] = value

    def collecting_all_the_values(self, count):
        self.we_look_at_the_nested_conditions(self.conditions.get('conditions'), self.meta_info, mool=False)
        self.info[f'info_log/{self.conditions["title_tanker"].split("lines.")[1]}_{count}'] = copy.copy(self.result)
        inf = self.filter(self.result, mool=False)
        self.result = []
        self.we_look_at_the_nested_conditions(self.conditions.get('conditions'), self.meta_info, mool=True)
        self.filter(self.result, mool=True)
        self.result = []
        result_condition = copy.deepcopy(self.conditions.get('conditions'))
        self.edits_to_the_condition_itself(result_condition, self.meta_info)
        self.info[f'info_log_conditions/{self.conditions["title_tanker"].split("lines.")[1]}_{count}'] = result_condition
        return inf

    def sborka(self):
        self.meta_info['type'] = self.task['chat_type']
        check = 0

        for count, history in enumerate(self.task['history']):
            for key, value in history.items():
                if key not in self.not_field:
                    self.meta_info[key] = value

            if history.get('tags_added'):
                for tags_added in history.get('tags_added'):
                    self.meta_info['tags'].append(tags_added)

            if history.get('tags_changes'):
                for tags_change in history.get('tags_changes'):
                    self.meta_info['tags'].append(tags_change['tag'])

            if history.get('meta_changes'):
                for meta_change in history.get('meta_changes'):
                    if meta_change.get('field_name') != 'tags':
                        self.meta_info[meta_change.get('field_name')] = meta_change.get('value')

            if history.get('action') == 'forward' and history.get('login') == 'superuser' and self.check_fl == 0:
                check += 1
                self.text_print.append(f'Роутинг: {self.collecting_all_the_values(count)}')
                self.text_print.append(f'history [{count}]: {history.get("action")} | superuser')

            elif history.get('action') == 'take' and check == 0 and self.check_fl == 1:
                check += 1
                self.text_print.append(f'Роутинг: {self.collecting_all_the_values(count)}')
                self.text_print.append(f'history [{count}]: {history.get("action")} | superuser')

            elif self.check_fl == 2 and len(self.task['history']) - 1 == count:
                self.text_print.append(f'Роутинг: {self.collecting_all_the_values(count)}')
                self.text_print.append(f'history [{count}]: {history.get("action")} | superuser')
                break

    def result_finis(self):
        result = []
        count = 0
        for k, v in self.info.items():
            if 'info_log_conditions/' in k:
                result.append({
                    'filter_bool': self.text_print[0 + count],
                    'filter_filed': self.text_print[1 + count],
                    'routing': self.text_print[2 + count],
                    'info': self.text_print[3 + count],
                    'conditions': v
                })
                count += 4
        return result

    def run(self, conditions, task):
        self.conditions = conditions
        self.task = task
        self.update_meta()
        self.sborka()
        return self.result_finis()


if __name__ == '__main__':
    #Для теста запуск
    r = Routing_conditionals(0)
    with open('conditions.json', 'r', encoding='utf-8') as f1:
        conditions: dict = json.load(f1)

    with open('task.json', 'r', encoding='utf-8') as f1:
        task: dict = json.load(f1)


    print(r.run(conditions=conditions, task=task))
    # 0 - это все действия суперюзера
    # 1 - первое действие
    # 2 - последнее