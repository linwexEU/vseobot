from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from question import TypeQuestion 
from bs4 import BeautifulSoup
import undetected_chromedriver
import time 
import re 


class FunctionBot: 
    ASCII = ["А", "Б", "В", "Г", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї", "Й", "К"]

    def __init__(self, link, test_id): 
        # Настройки для браузера
        options = webdriver.ChromeOptions() 
        options.add_argument('--no-sandbox')
        options.add_argument("--headless")

        # Запуск браузера
        self.browser = undetected_chromedriver.Chrome(options=options)
        self.browser.get(link)

        self.browser.execute_script(f"window.open('{link}', '_blank')")

        WebDriverWait(self.browser, 60).until( 
            EC.presence_of_all_elements_located((By.XPATH, "//button[@class='vo-go-login__btn orange']"))
        )

        # ID пользователя
        self.test_id = test_id

        # Количество вопросов в тесте
        self.count_of_question = None

        # Код для нажатий кнопок в тесте
        self.code = link.split("=")[-1]

        # Название теста
        self.name_of_the_test = None
        
        # Создание Файла 
        self.file_question = None 

    def get_into_the_test(self, name_for_test="ㅤㅤㅤ ㅤㅤ"):
        self.browser.switch_to.window(self.browser.window_handles[0])
        time.sleep(1)

        # Нажатие подтверждающей кнопки
        confirm_button = self.browser.find_element(By.XPATH, "//button[@class='vo-go-login__btn orange']")
        confirm_button.click() 
        
        WebDriverWait(self.browser, 10).until( 
            EC.presence_of_all_elements_located((By.XPATH, "//input[@id='testdesignersettings-full_name']"))
        )
        
        # Получение названия теста
        self.name_of_the_test = self.browser.find_element(By.XPATH, "//p[@class='a-center-class']").text.split("\n\n")[0].split(":")[-1].strip().replace("\"", "")

        # Создание сайта
        self.file_question = CreateFile(self.name_of_the_test, self.test_id)

        # Ввод имени (по умолчанию невидимый ник)
        name_input = self.browser.find_element(By.XPATH, "//input[@id='testdesignersettings-full_name']")
        name_input.send_keys(name_for_test) 
        
        
        # Сохранение имени
        save_button = self.browser.find_element(By.XPATH, "//button[@class='vo-go-login__btn orange']")
        save_button.click()

        WebDriverWait(self.browser, 10).until( 
            EC.presence_of_all_elements_located((By.XPATH, "//a[@class='v-hello-button v-z-index']"))
        )

        # Получение кол-во вопросов в тесте
        self.count_of_question = int(re.search("\d+", self.browser.find_element(By.XPATH, "//div[@class='v-hello-text-title']").find_element(By.TAG_NAME, "b").text).group())

        # Нажатие кнопки для начала теста
        start_test_button = self.browser.find_element(By.XPATH, "//a[@class='v-hello-button v-z-index']")
        start_test_button.click() 

        time.sleep(2)

    def save_and_go_button(self): 
        s_a_g_b = self.browser.find_element(By.CSS_SELECTOR, ".n-go-body-btn-col.v-blue-button-test")
        s_a_g_b.click()
        time.sleep(2)

    def go_down(self): 
        self.browser.execute_script("window.scrollBy(0, 10000);")

    def pass_the_tests(self): 
        # Обработка вопросов
        for _ in range(self.count_of_question + 1): 
            # Получение HTML кода
            src = self.browser.page_source 
            soup = BeautifulSoup(src, "lxml")

            # З ОДНІЄЮ ПРАВИЛЬНОЮ ВІДПОВІДДЮ | З КІЛЬКОМА ПРАВИЛЬНИМИ ВІДПОВІДЯМИ
            if soup.find("div", class_=TypeQuestion.ONE_CORECT_ANSWER.value):
                # Парсинг вопроса
                parsed = self.parse_the_question(TypeQuestion.ONE_CORECT_ANSWER.value)

                # Добавление вопроса в файл 
                self.file_question.add_question(TypeQuestion.ONE_CORECT_ANSWER.value, parsed)

                # Выбор варианта
                one_option = self.browser.find_element(By.XPATH, f"//input[@id='{self.code}-answer-0']")
                one_option.click()
                
                try:
                    WebDriverWait(self.browser, 3).until( 
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v-test-questions-radio-block n-checked color-1']"))
                    )
                except:
                    WebDriverWait(self.browser, 3).until( 
                        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v-test-questions-checkbox-block n-checked color-1']"))
                    )
                
                # Листаем вниз, чтоб видел кнопку (редкие случаи) 
                self.go_down()
                time.sleep(1)

                # Сохранение варианта и переход на следующий вопрос
                self.save_and_go_button()

                time.sleep(2)       
            # З ПОЛЕМ ДЛЯ ВВОДУ ВІДПОВІДІ
            elif soup.find("div", class_=TypeQuestion.INPUT_LAB.value): 
                # Парсинг вопроса
                parsed = self.parse_the_question(TypeQuestion.INPUT_LAB.value)

                # Добавление вопроса в файл 
                self.file_question.add_question(TypeQuestion.INPUT_LAB.value, parsed)

                # Ввод ответа в поле
                input_lab = self.browser.find_elements(By.XPATH, "//div[@class='content-box']")[-1].find_element(By.TAG_NAME, "input") 
                input_lab.send_keys("...") 
                
                time.sleep(1) 

                # Листаем вниз, чтоб видел кнопку (редкие случаи) 
                self.go_down()
                time.sleep(1)

                # Сохранение варианта и переход на следующий вопрос
                self.save_and_go_button()
            # НА ВСТАНОВЛЕННЯ ВІДПОВІДНОСТІ
            elif soup.find("div", class_=TypeQuestion.TO_ESTABLISH_COMPLIANCE.value):
                # Парсинг вопроса
                parsed = self.parse_the_question(TypeQuestion.TO_ESTABLISH_COMPLIANCE.value)

                # Добавление вопроса в файл 
                self.file_question.add_question(TypeQuestion.TO_ESTABLISH_COMPLIANCE.value, parsed)

                # Выбор первого варианта
                first_option = self.browser.find_element(By.XPATH, "//div[@class='rk-cross__item v-block-answers-table-numb']")
                first_option.click() 

                WebDriverWait(self.browser, 10).until( 
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v-block-answers-cross-block a-pointer-class n-checked color-1']"))
                )

                # Выбор первого ответа
                first_answer = self.browser.find_element(By.XPATH, "//div[@class='rk-cross__item v-block-answers-table-numb highlight']")
                first_answer.click() 

                time.sleep(1) 

                # Листаем вниз, чтоб видел кнопку (редкие случаи) 
                self.go_down()
                time.sleep(1)

                # Сохранение варианта и переход на следующий вопрос
                self.save_and_go_button()
            # ІЗ ЗАПОВНЕННЯМ ПРОПУСКІВ У ТЕКСТІ
            elif soup.find("span", class_=TypeQuestion.FILL_THE_GAP.value):
                # Парсинг вопроса
                parsed = self.parse_the_question(TypeQuestion.FILL_THE_GAP.value)

                # Добавление вопроса в файл 
                self.file_question.add_question(TypeQuestion.FILL_THE_GAP.value, parsed)

                # Нахождение всех форм с вводом текста
                for item in self.browser.find_elements(By.XPATH, "//span[@class='vr-fill-the-gap vr-control']"):
                    # Заполнение форм
                    input_lap_gap = item.find_element(By.TAG_NAME, "input") 
                    input_lap_gap.send_keys("...")

                time.sleep(1) 

                # Листаем вниз, чтоб видел кнопку (редкие случаи) 
                self.go_down()
                time.sleep(1)

                # Сохранение варианта и переход на следующий вопрос
                self.save_and_go_button()
            # З ВИБОРОМ ПРАВИЛЬНОЇ ВІДПОВІДІ У ТЕКСТІ
            elif soup.find("span", class_=TypeQuestion.FILL_THE_GAP_SELECT.value):
                # Парсинг вопроса
                parsed = self.parse_the_question(TypeQuestion.FILL_THE_GAP_SELECT.value)

                # Добавление вопроса в файл 
                self.file_question.add_question(TypeQuestion.FILL_THE_GAP_SELECT.value, parsed)

                # Форма с заполнением
                for item in self.browser.find_elements(By.XPATH, "//span[@class='vr-fill-the-gap-select vr-control']"):
                    item.find_elements(By.TAG_NAME, "option")[-1].click() 

                time.sleep(1)

                # Выбор варианта
                option = self.browser.find_element(By.XPATH, "//span[@class='vr-fill-the-gap-select vr-control']").find_element(By.TAG_NAME, "select").find_elements(By.TAG_NAME, "option")[-1]
                option.click()

                time.sleep(1) 

                # Листаем вниз, чтоб видел кнопку (редкие случаи) 
                self.go_down()
                time.sleep(1)

                # Сохранение варианта и переход на следующий вопрос
                self.save_and_go_button()
            # НА ВСТАНОВЛЕННЯ ПОСЛІДОВНОСТІ
            elif soup.find("div", class_=TypeQuestion.CONSISTENLY.value):
                # Парсинг вопроса
                parsed = self.parse_the_question(TypeQuestion.CONSISTENLY.value)

                #Добавление вопроса в файл 
                self.file_question.add_question(TypeQuestion.CONSISTENLY.value, parsed)

                # Листаем вниз, чтоб видел кнопку (редкие случаи) 
                self.go_down()
                time.sleep(1)

                # Сохранение варианта и переход на следующий вопрос
                self.save_and_go_button()

    def parse_the_question(self, type_of_question):
        # З ОДНІЄЮ ПРАВИЛЬНОЮ ВІДПОВІДДЮ | З КІЛЬКОМА ПРАВИЛЬНИМИ ВІДПОВІДЯМИ
        if type_of_question == TypeQuestion.ONE_CORECT_ANSWER.value: 
            # Собираем вопрос
            question = self.browser.find_element(By.XPATH, "//div[@class='content-box']").find_element(By.TAG_NAME, "div").text.strip() 
            
            # Собираем варианты ответа
            question_option = []
            count = 0 

            while True:
                try:
                    question_option.append(self.browser.find_element(By.XPATH, f"//label[@for='{self.code}-answer-{count}']").text.strip())
                    count += 1 
                except: 
                    break

            return (question, question_option)
        # З ПОЛЕМ ДЛЯ ВВОДУ ВІДПОВІДІ
        elif type_of_question == TypeQuestion.INPUT_LAB.value: 
            # Собираем вопрос
            question = self.browser.find_element(By.XPATH, "//div[@class='content-box']").find_element(By.TAG_NAME, "div").text.strip() 

            return question
        # НА ВСТАНОВЛЕННЯ ВІДПОВІДНОСТІ
        elif type_of_question == TypeQuestion.TO_ESTABLISH_COMPLIANCE.value: 
            soup = BeautifulSoup(self.browser.page_source, "lxml")

            # Собираем вопрос
            question = self.browser.find_element(By.XPATH, "//div[@class='content-box']").find_element(By.TAG_NAME, "div").text.strip()  

            # Собираем левую часть
            question_option = [] 
            for index1, item1 in enumerate(soup.find("div", class_="v-col-6").find_all("div", class_="n-kahoot-p")): 
                question_option.append(f'''{index1 + 1}) {item1.text}''')

            # Собираем правую часть
            answer_option = [] 
            for index2, item2 in enumerate(soup.find("div", class_="v-col-6 v-col-last").find_all("div", class_="n-kahoot-p")):
                answer_option.append(f'''{self.ASCII[index2]}) {item2.text}''')

            return (question, question_option, answer_option)
        # ІЗ ЗАПОВНЕННЯМ ПРОПУСКІВ У ТЕКСТІ
        elif type_of_question == TypeQuestion.FILL_THE_GAP.value:
            soup = BeautifulSoup(self.browser.page_source, "lxml")

            # Собираем вопрос
            question = self.browser.find_element(By.XPATH, "//div[@class='content-box']").find_element(By.TAG_NAME, "div").text.strip() 

            return (soup.find("div", class_="content-box").find("p").text.split("  "))
        # З ВИБОРОМ ПРАВИЛЬНОЇ ВІДПОВІДІ У ТЕКСТІ 
        elif type_of_question == TypeQuestion.FILL_THE_GAP_SELECT.value:
            soup = BeautifulSoup(self.browser.page_source, "lxml") 

            # Собирает вопрос
            question = re.sub(r"<span.+?</span>", "...", str(soup.find("div", class_="content-box").find("p")))[3:-4].split("...")

            # Собираем варианты ответа
            options = [f'({", ".join([i.text for i in item.find_all("option")[1:]])})' for item in soup.find_all("span", class_="vr-fill-the-gap-select vr-control")] 

            return (question, options)

        # НА ВСТАНОВЛЕННЯ ПОСЛІДОВНОСТІ 
        elif type_of_question == TypeQuestion.CONSISTENLY.value:
            # Собираем вопрос
            question = self.browser.find_element(By.XPATH, "//div[@class='content-box']").find_element(By.TAG_NAME, "div").text.strip() 

            options = [item.text for item in self.browser.find_elements(By.XPATH, "//div[@class='t-text-guest']")] 

            return (question, options) 


class CreateFile: 
    ASCII = ["А", "Б", "В", "Г", "Д", "Е", "Є", "Ж", "З", "И", "І", "Ї", "Й", "К"] 

    def __init__(self, name_of_the_test, test_id): 
        self.name_of_the_test = name_of_the_test
        self.count = 1 
        self.test_id = test_id
        with open(fr"all_tests\vseobot-question{self.test_id}.txt", "w", encoding="utf-8") as file:
            file.write("Done by vseobot 0.1 (linwexEU)\n")

    def add_question(self, type_question, question): 
        with open(fr"all_tests\vseobot-question{self.test_id}.txt", "a", encoding="utf-8") as file:
            # З ОДНІЄЮ ПРАВИЛЬНОЮ ВІДПОВІДДЮ | З КІЛЬКОМА ПРАВИЛЬНИМИ ВІДПОВІДЯМИ 
            if  type_question == TypeQuestion.ONE_CORECT_ANSWER.value:
                file.write("\n(З ОДНІЄЮ ПРАВИЛЬНОЮ ВІДПОВІДДЮ | З КІЛЬКОМА ПРАВИЛЬНИМИ ВІДПОВІДЯМИ)\n") 
                file.write(f"{self.count}. {question[0]}\n\n")

                for index, item in enumerate(question[1]): 
                    file.write(f"{self.ASCII[index]}) {item}\n")

                file.write(f"\n{('-' * 80)}\n")
                self.count += 1
            # З ПОЛЕМ ДЛЯ ВВОДУ ВІДПОВІДІ
            elif type_question == TypeQuestion.INPUT_LAB.value:
                file.write("\n(З ПОЛЕМ ДЛЯ ВВОДУ ВІДПОВІДІ)\n") 
                file.write(f"{self.count}. {question}\n") 
                
                file.write(f"\n{('-' * 80)}\n")
                self.count += 1
            # НА ВСТАНОВЛЕННЯ ВІДПОВІДНОСТІ
            elif type_question == TypeQuestion.TO_ESTABLISH_COMPLIANCE.value:
                file.write("\n(НА ВСТАНОВЛЕННЯ ВІДПОВІДНОСТІ)\n") 
                file.write(f"{self.count}. {question[0]}\n\n")

                for item in question[1]: 
                    file.write(f"{item}\n")

                file.write("\n") 

                for item in question[2]: 
                    file.write(f"{item}\n") 
                
                file.write(f"\n{('-' * 80)}\n")
                self.count += 1
            # ІЗ ЗАПОВНЕННЯМ ПРОПУСКІВ У ТЕКСТІ
            elif type_question == TypeQuestion.FILL_THE_GAP.value: 
                result = [] 
                for item in question:
                    result.append(item) 
                    if item != question[-1]: 
                        result.append("...")
                    else:
                        if item.endswith(" "): 
                            result.append("...")

                file.write("\n(ІЗ ЗАПОВНЕННЯМ ПРОПУСКІВ У ТЕКСТІ)\n") 
                file.write(f"{self.count}. {' '.join(result)}\n")

                file.write(f"\n{('-' * 80)}\n")
                self.count += 1
            # З ВИБОРОМ ПРАВИЛЬНОЇ ВІДПОВІДІ У ТЕКСТІ
            elif type_question == TypeQuestion.FILL_THE_GAP_SELECT.value: 
                question_full = [] 
                i = 0 
                for item in question[0]:
                    question_full.append(item) 

                    if i <= len(question[1]) - 1:
                        question_full.append(question[1][i])
                        i += 1

                file.write("\n(З ВИБОРОМ ПРАВИЛЬНОЇ ВІДПОВІДІ У ТЕКСТІ)\n") 
                file.write(f"{self.count}. {' '.join(question_full)}\n")

                file.write(f"\n{('-' * 80)}\n")
                self.count += 1
            # НА ВСТАНОВЛЕННЯ ПОСЛІДОВНОСТІ
            elif type_question == TypeQuestion.CONSISTENLY.value: 
                file.write("\n(НА ВСТАНОВЛЕННЯ ПОСЛІДОВНОСТІ)\n") 
                file.write(f"{self.count}. {question[0]}\n\n")

                for item in question[1]: 
                    file.write(f"{item}\n")

                file.write(f"\n{('-' * 80)}\n")
                self.count += 1


if __name__ == "__main__":
    fc = FunctionBot("https://vseosvita.ua/test/go-settings?code=hkj787", 1)
    fc.get_into_the_test()
    fc.pass_the_tests()
