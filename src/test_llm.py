from ollama import chat


def main():
    print("Sending request to Ollama...")

    response = chat(
        model="qwen3.5:4b",
        messages=[
            {
                "role": "user",
                "content": "RAG를 한 문장으로 설명해 주세요.",
            }
        ],
        think=False,
    )

    print("Response received")

    answer = response["message"]["content"]

    print("\nGenerated answer")
    print(answer)


if __name__ == "__main__":
    main()
