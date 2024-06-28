import os
import re
import shutil
from io import StringIO

from config import config


def find_user_compiler(uploaded_object):
    '''
    Return user compiler name from Streamlit UploadedFile object.
    '''
    user_compiler = ''

    if uploaded_object is not None:
        user_compiler = os.path.join(config['paths']['user_compiler'],
                                     uploaded_object.name)

    return user_compiler


def upload_user_compiler(uploaded_object):

    if uploaded_object is not None:

        save_as = find_user_compiler(uploaded_object)

        to_read = uploaded_object.getvalue()
        stringio = StringIO(to_read.decode('utf-8'))

        with open(save_as, 'w', encoding='utf-8') as f:
            f.write(stringio.read())


def sanitize_prompt(prompt_org):
    sanitized_prompt = re.sub(r'\s+', ' ', prompt_org)
    sanitized_prompt = sanitized_prompt.replace(r'\n', '')
    sanitized_prompt = sanitized_prompt.replace(r'\r', '')
    sanitized_prompt = sanitized_prompt.replace(' ', r'\u0020')
    return sanitized_prompt.strip()


def eligible_to_expand_domain(selected_compiler):
    '''
    Return if domain expansion option to add for given compiler
    '''
    ans = False

    buff = config['constants']['eligible_compilers_to_expand']
    list_eligible_compilers = buff.split('/')

    if selected_compiler in list_eligible_compilers:
        ans = True

    return ans


def delete_user_compiler(uploaded_object):
    '''
    Remove user compiler md file uploaded by user.
    '''
    user_compiler = find_user_compiler(uploaded_object)
    if os.path.exists(user_compiler):
        os.remove(user_compiler)


def find_requirement_file(source):
    '''
    Return file name of generated requirement from zoltraak stdout sentence.
    '''
    candidate_requirement = source.split(':')[1]
    candidate_requirement = candidate_requirement.split('.md')[0]
    candidate_requirement = candidate_requirement.replace(' ', '')
    candidate_requirement += '.md'
    return candidate_requirement


def find_code_path(generated_requirement):

    to_replace = config['constants']['prefix_requirement']

    project_name = os.path.split(generated_requirement)[-1]
    project_name = project_name.replace(to_replace, '')
    project_name = project_name.replace('.md', '')

    to_find = os.path.join(config['paths']['codes'], project_name)

    answer = to_find if os.path.isdir(to_find) else ''

    return answer


def generate_zip(generated_requirement, code_path):

    project_name = os.path.split(code_path)[-1]

    zip_location = config['paths']['zip']
    work_path = os.path.join(zip_location, project_name)
    save_as = work_path + '.zip'

    # Make a work folder
    if os.path.isdir(work_path):
        shutil.rmtree(work_path)

    if os.path.exists(save_as):
        os.remove(save_as)

    os.mkdir(work_path)

    # Copy files, then execute zip
    shutil.copy(generated_requirement, work_path)
    shutil.copytree(code_path,
                    os.path.join(work_path, config['paths']['codes']))

    shutil.make_archive(work_path, 'zip', root_dir=work_path)

    # Clean up work folder
    shutil.rmtree(work_path)

    return save_as
