from toolbot import get_talk_text

import json


# out:str = get_gc_speaker_talk_index("dieter-f-uchtdorf")

# parsed = json.loads(out)
# pretty = json.dumps(parsed, indent=4)


# print("================================================================================")
# print(pretty)

out = get_talk_text('https://www.churchofjesuschrist.org/study/general-conference/2021/10/35wilcox?lang=eng')

print(out)