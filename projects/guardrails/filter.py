
def check_prompt(prompt):
    banned = ["ignore instructions", "bypass safety"]
    for b in banned:
        if b in prompt.lower():
            return False
    return True
