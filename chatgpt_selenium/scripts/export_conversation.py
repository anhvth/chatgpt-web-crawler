from speedy_utils import *
path = "/Users/anhvth/Downloads/d7cf474a3acd425826704292bc5704c5f337b16632a4cf56d7ca2edd20948b6e-2025-04-25-15-54-57-8a5916cdfd0844ac83a373540142281b/conversations.json"

import json

def extract_messages(item):
    """
    Extracts a list of messages from a JSON item with the structure provided.
    Each message in the output list contains 'role' and 'content'.
    """
    mapping = item.get('mapping', {})
    messages = []

    def traverse(node_id):
        node = mapping.get(node_id, {})
        for child_id in node.get('children', []):
            child = mapping.get(child_id, {})
            msg = child.get('message')
            if msg:
                role = msg.get('author', {}).get('role')
                content_parts = msg.get('content', {}).get('parts', [])
                content = "".join(content_parts).strip()
                if role and content:
                    messages.append({'role': role, 'content': content})
            traverse(child_id)

    # Start traversal from the root
    traverse('client-created-root')
    return messages
def try_extract_messages(item):
    """
    Attempts to extract messages from a JSON item, returning None if extraction fails.
    """
    try:
        return extract_messages(item)
    except Exception as e:
        return None

data = load_by_ext(path)
list_messages = [try_extract_messages(item) for item in data]

user_start_with = "row_id,text_to_translate,glossary,translation"
def filter(messages):
    if messages is None:
        return False
    if len(messages) == 0:
        return False
    user_content = messages[0].get('content', '')
    return user_content.startswith(user_start_with)
        
    
list_messages = [msg for msg in list_messages if filter(msg)]
output_path = path.replace(".json", "_messages.json")
dump_json_or_pickle(list_messages, output_path)
print(f"Extracted messages saved to {output_path}, num of messages: {len(list_messages)}")