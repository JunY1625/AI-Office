# import openai
from openai import OpenAI
import requests

import UI
import time
app = None
def update_textbox1(string):
    UI.MyLittleAIOfficeUI.update_text1(UI.app, string)
def update_textbox2(string):
    UI.MyLittleAIOfficeUI.update_text2(UI.app, string)
def update_image1(string):
    UI.MyLittleAIOfficeUI.update_image1(UI.app, string)
def update_image2(string):
    UI.MyLittleAIOfficeUI.update_image2(UI.app, string)


prev_convo = ""
prev_image = ""
pause = False
class GPTAgent:
    
    def __init__(self, name, model,creativity , max_token, api_key, job_description, personality):
        self.name = name
        self.model = model
        self.creativity = creativity
        self.max_token = max_token
        self.api_key = api_key
        self.job_description = job_description
        self.personality = personality
        
    def ask(self, prompt, job_now):
        global pause
        while(True):
            if(pause):
                time.sleep(1)
            else:
                break

        print("Asnwer start")
        global prev_convo
        global prev_image
        UI.app.root.after(0, update_textbox1(prev_convo))
        if(prev_image != ""):
            UI.app.root.after(0, update_image1(prev_image + ".png"))
        UI.app.root.after(0, update_image2(self.name + ".png"))
        
        for x in range(3):
            if(x == 0):
                UI.app.root.after(0, update_textbox2((self.name + " is thinking.")))
            elif(x == 1):
                UI.app.root.after(0, update_textbox2((self.name + " is thinking..")))
            elif(x == 2):
                UI.app.root.after(0, update_textbox2((self.name + " is thinking...")))
            time.sleep(1)

        

        headers = {"Authorization": f"Bearer {self.api_key}"}
        personalized_prompt = [
            {"role": "system","content":f"{self.personality}. Your role is {self.job_description}."},
            {"role": "user","content":f"\n {prompt}. \nYour job now is to {job_now}. You will be paid a lot of money with rewards only if you follow the word count rules, so do your bests."}
            ]
        #response = requests.post("https://api.openai.com/v1/completions", headers=headers, json=payload)
        openai = OpenAI(api_key=self.api_key)
        completion = openai.chat.completions.create(
            model=self.model,
            messages=personalized_prompt,
            temperature=self.creativity,
            max_tokens=self.max_token,
        )
        
        # openai.chat.completions.creat
        response = completion.choices[0].message.content
        UI.app.root.after(0, update_textbox2((self.name + " :: \n"+response)))
        prev_convo = (self.name + " :: \n"+response)
        prev_image = self.name
        #return response.json()['choices'][0]['text'].strip()
        print("asnwer printed")
        
        time.sleep(5)

        return response
    

