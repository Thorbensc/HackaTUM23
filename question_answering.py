import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering, AutoModel
from scipy.spatial.distance import cosine
from chunking import LogChunker

class LogAIAgent():

    def __init__(self,model_name = "bert-large-uncased-whole-word-masking-finetuned-squad") -> None:
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name) #used for answering
        self.model_vec = AutoModel.from_pretrained(model_name) #used for vectorization
        self.tokenizer = AutoTokenizer.from_pretrained(model_name) #used for tokenization
        self.chunker = LogChunker()

    def _answer_question(self, context, question) -> str:
        # Encode the context and question
        encoded = self.tokenizer.encode_plus(question, context, truncation=True, padding='max_length', max_length=512, return_tensors='pt', add_special_tokens = True)
        # Get the start and end scores for all tokens
        result = self.model(**encoded)
        start_scores = result["start_logits"]
        end_scores = result["end_logits"]

        # Find the tokens with the highest start and end scores
        answer_start = torch.argmax(start_scores)
        answer_end = torch.argmax(end_scores)

        # If the end score is higher than the start score, swap them
        if answer_end < answer_start:
            answer_start, answer_end = answer_end, answer_start

        # Get the tokens for the answer
        all_tokens = self.tokenizer.convert_ids_to_tokens(encoded['input_ids'][0])
        answer = ' '.join(all_tokens[answer_start : answer_end+1])

        return answer

    def _calculate_similarity(self, question_vector, answer_vector) -> float:
        similarity = 1 - cosine(question_vector[0], answer_vector[0])

        return similarity

    def _vectorize_text(self, input_string) -> list:
        # Encode the input string
        inputs = self.tokenizer.encode_plus(
            input_string,
            add_special_tokens=True,
            return_tensors="pt",
            padding=True, truncation=True,max_length=512
        )
        # Get the output from the model
        outputs = self.model_vec(**inputs)
        # Get the embeddings from the last hidden state
        embeddings = outputs.last_hidden_state
        # Average the embeddings
        vector = torch.mean(embeddings, dim=1)
        # Convert tensor to numpy array
        vector = vector.detach().numpy()
        return vector

    

    def find_best_answer(self, context, question, num_answers=3, overlap=50, max_length=512) -> list:

        # Vectorize the question
        question_vector = self._vectorize_text(question)
        
        # Initialize the best answers and their similarities to the question
        best_answers = [(None, -1) for _ in range(num_answers)]
        
        # Split the context into chunks
        chunks = self.chunker.split_context(context)
        #filtered_chunks = self.chunker.filter_error_chunks(chunks)

        for chunk in chunks:
            answer = self._answer_question(chunk, question)
            if answer is not None:
                answer_vector = self._vectorize_text(answer)
                if answer_vector is not None:
                    similarity = self._calculate_similarity(question_vector, answer_vector)
                    # Check if the similarity is higher than the current lowest in best_answers
                    if similarity > best_answers[0][1]:
                        # Replace the lowest
                        best_answers[0] = (answer.replace(" ##", ''), similarity)
                        # Sort the list so the lowest similarity is first
                        best_answers = sorted(best_answers, key=lambda x: x[1])
        # Return the answers along with their similarities
        return best_answers

    