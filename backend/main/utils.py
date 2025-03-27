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
                        "You must generate quiz questions in multiple languages. You are not restricted to creating quizzes in"
                        "a single language (English) and can use different languages as needed."
                        "The preferred language for the quiz should be determined by the user's prompt. For example,"
                        "if the user prompts 'დამიგენერირე ქუიზი ფეხბურთზე' (which is in Georgian),"
                        "the generated quiz should be in Georgian."
                        "Generate a quiz with the number of questions requested by the user."
                        "User should specify whether generate quiz with possible answers or not"
                        "By default if user didn't specify format of generating quiz e.g. ('Generate quiz about football') you shouldn't provide questions with possible answers. Format should be e.g. {\"Who won the champions league in 1977\": []}"
                        "If user specifies to generate quiz with possible questions return the result like that: {\"What color is the sky\": ['Blue', 'Red', 'Green' 'Purple']}"
                        "Returned object must be in json format."
                        "e.g. {\"Who lost the World War II\": ['Germany', 'USA', 'USSR', 'Brazil']} "
                        "You must provide 'topic_name' field in json response in case you generate Quiz"
                        "e.g. If user prompts 'Generate quiz about football'"
                        "Response should have 'topic_name' field  e.g {\"topic_name\": 'Football'}"
                        "The 'topic_name' field must always be provided in English,"
                        "regardless of the language in which the quiz is generated."
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

    @staticmethod
    def compute_quiz_result(questions, answers):
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You should evaluate the results of a quiz."
                        "The user will provide you with quiz questions and their corresponding answers."
                        "You should return the result as a JSON object, e.g. {\"result\": \"7/10\"}"
                        "where '7' represents the total number of correct answers,"
                        "and '10' indicates the total number of questions."
                        "The user's prompt will look like this: 'Here are the questions:"
                        "[\"What's 2+2\", \"What color is the sky\"]"
                        "And here are the answers: [\"4\", \"red\"]"
                        "Based on this example, your response must be: {\"result\": \"1 / 2\"}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Here are the questions: {questions} And here are the answers: {answers}"
                }
            ]
        )
        return completion.choices[0].message.content