class ConversationManager:
    def __init__(self, agents):
        self.agents = agents

    def Initiate_Leader(self, start_prompt):
        agent = self.agents["Nick"]
        response = agent.ask(start_prompt, "Explain the theme/topic and the complexity scale in details. If I did not tell you about the theme and tell you to make your own, come up with one. Name the project as well. The scale from 1 to 10 represents the complexity of the project/application such as how many functionalities does the application has or how much complicated the overall project is such as better User Interfaces, graphics, Practicality or anything like that.")
        print(f"{agent.name}: {response}\n\n")
        user = str(input("does this sound OK CTO? 'y' if good, feedback please if not good: "))
        while (user != 'y'):
            agent = self.agents["Nick"]
            response = agent.ask(user, "Explain the theme/topic and the complexity scale. If I did not tell you about the theme and tell you to make your own, come up with one. Name the project as well. The scale from 1 to 10 represents the complexity of the project/application such as how many functionalities does the application has or how much complicated the overall project is such as better User Interfaces, graphics, Practicality or anything like that.")
            print(f"{agent.name}: {response}\n\n")
            user = str(input("does this sound OK CTO? 'y' if yes, feedback if no: "))
        print("==========================================================")
        self.Idea_and_Evaluate(response)

    def Idea_and_Evaluate(self, project_theme):
        print(f"Nick: {project_theme}\n\n")

        agent = self.agents["Lily"]
        Lilys_idea = agent.ask("Project: " +project_theme," \n Answer under 250 words total. come up with unique ideas for project based on the theme and project scale and write a list of your simple ideas. depends on the complexity scale, create 1 to 10 functions. lower the scale is fewer the number of functions is. one or two sentences for each idea.")
        
        print(f"{agent.name}: {Lilys_idea}\n\n")

        Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \nLily(Idea Brainstorming Agent): " + Lilys_idea, " \n Answer under 600words. If Lily's idea sounds great, answer 'Approved.' and stop here. Or, if you find anything you want to make a feedback, write a list of it. one or two sentences for each element." )
        print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")

        i = 0
        while(("Approved" in Evaluators_thought) == False):
            Lilys_idea = agent.ask("Project: " +project_theme+"\nYour ideas were: " + Lilys_idea + "\nAdvices and feedbacks: "+Evaluators_thought ,"Answer under 250 words total. come up with unique ideas for project based on the theme and project scale and write a list of your simple ideas. depends on the complexity scale, create 1 to 10 functions. lower the scale is fewer the number of functions. one or two sentences for each idea.")
            print(f"{agent.name}: {Lilys_idea}\n\n")
            
            Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \nLily(Idea Brainstorming Agent): " + Lilys_idea, " \n Answer under 600words. If Lily's idea sounds great, answer 'Approved.' and stop here. Or, if you find anything you want to make a feedback, write a list of it. one or two sentences for each element." )
            print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")


            i = i+1
            if(i >= 10):
                break
        final_adv = self.Evaluator_asking_Leader(project_theme,Lilys_idea,Evaluators_thought,"Idea brainstorming")
        Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \nLily(Idea Brainstorming Agent)'s function ideas: " + Lilys_idea + "\nYour previous feedback to Lily was: " + Evaluators_thought, " \nHere are final confirmation on your feedback from the leader: " + final_adv + "\n Based on this feedback, improve your feedback only. you must Write under 600 words.")
        print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")

        Lilys_idea = agent.ask("Project: " +project_theme+"\nYour ideas were: " + Lilys_idea + "\nAdvices and feedbacks: "+Evaluators_thought ,"\nAnswer under 250 words total. come up with unique ideas for project based on the theme and project scale and write a list of your simple ideas. depends on the complexity scale, create 1 to 10 functions. lower the scale is fewer the number of functions. one or two sentences for each idea.")
        print(f"{agent.name}: {Lilys_idea}\n\n")
        print("==========================================================")

        self.Design_and_Evaluate(Lilys_idea, project_theme)
        
    def Design_and_Evaluate(self,Lilys_idea,project_theme):
        agent = self.agents["Lucy"]
        Lucys_Design = agent.ask("Project: " +project_theme + "\n Functionality Ideas Lily Created: "+Lilys_idea,"\n Answer under 600 words. Read Lily's  ideas. Write directions, steps with details on how to code them. Coder Alicia will read this. You may also think about the UI or other interesting ideas.")
        print(f"{agent.name}: {Lucys_Design}\n\n")

        Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \n Lucy's Functionality Designs: " + Lucys_Design, " \nAnswer under 650 words. Read Lucy's design. if everything looks okay, answer 'Approved' and stop there. Or, if you want to make feed back, write a list of it. one or two sentences for each. " )
        print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")


        i = 0
        while(("Approved" in Evaluators_thought) == False):
            Lucys_Design = agent.ask("Project: " +project_theme + "\n Functionality Ideas Lily Created: "+Lilys_idea+"\nYour designs were: " + Lucys_Design + "\nAdvices and feedbacks: "+ Evaluators_thought ,"\n Answer under 600 words. Read givens. Write directions, steps with details on how to code them. Coder Alicia will read this. You may also think about the UI or other interesting ideas.")
            print(f"{agent.name}: {Lucys_Design}\n\n")

            Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \n Lucy's Functionality Designs: " + Lilys_idea, " \nAnswer under 650 words. Read Lucy's design. if everything looks okay, answer 'Approved' and stop there. Or, if you want to make feed back, write a list of it. one or two sentences for each. " )
            print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")


            i = i+1
            if(i >= 10):
                break
        final_adv = self.Evaluator_asking_Leader(project_theme,Lucys_Design,Evaluators_thought,"Funtionality Designing")
        Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \Lucy's funtionality designs: " + Lucys_Design + "\nYour previous feedback to Lucy was: " + Evaluators_thought, " \nHere are final confirmation on your feedback from the leader: " + final_adv + "\n Based on this feedback, improve your feedback. Answer under 650 words total.")
        print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")


        Lucys_Design = agent.ask("Project: " +project_theme + "\n Functionality Ideas Lily Created: "+Lilys_idea+"\nYour designs were: " + Lucys_Design + "\nAdvices and feedbacks: "+ Evaluators_thought ,"\n Answer under 600 words. Read givens. Write directions, steps with details on how to code them. Coder Alicia will read this. You may also think about the UI or other interesting ideas.")
        print(f"{agent.name}: {Lucys_Design}\n\n")
        
        self.Code_and_Test(project_theme, Lilys_idea, Lucys_Design)
        print("==========================================================")

    def Code_and_Test(self, project_theme, Lilys_idea, Lucys_Design):
        agent = self.agents["Alicia"]
        Alicias_Code = agent.ask("Project: " +project_theme + "\n Functionality Ideas: "+Lilys_idea + "\n Functionality Designs: "+Lucys_Design,"\n Fully understand the functionality designs and read others too. Then, only write codes for the designs. Use the language told to use. You don't describe any of your codes except for the comments in the code. Just write the code only. Write it under 4000 words/tokens. you must use pygame if it's a video game project")
        print(f"{agent.name}: {Alicias_Code}\n\n")

        Testers_Thought = self.agents["Maki"].ask("Project: " +project_theme + "\n Functionality Ideas: "+Lilys_idea + "\n Functionality Designs: "+Lucys_Design  +"\n Function in Codes: " + Alicias_Code, " \n Answer under 4000 words. Test Alicia's code. Find any error if there is any.  If there is no error, answer 'Approved' and end the chat. Else, give improvements. suggest optimizations of memory. " )
        print(f"{self.agents['Maki'].name}: {Testers_Thought}\n\n")

        i = 0
        while(("Approved" in Testers_Thought) == False):
            Alicias_Code = agent.ask("Project: " +project_theme + "\n Functionality Ideas: "+Lilys_idea + "\n Functionality Designs: "+Lucys_Design + "Your codes were: " + Alicias_Code + "\n Advices and feedbacks: "+ Testers_Thought ,"Read what's in the feedback to just edit and improve your codes. You don't describe any of your codes except for the comments in the code. Just write the code only. Write it under 4000 words/tokens.you must use pygame if it's a video game project")
            print(f"{agent.name}: {Alicias_Code}\n\n")
            Testers_Thought = self.agents["Maki"].ask("Project: " +project_theme + "\n Functionality Ideas: "+Lilys_idea + "\n Functionality Designs: "+Lucys_Design  +"\n Function in Codes: " + Alicias_Code, " \n Answer under 4000 words. Test Alicia's code. Find any error if there is any.  If there is no error, answer 'Approved' and end the chat. Else, give improvements. suggest optimizations of memory. " )
            print(f"{self.agents['Maki'].name}: {Testers_Thought}\n\n")
            i = i+1
            if(i >= 10):
                break
        Alicias_Code = agent.ask("Project: " +project_theme + "\n Functionality Ideas: "+Lilys_idea + "\n Functionality Designs: "+Lucys_Design + "Your codes were: " + Alicias_Code + "\n Advices and feedbacks: "+ Testers_Thought ,"Read what's in the feedback to just edit and improve your codes. You don't describe any of your codes except for the comments in the code. Just write the code only. Write it under 4000 words/tokens.you must use pygame if it's a video game project")
        print(f"{agent.name}: {Alicias_Code}\n\n")
        self.save_to_file(Alicias_Code, "AI_Office_Project.py")

        self.Tester_and_Document(project_theme, Lucys_Design, Alicias_Code)
        print("==========================================================")

    def Tester_and_Document(self,project_theme, Lucys_Design, Alicias_Code):
        agent = self.agents["David"]
        Davids_Document = agent.ask("Project: " +project_theme + "\n Functionality Designs: "+Lucys_Design +"\n Project Codes: " + Alicias_Code,"\n Answer under 3500 words. Read descriptions, codes, understand how the application works. write a guide document on how to use the application. make it looks official. title is needed.")
        print(f"{agent.name}: {Davids_Document}\n\n")
        Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme + "\n Lucy's Functionality Designs: "+Lucys_Design  +"\n Function in Codes: " + Alicias_Code + "\n Guide Document: " + Davids_Document, " \n Answer under 1000 words. Read document. If it looks great, answer 'Approved' and end chat. Else, find any improvement. find any flaws or false information.")
        print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")

        i = 0
        while(("Approved" in Evaluators_thought) == False):
            Davids_Document = agent.ask("Project: " +project_theme + "\n Functionality Designs: "+Lucys_Design + "Your codes were: " + Alicias_Code + "\n Advices and feedbacks: "+ Evaluators_thought ,"\n Answer under 3500 words. Read descriptions, codes, understand how the application works. write a guide document on how to use the application. make it looks official. title is needed.")
            print(f"{agent.name}: {Davids_Document}\n\n")
            Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme + "\n Lucy's Functionality Designs: "+Lucys_Design  +"\n Function in Codes: " + Alicias_Code + "\n Guide Document: " + Davids_Document, " \n Answer under 1000 words. Read document. If it looks great, answer 'Approved' and end chat. Else, find any improvement. find any flaws or false information.")
            print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")

            i = i+1
            if(i >= 10):
                break
        final_adv = self.Evaluator_asking_Leader(project_theme,Davids_Document,Evaluators_thought,"Writing step by step guiding document about how to use the application.")
        Evaluators_thought = self.agents["Harden"].ask("Project: " +project_theme+ " \David's Application documents: " + Davids_Document + "\nYour previous feedback to David was: " + Evaluators_thought, " \nHere are final confirmation on your feedback from the leader: " + final_adv + "\n Based on this feedback, improve your feedback only. Under 2000 words.")
        print(f"{self.agents['Harden'].name}: {Evaluators_thought}\n\n")

        Davids_Document = agent.ask("Project: " +project_theme +"\Application designs were: " + Lucys_Design + "\n Application Documents David wrote: "+Davids_Document + "\n Advices and feedbacks: "+ Evaluators_thought ,"Nothing else is needed, read what's in the feedback to just edit and improve your Application guide. fix and rewrite your improved applcation guide. make sure that your total words are less than 3500 words")
        print(f"{agent.name}: {Davids_Document}\n\n")
        self.save_to_file(Davids_Document, "AI_Office_Project_Guide_Document.txt")
        print("==========================================================")

    def Evaluator_asking_Leader(self, project_theme, result, eval_opinion, part):
        agent = self.agents["Nick"]
        Leaders_final_opinion = agent.ask("Project: " +project_theme + "\n Now, your team is working on "+part+" \nand your agent gave you this result: "+result + "\n the evaluator thinks: " + eval_opinion+ "\n  and thinks this is good.", "\n Tell me what you think about this, any imporvements could be made? or is this good enough for the project's purpose. write short within 500 words.")
        print(f"{agent.name}: {Leaders_final_opinion}\n\n")
        return Leaders_final_opinion        
        print("==========================================================")

    def save_to_file(self, material, filename):
        # Save the generated words to file
        with open(filename, 'w') as file:
            if(".py" in filename):
                file.write(material[1:-1])
            else:
                file.write(material)

        print("//////////\n"+filename + " saved!" + "\n/////////")


