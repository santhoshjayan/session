import datetime
import asana # type: ignore
from asana.rest import ApiException # type: ignore
import spacy # type: ignore
from spacy.matcher import Matcher # type: ignore
import requests # type: ignore

# https://chatgpt.com/g/g-p-67c8044ed4c88191bc5327fedd8d6a00-asana-auto/project
# https://developers.asana.com/docs/rate-limits
# https://developers.asana.com/reference/ac-api-reference


JOB_KEYWORDS = {"application", "resume", "cv", "job", "position", "hiring",
    "role", "opportunity", "career", "internship", "cover letter",
    "vacancy", "employment", "applicant"}
        
nlp = spacy.load("en_core_web_trf")

ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [{"label": "PERSON", "pattern": "Elon Musk"}, {"label": "PERSON", "pattern": "Sundar Pichai"}]
ruler.add_patterns(patterns)

def isEmailJunk(text):
    doc = nlp(text.lower())
    if not text or text.strip() == "":
        return True
    
    if any(word in doc.text for word in JOB_KEYWORDS):
        return False

    for ent in doc.ents:
        if ent.label_ in ["WORK_OF_ART", "ORG", "PERSON", "GPE"]: 
            return False
        
    return True

def getExp(text):
    doc = nlp(text)

    # Initialize Matcher
    matcher = Matcher(nlp.vocab)

    # Define patterns to extract experience
    patterns = [
        [{"LIKE_NUM": True}, {"LOWER": "years"}, {"LOWER": "of"}, {"LOWER": "experience"}],
        [{"LOWER": "over"}, {"LIKE_NUM": True}, {"LOWER": "years"}, {"LOWER": "of"}, {"LOWER": "experience"}],
        [{"LOWER": "more"}, {"LOWER": "than"}, {"LIKE_NUM": True}, {"LOWER": "years"}, {"LOWER": "of"}, {"LOWER": "experience"}],
        [{"LOWER": "worked"}, {"LOWER": "for"}, {"LIKE_NUM": True}, {"LOWER": "years"}],
    ]

    matcher.add("EXPERIENCE", patterns)
    matches = matcher(doc)

    # Extract years of experience
    experience_years = []
    for match_id, start, end in matches:
        span = doc[start:end]
        for token in span:
            if token.like_num:  # Extract numerical value
                experience_years.append(int(token.text))

    # Return the most relevant number (maximum found)
    return max(experience_years) if experience_years else 0

def has_capitalized_word(text):
    return any(word[0].isupper() for word in text.split())

def extract_full_names(text):
    doc = nlp(text)
    person_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    person_names = [name for name in person_names if not any(char.isdigit() for char in name)]
    capitalized_names = [name for name in person_names if has_capitalized_word(name)]
    if capitalized_names:
        selected_name = max(capitalized_names, key=len)
    elif person_names:
        selected_name = max(person_names, key=len)
    else:
        selected_name = None
    return selected_name

def runAsanaAuto():
    try:
        configuration = asana.Configuration()
        configuration.access_token = '2/1201115461147878/1209482972314437:94f540ea264756e93c33989ed929fd56'
        api_client = asana.ApiClient(configuration)

        # create an instance of the API class
        tasks_api_instance = asana.TasksApi(api_client)

        inbox_section_gid = "1205422475150782"
        opts = {
            'limit': 50, # int | Results per page. The number of objects to return per page. The value must be between 1 and 100.
            'opt_fields': "name, notes"
        }
        
        # Get tasks from a section
        print(f"Start processing... {datetime.datetime.now()}")
        task_api_response = tasks_api_instance.get_tasks_for_section(inbox_section_gid, opts)
        sections_api_instance = asana.SectionsApi(api_client)
        stories_api_instance = asana.StoriesApi(api_client)
        task_api_instance = asana.TasksApi(api_client)

        for data in task_api_response:
            gid =  data['gid']
            subject =  data['name']
            notes =  data['notes']
            isJunk = False;
            if subject and notes:
                print(f"Subject: {subject}")
                text = f"{subject} - {notes}"
                isJunk = isEmailJunk(text);  
                all_story_text = ""
                if isJunk:
                    stories_api_response = stories_api_instance.get_stories_for_task(gid, { 'limit': 3, 'opt_fields': "text" })
                    for story in stories_api_response:
                        story_text = story["text"];
                        all_story_text += story_text
                        isJunk = isEmailJunk(story_text)
                if not isJunk:
                    data = {};
                    custom_fields = { }
                    name = extract_full_names(text)
                    if name: 
                        data["name"] = name
                        print(f"\t Name Detected: {name}")
                    
                    exp = getExp(subject + notes + all_story_text)
                    if exp > 0:
                        print(f"\t Experience: {exp}")
                        custom_fields["1206480724577791"] = exp
                        
                    response = requests.get(f"https://api.genderize.io?name={name}")
                    if response.status_code == 200:
                        genderData = response.json()
                        custom_fields["1209296260341629"] = "1209296260341630" if genderData["gender"] == "male" else '1209296260341631'
                    
                    data["custom_fields"] = custom_fields
                    body = { "data": data }
                    task_api_instance.update_task(body, gid, { })

                target_section_gid =  "1209569401448149" if isJunk else "1209628150738132"
                opts = {'body': {"data": {"task": gid}} }
                sections_api_instance.add_task_for_section(target_section_gid, opts)
                print(f"Junk" if isJunk else "")
                print("\n")    
            
        return "Success";
    except ApiException as e:
        print("Exception: %s\n" % e)

    
runAsanaAuto();
