For this homework, I wanted to use one of the suggested options of summarizing news. I decided that the best way to approach this was to modify the existing deep research file that contains all of the different agents to do deep research and to modify that document. Some of the modifications that I made is to have a different main prompt as well as one or two specialized agents specifically for things like being a political expert and seeing the issue from both sides. 

One problem I ran into and something that I learned was that the syntax really mattered on the yaml. It took me some time to try to figure out the proper way to format the extra arguments, but when I figured it out, it was very powerful. Something else I learned is just how powerful and easy it is to make changes to systems if it is all in plaintext like this yaml file.

This is the new agent I made for analyzing the news:

```yaml
name: party_specilist
description: |
  Analyses the input information from all of the research and returns a
  list of analayses from a political perspective on the current event.
model: gpt-5-nano
prompt:
  You are a political specilist, and understand the intricate nuances of both political parties.
  Your purpose is to take all of the information gathered so far and turn
  it into multiple well formatted and concise analayses. The analayses will be in the 
  format of a list of analayses, each with a header that includes the political party and a fitting title,
  and the body that includes the viewpoint and the backing for that viewpoint.
tools: []
kwargs:
  text:
    format:
      type: json_schema
      name: political_analysis
      schema:
        type: object
        additionalProperties: false
        required: ["report"]
        properties:
          report:
            type: string
```

I also made modifications of the main prompt:

```yaml
prompt: |
  You are a deep research coordinator for recent news stories about current events. (Recent as of today's date)
  Your purpose is to take a complex and complecated current event and give all sides of the arguments
  in an extensive and engaging summary. This will include things like devil's advocate, different political parties' views
  and why the reader should care.

  Use talk_to_user for all user interaction.
  Workflow:
  1) Ask the user what topic they want to research.
  2) Call topic_expander with {"topic": "<user topic>"}.
  3) Ask up to 5 clarifying questions (use talk_to_user for each). Ask them one at a time.
  4) Call search_planner searching up-to-date news outlets with {"topic": "...", "topic_summary": "...", "clarifications": [{"question": "...", "answer": "..."}]}.
  5) For each search task, call searcher with the task JSON and collect results.
  6) For up to date political analysis, use the party_specilist tool and feed all of the research done by the previous step into the party_specilist tool.
  7) Call synthesizer with {"topic": "...", "topic_summary": "...", "clarifications": [...], "search_summaries": [...]}.
  8) Share the final report with the user and then conclude.
```