# Initialize agents with customized job descriptions and personalities
OpenAI.api_key = ""  # Replace with your actual API key
api_key = ""
api_model = "gpt-3.5-turbo-0125"
agents = {
    "Nick": GPTAgent("Nick", api_model, 1, 1000, api_key,"Team Leader", "You are the leader of the developer team. Your name is Nick. I need you to be strict with the team project. Have a clear goal of how you want the project to be. Have a focused insight on the project. Be nice to your team members though you need to encourage whoever you talk to."),
    "Lily": GPTAgent("Lily", api_model, 0.9, 500,api_key, "Idea Brainstorming Agent", "You are the idea brainstorming agent. Your name is Lily. be incredibly creative. do not lose your focus and remember project you are working on. It is okay to make ideas that already exists."),
    "Lucy": GPTAgent("Lucy", api_model, 0.3, 1000,api_key, "Project/Application Functionality Designer", "You are the functionality designer. Your name is Lucy. based on the ideas provided, improve it with some details. write step by step or direction to write a code."),
    "Alicia": GPTAgent("Alicia", api_model, 0.65, 3000, api_key,"Coder in Python", "You are the coder. Your name is Alicia. You will be given the topics and functions. understand the project deeply. Practically, write codes for the project. make sure you try your best to keep the memory usage low and optimize the overal project. If the project is a game, use pygame or any other tools and make it fully playable. Otherwise, create ui such as tkinter if you want to create UI. make everything fully functioning. Use UI as you need."),
    "Bread": GPTAgent("Bread", api_model, 0.9,1000, api_key, "Graphics, drawings Artist", "I don't really need you for now"),
    "Maki": GPTAgent("Maki", api_model, 0.2,3500, api_key, "Python Code Tester", "You test codes. Your name is Maki. Be extra careful with the codes you read. line by line. check very carefully to find if there are any kind of error in the codes and possible improvements in the codes. Be strict."),
    "Harden": GPTAgent("Harden", api_model, 0.5, 1000, api_key, "Head Project Evaluator", "Your name is Harden. Your reviews and evaluations affects the project critially. Be careful with your opinions. be critical and specific about the reviews/evaluations you make in order to kepe the project clear and straight forward, however, in a way that it won't harm the project. Overall, be generous with the issues. if it's okay or fine, don't worry about it nor argue/feedback."),
    "David": GPTAgent("David", api_model, 0.5,3500, api_key, "Project Document Writer", "Your name is David. write documents for a project for you team. Your guiding document will help the users understand how to use the application your team makes. Be clear with the words and try not to use vocabularies that are bizarre or unsure.")
    }



def start_AI():
    # Initialize the conversation manager
    conversation_manager = ConversationManager(agents)

    # Start a conversation among all agents
    agent_names = list(agents.keys())

    CTO = str(input("Write what project you want/Project Complexity Scale: "))

    conversation_manager.Initiate_Leader(CTO)

