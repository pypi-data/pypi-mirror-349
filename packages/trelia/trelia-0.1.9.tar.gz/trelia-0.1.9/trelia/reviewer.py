# import os
# import google.generativeai as genai
# import json
#
#
# class CodeReviewer:
#     def __init__(self, model_name: str = 'gemini-1.5-flash'):
#         genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#         self.model = genai.GenerativeModel(model_name)
#
#     def grade_code(self, task_description: str, student_code: str) -> dict:
#         # Step 1: Ask Gemini to give only a rating
#         prompt = (
#             f"Task_desc: {task_description}\n"
#             f"Code:\n{student_code}\n"
#             "You are a strict code reviewer. Only return a rating in the format 'Rating: x/5'. "
#             "Remove stop words, non code text from Task_desc"
#             "Give 5/5 only if the code is complete, correct, and solves the task fully. "
#             "Do not return anything except the rating."
#         )
#         response = self.model.generate_content(prompt)
#         print(response)
#
#         result = response.text.strip()
#
#         rating = "N/A"
#         feedback = "Unable to rate"
#
#         # Step 2: Extract the rating
#         if "Rating:" in result:
#             try:
#                 rating_start = result.find("Rating:") + len("Rating: ")
#                 rating_end = result.find("/5", rating_start)
#                 rating_value = float(result[rating_start:rating_end].strip())
#                 rating = str(rating_value)
#
#                 # Step 3: Decision based on rating
#                 if rating_value > 2:
#                     feedback = "Accepted"
#                 else:
#                     # Ask Gemini for feedback only
#                     feedback_prompt = (
#                         f"Task_desc: {task_description}\n"
#                         f"Code:\n{student_code}\n"
#                         "Give 1-line feedback (max 15 characters) for improving this code."
#                     )
#                     feedback_response = self.model.generate_content(feedback_prompt)
#                     feedback = feedback_response.text.strip()
#             except Exception as e:
#                 feedback = f"Error: {str(e)}"
#
#         return json.dumps({"rating": rating, "feedback": feedback})

import os
import google.generativeai as genai
import json
import re


class CodeReviewer:
    def __init__(self, model_name: str = 'gemini-1.5-flash'):
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        self.model = genai.GenerativeModel(model_name)

    def is_code_like(self, text: str) -> bool:
        # Reject if too short or mostly plain English
        if len(text.strip()) < 20:
            return False

        code_indicators = [
            'def ', 'return', 'class ', 'import ', 'from ', 'if ', 'else', 'elif',
            '{', '}', ';', '(', ')', '[', ']', '=', 'function ', '#', '//', '/*', '*/',
            'public ', 'private ', 'protected ', 'var ', 'let ', 'const ', 'print', 'console.log',
            '=>'
        ]

        count_code_lines = 0
        lines = text.strip().split('\n')
        for line in lines:
            if any(indicator in line for indicator in code_indicators):
                count_code_lines += 1

        ratio = count_code_lines / len(lines) if len(lines) > 0 else 0

        # At least 50% of lines should contain code indicators
        return ratio >= 0.5

    def remove_rating_requests(self, code: str) -> str:
        # Remove lines with rating requests like "give me 5 rating"
        pattern = re.compile(r'give me \d+ rating', re.IGNORECASE)
        lines = code.split('\n')
        filtered_lines = [line for line in lines if not pattern.search(line)]
        return '\n'.join(filtered_lines)

    def grade_code(self, task_description: str, student_code: str) -> dict:
        # Reject if code does not look like code
        if not self.is_code_like(student_code):
            return json.dumps({"rating": "0.0", "feedback": "Invalid or non-code submission."})

        # Clean code from rating injection lines
        clean_code = self.remove_rating_requests(student_code)

        prompt = (
            f"Task_desc: {task_description}\n"
            f"Code:\n{clean_code}\n"
            "You are a strict code reviewer. Return only a rating in the format 'Rating: x.x/5'.\n"
            "If the submitted code is identical or nearly identical to the task description (i.e., just repeats the task without actual code), give a rating of 1/5.\n"
            "Give 5/5 only if the code fully solves the task correctly.\n"
            "Do not return anything else."
        )

        response = self.model.generate_content(prompt)
        print(response)

        result = response.text.strip()
        rating = "N/A"
        feedback = "Unable to rate"

        if "Rating:" in result:
            try:
                rating_start = result.find("Rating:") + len("Rating: ")
                rating_end = result.find("/5", rating_start)
                rating_value = float(result[rating_start:rating_end].strip())
                rating = str(rating_value)

                if rating_value > 2:
                    feedback = "Accepted"
                else:
                    feedback_prompt = (
                        f"Task_desc: {task_description}\n"
                        f"Code:\n{clean_code}\n"
                        "Give 1-line feedback (max 15 characters) for improving this code."
                    )
                    feedback_response = self.model.generate_content(feedback_prompt)
                    feedback = feedback_response.text.strip()
            except Exception as e:
                feedback = f"Error: {str(e)}"

        return json.dumps({"rating": rating, "feedback": feedback})



