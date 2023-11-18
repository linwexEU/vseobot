from app.tests.dao import TestDAO


async def get_id_test(user_id: int): 
    tests_id = await TestDAO.get_user_tests(user_id)
    return tests_id


async def get_text_from_file(test_id: int) -> list:  
    with open(f"all_tests/vseobot-question{test_id}.txt", encoding="utf-8") as file:
        file_content = [line.split("\n") for line in file.read().split("-" * 80)]
         
    return [[line for line in item if line != ""] for item in file_content if item != []][:-1]
