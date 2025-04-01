import pandas as pd
from time import sleep
from openai import OpenAI
from rouge import Rouge

client = OpenAI(
    api_key="your api key here"
    # base_url="your base url here"
)

def calculate_rougeL_score(prediction, reference):
    rouge = Rouge()
    scores = rouge.get_scores(prediction, reference, avg=True)
    return scores['rouge-l']['f']

def ask_text(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": question}
                    ],
                }
            ]
        )
        answer = response.choices[0].message.content
        return answer
    except Exception as e:
        print(f"Error in processing: {e}")
        return None

# Main function to process the Excel file
def process_questions(input_file, output_file, start_id, end_id, prefix1, prefix2, prefix3, prefix4, evaled_col:str):
    df = pd.read_excel(input_file)
    output_df = pd.DataFrame(columns=['question_id', 'score'])

    for index, row in df.iterrows():
        q_id = row['question_id']
        if row['gt'] == '' or pd.isnull(row['gt']):
            output_df = output_df._append({'question_id': q_id, 'score': "0"}, ignore_index=True)
            output_df.to_excel(output_file, index=False)
            print(f"Stored evaluated result for question_id {q_id}")
            sleep(1)
            continue
        try:
            if start_id <= q_id <= end_id:
                if 1243 <= q_id <= 1292 or 2710 <= q_id <= 2859:
                    response = calculate_rougeL_score(row[evaled_col], row['gt'])
                else:
                    formatted_question = f"{prefix1}{row['question']}{prefix2}{row['gt']}{prefix3}{row[evaled_col]}{prefix4}"
                    response = ask_text(formatted_question)
                output_df = output_df._append({'question_id': q_id, 'score': response}, ignore_index=True)
                output_df.to_excel(output_file, index=False)
                print(f"Stored evaluated result for question_id {q_id}")

                sleep(1)
        except Exception as e:
            print(f"Error in processing question_id {q_id}: {e}")
            output_df = output_df._append({'question_id': q_id, 'score': "0"}, ignore_index=True)
            output_df.to_excel(output_file, index=False)
            print(f"Stored evaluated result for question_id {q_id}")
            sleep(1)

# Configuration
input_file = './eval_results/model_predictions.xlsx'
output_file = './eval_results/model_scores.xlsx'
start_id = 1   # change as needed
end_id = 3232   # change as needed
prefix1 = """You are an AI assistant who will help me evaluate responses given the questions and the correct answers. To assess a response, you should provide a single integer score like 0 or 1.
A score of 0 indicates that the response is entirely different from answers.
A score of 1 indicates that the response aligns perfectly with the answer or is correct for the given question and answer.

Question: """
prefix2 = "\nAnswer: "
prefix3 = "\nResponse: "
prefix4 = "\nYour mark: \n"

# Run the script
process_questions(input_file, output_file, start_id, end_id, prefix1, prefix2, prefix3, prefix4, "prediction")
