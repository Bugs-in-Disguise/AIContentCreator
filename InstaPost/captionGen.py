from google import genai

def generate_instagram_post(industry, audience, description):
    api_key = "AIzaSyC4_Of0KLBwuZ-x6JmzBroOnso580FnQCg"
    model = "gemini-2.0-flash"

    client = genai.Client(api_key=api_key)

    prompt = (
        f"WRITE A SINGLE engaging Instagram post caption for a business in the {industry} industry. "
        f"The target audience is {audience}. "
        f"Here is a description of the post: {description}"
    	f"Use less than 100 words"
    )
    response = client.models.generate_content(
        model=model, 
        contents=prompt,
        config=genai.types.GenerateContentConfig(
            system_instruction='you create short and engaging social media captions',
            max_output_tokens= 400,
            top_k= 1,
            top_p= 0.5,
            temperature= 1,
            response_mime_type= 'text/plain',
        ),
    )
    return response.text

# Example usage
if __name__ == "__main__":

    industry = input("What industry are you a part of? ")
    audience = input("What is your target Audience? ")
    description = input("Describe the purpose behind your post: ")
    # industry = "flowers"
    # audience = "highschoolers"
    # description = "dont forget to give your prom date some beautiful flowers"

    post_text = generate_instagram_post(industry, audience, description)
    print(post_text)


