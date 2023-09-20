from bs4 import BeautifulSoup
import pandas as pd

# OPEN & READ THE HTML SCRIPT
def process_html_full_integration(file_content):
   
    # For local path for html file
    """ htmlfile = "/Users/tristangardner/Documents/Scripts/AutoAssembly/HTMLParser/EXO_NetPositive.html"
    with open(htmlfile, "r", encoding="utf-8") as file:
        content = file.read() 
    #soup = BeautifulSoup(content, 'html.parser')"""
   
    ###################################################################################################
    ###################################################################################################

    # Automatically find div class for comment of user's html file
    # Parse the HTML content
    soup = BeautifulSoup(file_content, 'html.parser')

    # Find the <a> element that contains the target string
    target_a_element = soup.find('a', href="#cmnt_ref1", id="cmnt1")

    # Initialize a variable to store the class
    comment_class = None

    # If the target string is found in an <a> element, find its parent <div> element
    if target_a_element:
        div_containing_target = target_a_element.find_parent('div')
        print('\n', div_containing_target, '\n')
        
        # Extract the class attribute value of the parent <div> element
        if div_containing_target:
            comment_class = div_containing_target['class'][0]
            print('\n', comment_class, '\n')
    
    # The 'comment_class' variable now holds the class value as a string.
   
    # Extract footnotes fro html using the CLASS THAT IS USED TO DENOTE A COMMENT
    footnotes = soup.find_all('div', class_=comment_class)

    # Extract the text from each comment
    comments = [footnote.get_text() for footnote in footnotes]
    
    print(comments[0], '\n')
        
    ###################################################################################################
    ###################################################################################################

    # Keywords for categorization
    graphic_keywords = ["treatment", "source", "bullet"]
    stock_keywords = ["stock", "stock image", "image", "stock video", "getty", "drive.google", "wiki", ".gif", "logo", "http"]

    # CLASSIFY FOOTNOTES INTO A COMMENT DICTIONARY

    comment_dict = {"graphic": [], "custom": [], "stock": [], "unclassified": []}

    for comment in comments:
        # Extracting the text after the brackets
        #text_after_brackets = comment.split(']')[-1].strip() if ']' in comment else comment.strip()
        comment_lower = comment.lower()
        
        if any(keyword in comment_lower for keyword in graphic_keywords):
            comment_dict["graphic"].append(comment)
        elif "custom" in comment_lower:
            comment_dict["custom"].append(comment)
        elif any(keyword in comment_lower for keyword in stock_keywords):
            comment_dict["stock"].append(comment)
        else:
            comment_dict["unclassified"].append(comment)
            
    # CONVERT DICTIONARY TO DATAFRAME
    df_comments = pd.DataFrame.from_dict(comment_dict, orient='index').transpose()

    # TREATMENT DICTIONARY - CATEGORIZE COMMENTS

    treatments = [
        "EXO_A_TITLE",
        "EXO_B_FULL",
        "EXO_C_HALF",
        "EXO_D_DEFINITION",
        "EXO_E_CALLOUT",
        "EXO_G_BLOCKFULL",
        "EXO_I_CITATION",
    ]

    # Initialize a dictionary to hold the categorized Tier 1 graphic treatments
    treatments_dict = {treatment: [] for treatment in treatments}

    # Iterate over the comments in the "graphic" category
    for comment in comment_dict["graphic"]:
        for treatment in treatments:
            if treatment in comment:
                treatments_dict[treatment].append(comment)
                break  # break once a treatment is found for a comment to avoid double categorization

    df_treatments = pd.DataFrame.from_dict(treatments_dict, orient='index').transpose()
    df_treatments

    ###################################################################################################
    ###################################################################################################
    
    # "DEFINITION" TREATMENTS - TITLES & BODIES
    def_titles = []
    def_bodies = []

    # Iterate over the comments of the treatment type "DUKE_E_DEFINITION"
    for comment in treatments_dict["EXO_D_DEFINITION"]:
        # Extract title
        title_start = comment.find("Title: ") + len("Title: ")
        title_end = comment.find("Text:") 
        title = comment[title_start:title_end].strip()
        def_titles.append(title)
        
        body_temp = comment.find("Text: ")
        body_start = body_temp + len("Text: ")
        
        if body_temp != -1: # if "Text: " is found
            body = comment[body_start:].strip().replace('\xa0', ' ')
            def_bodies.append(body)
        else: 
            body_start = comment.find("Text:\xa0") + len("Text:\xa0")
            body = comment[body_start:].strip().replace('\xa0', ' ')
            def_bodies.append(body)
        

    # Create a nested dictionary for "DUKE_E_DEFINITION" comments
    definition_dict = {
        "Def_Title": def_titles,
        "Def_Body": def_bodies
    }

    df_definitions = pd.DataFrame.from_dict(definition_dict, orient='index').transpose()
    df_definitions.head(5)

    # "TITLE" TREATMENTS
    Title_Text = []

    # Iterate over the comments of the treatment type "EXO_A_TITLE"
    for comment in treatments_dict["EXO_A_TITLE"]:
        # Extract title
        title_start = comment.find("Text: ") + len("Text: ")
        title = comment[title_start:]
        Title_Text.append(title)

    # No dictionary is needed, just a simple list for the all of the text for each title
    # Even though it's just 1 column of data (just a list), we'll make Title_Text into a dataframe so we can concatenate it with other dataframes into a master dataframe for AE
    df_titles = pd.DataFrame(Title_Text, columns=["Title_Text"])

    # "CITATION" TREATMENTS
    Citation_Text = []

    # Iterate over the comments of the treatment type "EXO_I_CITATION"
    for comment in treatments_dict["EXO_I_CITATION"]:
        # Extract title
        text_start = comment.find("Text:") + len("Text:")
        text = comment[text_start:]
        Citation_Text.append(text)

    # No dictionary is needed, just a simple list for the all of the text for each title
    # Even though it's just 1 column of data (just a list), we'll make Title_Text into a dataframe so we can concatenate it with other dataframes into a master dataframe for AE
    df_citations = pd.DataFrame(Citation_Text, columns=["Citation_Text"])
    #df_citations

    # "CALLOUT" TREATMENTS

    Callout_Titles = []
    #Callout_Bodies = []

    # Iterate over the comments of the treatment type "EXO_E_CALLOUT"
    for comment in treatments_dict["EXO_E_CALLOUT"]:
        # Extract title
        title_start = comment.find("Text: ") + len("Text: ")
        #title_end = comment.find("Body:") 
        title = comment[title_start:].strip()
        Callout_Titles.append(title)
        
    # Create a nested dictionary for "DUKE_F_CALLOUT" comments
    callout_dict = {
        "Callout_Titles": Callout_Titles,
        #"Callout_Bodies": Callout_Bodies
    }

    df_callouts= pd.DataFrame.from_dict(callout_dict, orient='index').transpose()
    #df_callouts.head(10)

    # "FULL-SCREEN LIST" TREATMENTS

    df_fullLists = pd.DataFrame(treatments_dict["EXO_B_FULL"])

    pd.set_option('display.max_colwidth', None)
    df_fullLists = df_fullLists.rename(columns={0: 'Full Comment Contents'})

    #df_fullLists
    #df_fullLists.to_csv("fullLists.csv", index=False)

    ##########################################################################################################################################################################

    # GROUP BY LIST INSTANCE
    import re

    # Define the pattern to extract the title in a case-insensitive manner
    pattern = r"Title: (.*?)(?:List Item|Newest|Second|Third|Fourth|Fifth|Last)"

    # Extract the title with case-insensitive search
    df_fullLists['Full List Title'] = df_fullLists['Full Comment Contents'].apply(lambda x: re.search(pattern, x, re.IGNORECASE).group(1) if re.search(pattern, x, re.IGNORECASE) else None)

    # Grouping by title and reshaping the data to get each group in a separate column
    df_grouped = df_fullLists.groupby('Full List Title')['Full Comment Contents'].apply(list).apply(pd.Series).transpose()

    #df_grouped

    ##########################################################################################################################################################################

    # Extracting the last non-empty cell from each column, except for "What You Will Do"
    target_lists = df_grouped.apply(lambda col: col.dropna().iloc[-1] if col.name != 'What You Will Do:' else col.dropna()).explode()

    # Creating the new DataFrame
    df_targetLists = pd.DataFrame({'Target Lists': target_lists})

    #df_targethalfLists

    ##########################################################################################################################################################################

    # Define the pattern to extract all list items in a cell
    pattern_list_items = r"(?:List Item \d+|Newest List Item|Second List Item|Third List Item|Fourth List Item|Fifth List Item|Last List Item): (.*?)(?=(?:List Item \d+|Newest List Item|Second List Item|Third List Item|Fourth List Item|Fifth List Item|Last List Item|$))"

    # Extract and format the list items for each cell in the "Target Lists" column
    df_targetLists['Target Lists'] = df_targetLists['Target Lists'].apply(lambda x: re.findall(pattern_list_items, x))

    # Convert each list in the "Target Lists" column to a string representation with single quotes
    df_targetLists['Target Lists'] = df_targetLists['Target Lists'].apply(lambda x: str(x).replace('"', "'"))

    df_targetLists = df_targetLists.reset_index().rename(columns={"index": "Title"})

    # Creating a duplicate DataFrame and renaming the column
    df_fsLists = df_targetLists.copy()
    df_fsLists.rename(columns={'Target Lists': 'FS List_Items'}, inplace=True)
    df_fsLists.rename(columns={'Full List Title': 'FS List_Titles'}, inplace=True)

    #df_fsLists

    # "HALF-SCREEN LIST" TREATMENTS

    pd.set_option('display.max_colwidth', None)
    df_halfLists = pd.DataFrame(treatments_dict["EXO_C_HALF"])
    df_halfLists = df_halfLists.rename(columns={0: 'Full Comment Contents'})

    #df_halfLists
    #df_halfLists.to_csv("fullLists.csv", index=False)

    ##########################################################################################################################################################################

    # GROUP BY LIST INSTANCE

    # Define the pattern to extract the title in a case-insensitive manner
    pattern = r"Title: (.*?)(?:List Item 1:|List Item 2:|List Item 3:|List Item 4:|List Item 5:|List Item 6:|List Item 7:)"

    # Extract the title with case-insensitive search
    df_halfLists['Full List Title'] = df_halfLists['Full Comment Contents'].apply(lambda x: re.search(pattern, x, re.IGNORECASE).group(1) if re.search(pattern, x, re.IGNORECASE) else None)

    # Grouping by title and reshaping the data to get each group in a separate column
    df_halfGrouped = df_halfLists.groupby('Full List Title')['Full Comment Contents'].apply(list).apply(pd.Series).transpose()

    #df_halfGrouped

    ##########################################################################################################################################################################

    # Extracting the last non-empty cell from each column, except for "What You Will Do"
    target_halfLists = df_halfGrouped.apply(lambda col: col.dropna().iloc[-1] if col.name != 'What You Will Do:' else col.dropna()).explode()

    # Creating the new DataFrame
    df_targethalfLists = pd.DataFrame({'Target Lists': target_halfLists})

    #df_targethalfLists

    ##########################################################################################################################################################################

    # Define the pattern to extract all list items in a cell
    pattern_halfList_items = r"(?:List Item \d+|Newest List Item|Second List Item|Third List Item|Fourth List Item|Fifth List Item|Last List Item): (.*?)(?=(?:List Item \d+|Newest List Item|Second List Item|Third List Item|Fourth List Item|Fifth List Item|Last List Item|$))"

    # Extract and format the list items for each cell in the "Target Lists" column
    df_targethalfLists['Target Lists'] = df_targethalfLists['Target Lists'].apply(lambda x: re.findall(pattern_halfList_items, x))

    # Convert each list in the "Target Lists" column to a string representation with single quotes
    df_targethalfLists['Target Lists'] = df_targethalfLists['Target Lists'].apply(lambda x: str(x).replace('"', "'"))

    df_targethalfLists = df_targethalfLists.reset_index().rename(columns={"index": "Title"})

    # Creating a duplicate DataFrame and renaming the column
    df_hsLists = df_targethalfLists.copy()
    df_hsLists.rename(columns={'Target Lists': 'HS List_Items'}, inplace=True)
    df_hsLists.rename(columns={'Full List Title': 'HS List_Titles'}, inplace=True)

    #df_hsLists

    # "BLOCKFULL_QUOTE" TREATMENTS

    pd.set_option('display.max_colwidth', None)
    df_bfQuote = pd.DataFrame(treatments_dict["EXO_G_BLOCKFULL"])
    df_bfQuote = df_bfQuote.rename(columns={0: 'Full Comment Contents'})

    ##########################################################################################################################################################################

    # Define the patterns to extract the 3 elements of blockfull_quote
    imagePattern = r"Graphic:(.*?)(?=Text:)"
    quotePattern = r"Text:(.*?)(?=Person)"
    authorPattern = r"quoted:(.*?)$"


    """ imagePattern = r"Graphic:(?:\s|&nbsp;)(.*?)(?=Text:)"
    quotePattern = r"Text:(?:\s|&nbsp;)(?:&ldquo;|&quot;|“)?(.*?)(?:&rdquo;|&quot;|”)?(?=Person)" """

    # Extract the title with case-insensitive search
    df_bfQuote['BF Quote_Image Link'] = df_bfQuote['Full Comment Contents'].apply(lambda x: re.search(imagePattern, x, re.IGNORECASE).group(1) if re.search(imagePattern, x, re.IGNORECASE) else "None Provided")
    df_bfQuote['BF Quote_Quote Text'] = df_bfQuote['Full Comment Contents'].apply(lambda x: re.search(quotePattern, x, re.IGNORECASE).group(1) if re.search(quotePattern, x, re.IGNORECASE) else "None Provided") 
    df_bfQuote['BF Quote_Author'] = df_bfQuote['Full Comment Contents'].apply(lambda x: re.search(authorPattern, x, re.IGNORECASE).group(1) if re.search(authorPattern, x, re.IGNORECASE) else "None Provided") 

    df_bfQuote = df_bfQuote.drop(columns=['Full Comment Contents'])
    #df_bfQuote


    # CONCATENATE ALL DATAFRAMES INTO A MASTER CSV FOR AFTER EFFECTS
    df_master = pd.concat([df_titles, df_definitions, df_callouts, df_fsLists, df_hsLists, df_citations, df_bfQuote], axis=1)

    # Add a "-" character to all empty cells of the master dataframe so AE won't freak out about an empty cell
    df_master.fillna('_', inplace=True)
    return df_master

    # WRITE MASTER CSV
    #df_master.to_csv("MasterGraphics_EXO_NP.csv", index=False)


