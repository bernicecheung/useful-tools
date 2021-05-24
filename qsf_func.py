import json
from pprint import pprint

def open_qsf(f_name):
    '''
    (str) -> dict
    This function will load the qualtric file(f_name) as a json file and returns a dicitonary
    '''
    with open(f_name) as infile:
        data = json.load(infile)
    return data

def target_question(data, block_name):
    '''
    (dict, str) -> list
    This function will extract all the question IDs from the block(block_name) in the data file(data). It will be called by fucntion replace_content, and return a list of question IDs.
    '''
    # extract block information from the survey data file
    blocks = data["SurveyElements"][0]['Payload']

    # record all the question ID from the given block
    for b in blocks:
        if blocks[b]['Description'] == block_name:
            targetQ = []
            blockElement_list = blocks[b]['BlockElements']
            for q in blockElement_list:
                if q['Type'] == 'Question': 
                    targetQ.append(q['QuestionID'])
    return targetQ

def replace_content(data, block_name, elem_name, old_content, new_content):
    '''
    (qsf_data, str, str, str, str) -> qsf_data

    '''
    targetQ = target_question(data, block_name)
    for elem in data["SurveyElements"]:
        if elem['Element'] == 'SQ' and elem['Payload']['QuestionID'] in targetQ:
            elem['Payload'][elem_name] = elem['Payload'][elem_name].replace(old_content, new_content)
    return data

def create_newTags(total_n, prefix = '', suffix = '', start_n = 1):
    '''
    (str, str, int, int) -> list
    This function will create question export tags with consecutive numbers and prefix or suffix
    '''
    if prefix != '' and suffix != '':
        tag_list =  [prefix + str(n) + suffix for n in range(start_n, (start_n + total_n))]
    elif prefix != '':
        tag_list =  [prefix + str(n) for n in range(start_n, (start_n + total_n))]
    elif suffix != '':
        tag_list =  [str(n) + suffix for n in range(start_n, (start_n + total_n))]
    else:
        tag_list = [str(n) for n in range(start_n, (start_n + total_n))]
    return tag_list

def replace_defaultTags(data, block_name, new_tags):
    '''
    '''
    targetQ = target_question(data, block_name)
    if len(targetQ) != len(new_tags):
        raise ValueError('tags and the questions must have the same length')
    else:
        for elem in data["SurveyElements"]:
            if elem['Element'] == 'SQ' and elem['Payload']['QuestionID'] in targetQ:
                q_index = targetQ.index(elem['Payload']['QuestionID'])
                old_content = elem['Payload']['DataExportTag']
                new_content = new_tags[q_index]
                elem['Payload']['DataExportTag'] = elem['Payload']['DataExportTag'].replace(old_content, new_content)
    
    return data

def rename_survey(data, new_name):
    '''

    '''
    data['SurveyEntry']['SurveyName'] = new_name
    return data

def write_qsf(f_name, data):
    with open(f_name, 'w') as outfile:
        json.dump(data, outfile)
    return None
