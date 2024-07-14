def configure_final_answer_prompt(label, text, query):
    final_answer_prompt_template = \
f'''
!Задача!
Определи наиболее релевантный пункт текста и дай ответ на вопрос

!формат ответа !
Запрос: <входящий запрос>
Ответ: <число рублей> рублей
Норма: <Норма>

!Входные данные!
Норма: {label}
Текст закона: {text}
Запрос: {query}
'''
    return final_answer_prompt_template