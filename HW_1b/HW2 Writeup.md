I did some experimenting with breaking up the prompt into 3 sections, up from the previous two. This segmented prompt consisted of 1) A generic text prompt for proposing information about an item, such as wanting a simple list, or wanting a complex collection. 2) The actual item/object/word that the prompt is about. 3) A style or output format that had a specified output category, allowing the user to switch out formatting like JSON vs YAML without needing to modify the original prompt. This worked out pretty well for human readability, but as I was attaching the JSON interpreter/parser, I realized that the output format is almost entirely tied to the text prompt. It is pretty tough to have an exact and repeatable output prompt without  

I noticed that even with a very low powered model, gemma3:4b, the structured output was pretty solid. On the other hand, when I started having something much more subjective, a description of the song, I noticed quite a few differences

Older models do quite a bit worse with structured outputs, I also tested with JSON vs YAML, and JSON was much more reliable of an output compared to YAML.

