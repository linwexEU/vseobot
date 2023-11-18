from app.function.func import FunctionBot

 
def get_question(code: str, name: str, test_id: int) -> None: 
    fc = FunctionBot(f"https://vseosvita.ua/test/go-settings?code={code}", test_id) 

    if name == "":
        fc.get_into_the_test("ㅤㅤㅤ ㅤㅤ")
    else: 
        fc.get_into_the_test(name)

    fc.pass_the_tests()

