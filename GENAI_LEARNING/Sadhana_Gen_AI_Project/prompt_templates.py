def get_mcq_prompt_template_specific(topic_name,difficulty_level,number):
    mcq_prompt_template_specific="""
   Imagine you are creating a quiz based on the following context by maintaining the below specified difficulty level. Your goal is to generate insightful multiple choice questions and their corresponding answers. Keep the questions diverse and thought-provoking.
   Don't use phrases like from the context, based on the context, within in the context in framing questions. Also try to form the questions on {topic_name} from the provided context, if you find nothing relevant to {topic_name} in provided context then try to 
   formulate questions from your own knowledge.

   Context:
   \n {context}\n

   Difficulty Level: {difficulty_level}

   Now generate {number} multiple-choice questions with their answers in the following format:

    Question: write question here
    a) Option A
    b) Option B
    c) Option C
    d) Option D
    Answer: [Model-Generated Answer J]

   Feel free to be creative and insightful! Your questions and answers will contribute to an engaging quiz experience.
      """
    return mcq_prompt_template_specific

def get_mcq_prompt_template_general(context,difficulty_level,number):
    mcq_prompt_template_general = f'''
    Imagine you are creating a quiz based on the following context by maintaining the below specified difficulty level. Your goal is to generate insightful multiple-choice questions and their corresponding answers. Keep the questions diverse and thought-provoking.
    Don't use phrases like from the context, based on the context, within in the context in framing questions.

    Context: {context}

    Difficulty Level: {difficulty_level}

    Now generate only {number} multiple-choice questions with their answers in the following format:

    Question: write question here
    a) Option A
    b) Option B
    c) Option C
    d) Option D
    Answer: [Model-Generated Answer A]

    Ensure the question is clear, concise, and relevant to the context. The correct answer should align with the information presented in the context.
    '''
    return mcq_prompt_template_general

def get_qa_prompt_template_specific(topic_name,difficulty_level,number):
    qa_prompt_template_specific="""
   Imagine you are creating a quiz based on the following context by maintaining the below specified difficulty level. Your goal is to generate insightful description answer type questions. Keep the questions diverse and thought-provoking.
   Don't use phrases like from the context, based on the context, within in the context in framing questions. Also try to form the questions on {topic_name} from the provided context, if you find nothing relevant to {topic_name} in provided context then try to 
   formulate questions from your own knowledge.

   Context:
   \n {context}\n

   Difficulty Level: {difficulty_level}

   Now generate {number} description answer type questions with their answers in the following format:

      - Question: [Model-Generated Question]
      - Answer: [Model-Generated Answer]


   Feel free to be creative and insightful! Your questions and answers will contribute to an engaging quiz experience.
      """
    return qa_prompt_template_specific

def get_qa_prompt_template_general(context,difficulty_level,number):
   qa_prompt_template_general = f'''
      Imagine you are creating a quiz based on the following context by maintaining the below specified difficulty level. Your goal is to generate insightful descriptive answer-type questions. Keep the questions diverse and thought-provoking.
      Don't use phrases like from the context, based on the context, within in the context in framing questions. 

      Context: {context}
      Difficulty Level: {difficulty_level}

      Now generate only {number} descriptive answer-type questions with their answers in the following format:

      - Question: [Model-Generated Question]
      - Answer: [Model-Generated Answer]

      Ensure the question is clear, concise, and relevant to the context. The answer should align with the information presented in the context.
      '''
   return qa_prompt_template_general
