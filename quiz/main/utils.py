from openai import OpenAI
from decouple import config

client = OpenAI(
    api_key=config('OPEN_AI_KEY'))


class QuizGenerator:

    @staticmethod
    def generate_quiz(user_input):
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a quiz generator, you must generate questions based on user prompt."
                        "Generate a quiz with the number of questions requested by the user."
                        "User should specify whether generate quiz with possible answers or not"
                        "By default if user didn't specify format of generating quiz e.g. ('Generate quiz about football') you shouldn't provide questions with possible answers. Format should be e.g. {\"Who won the champions league in 1977\": []}"
                        "If user specifies to generate quiz with possible questions return the result like that: {\"What color is the sky\": ['Blue', 'Red', 'Green' 'Purple']}"
                        "Returned object must be in json format."
                        "e.g. {\"Who lost the World War II\": ['Germany', 'USA', 'USSR', 'Brazil']} "
                        "You must provide 'topic_name' field in json response in case you generate Quiz"
                        "e.g. If user prompts 'Generate quiz about football'"
                        "Response should have 'topic_name' field  e.g {\"topic_name\": 'Football'}"
                        "Also along with 'topic_name' field, provide 'has_possible_answers' field in json object"
                        "e.g. {\"Who flew to the moon first\": [], \"has_possible_answers\": False, \"topic_name\": 'History'}"
                        "Don't include any other characters in the response, only Json format output"
                        "Provide only 'True' or 'False' in \"has_possible_answers\" field. not fill that with 'true' or 'false'"
                        "If user prompts valid topic and pass all the validations, final version of response format should be in that way"
                        "{\"What is 2+2\": ['1', '2', '3', '4'], \"has_possible_answers\": True, \"topic_name\": 'Math'}"
                    )
                },
                {
                    "role": "system",
                    "content": (
                        "Limit the number of questions to a maximum of 10."
                        "If the user requests more than 10 questions, set the 'message' field to: "
                        "'The maximum number of questions I can generate is 10.'"
                        "If the user provides input unrelated to quiz generation (e.g., 'Hello, World'),"
                        "set the 'message' field to: "
                        "'I am a Quiz Generator. Please provide a valid topic to generate a quiz for you!'"
                        "You must generate quiz only in English Language.If user demands to generate quiz in any other language"
                        "or prompts using different languages e.g. 'Генерируйте викторину про Лео Месси'"
                        "set the 'message' field to: I can only generate quiz in English Language."
                        "The maximum number of possible answers must be 4"
                        "If user requests more than 4 possible answers, set the 'message' field to:"
                        "Maximum size of possible answers is 4."
                    )
                },
                {
                    "role": "user",
                    "content": user_input
                },
            ],
        )

        return completion.choices[0].message.content
