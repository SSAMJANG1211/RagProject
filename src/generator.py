from ollama import chat


class AnswerGenerator:
    def __init__(self, model_name="qwen3.5:4b"):
        self.model_name = model_name

    def generate(self, prompt):
        response = chat(
            model=self.model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            think=False,
        )

        answer = response["message"]["content"]

        return answer
