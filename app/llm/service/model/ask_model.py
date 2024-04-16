
def inference(llm, prompt):
    output = llm(
      prompt, # Prompt
      max_tokens=2000,  # Generate up to 512 tokens
      stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
      echo=True        # Whether to echo the prompt
    )
    return output
