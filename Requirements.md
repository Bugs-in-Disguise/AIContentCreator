# Requirements
## Overview
Social media is becoming one of the most effective ways to market products, but can be difficult to get into.
Small buisnesses often lack time, resources, expertiese, and know-how needed to create engaging social media content.
Our solution is an AI powered tool that can generate, post, and monitor social media.
### Objectives:
- Automate content creation process for small business
- Provide engaging post ideas
- generate content from various sources
- Schedule posts on multiple social media platforms.
## Scope (using MoSCoW)
- Core functionalities
	- PostNow: lets user input image, industry, audience, description and post
	- PostLater: Lets user input multiple images and schedule for repeating posts without them doing anything
	- Success Metric
- Out-of-scope features
    - AI image editing
### Manual Tasks:
- The idea here is to start by having one of us manually take the input from the consumer and create the content to post.
- This reduces the technical need for a minimum viable product, letting us get something to consumers faster.
- Edit photos, adding text and filters to make it look nice
## Functional Requirements
- Content *generation* abilities
    - The website should have the ability to generate AI images for video thumbnails [S]
    - The website could have the ability to generate AI video content [C]
    - The website could have the ability to generate descriptions and a title of user uploaded videos [C]
- Customize options (things like description, title, when it'll post...etc)
    - The website must have the ability to edit the description, title
- Languages, API's, frameworks
    - Backend:
        - Language: Python
        - Framework: Flask
        - 'Dependancy manager': Python + Docker
        - API's: Instagram API, Facebook API, YouTube API
- SEO tools?
## Non-functional
- [Accessability](https://www.w3.org/WAI/standards-guidelines/wcag/faq/#start)
    - The webiste *should* abide by the w3 accessability standards [S]
        - we'll do this if it actually becomes our Sandbox project
- Scalability
    - Raspberry PI for inital hosting, but we can move to either Firebase or AWS for scalable hosting
- Security
    - User creation and authentication must be implemented [M]
        - this'll be for the two different pages: the form and the success metrics
    - The website will need to store user data [M] - website should be clear about this and make it clear it's a feature
        - It will only ever send the data to the various social media API's
        - We will also be their media backup service, in case any of their videos get removed by YouTube or Instagram or something
    - The AI API's will need some of the user data [S] (this is a should since AI integration in general is a should)
        - The website should be clear on this point
    - Taking in user data is a **BIG** security risk
        - The website *should* implement security measures to protect against any malicious code uploaded instead of regular videos or photos. 
            - Sanitize inputs
            - This should mostly be handled by Flask and its various extensions
    - The website could have OAuth authentication though Meta or Google accounts to sign in
        - Flask-OAuth/OAuth2 (they're now the same name for the extension) could be used for this
## Risks
- Copywrite
- Malicious content sent to the server via the form
    - Should be handled by Flask