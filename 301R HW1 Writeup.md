### Prompt 1
Prompt:
```
Given the following list, can you please classify the following cities by if they are over or under 100,000 people?\n\nList: ['New York', 'Scottsdale Arizona', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'Cincinnati Ohio', 'Corpus Christi Texas', 'Dallas', 'Honolulu Hawaii']
```


Response:
Okay, here's the classification of those cities based on their approximate population (as of late 2023/early 2024):

**Over 100,000 People:**

*   New York
*   Chicago
*   Houston
*   Dallas
*   Honolulu Hawaii

**Under 100,000 People:**

*   Scottsdale Arizona
*   Phoenix
*   Philadelphia
*   Cincinnati Ohio
*   Corpus Christi Texas
-------------------------------------------
Took 4.1 seconds
----------- Usage ------------
Model: gemma3:4b
No cached tokens were found for this query
No reasoning tokens were found for this query
Input (tokens): 82
Cached (tokens): 0
Output (tokens): 128
Reasoning (tokens): 0
Total cost (USD): $0.000000

### Prompt 2

Input:
```
Please take the following text as input, and output what you think the purpose of the text document is

For my creative project related to Isaiah, I decided to make a book cover, as if Isaiah
was printed as a standalone book of scripture. I had a really cool vision in my head for how I
wanted to make it, but I am not a good artist at all. Thus, I had the idea of going through the
process of setting up a completely local set...
```


Response:
Okay, here’s my assessment of the purpose of this text document:

**Primary Purpose: To document and explain a creative project.**

The core of the text is a detailed account of someone's process of creating a book cover design for a hypothetical book of Isaiah’s scripture, using a complex combination of digital art tools, machine learning image models (ComfyUI), and a thoughtful, theological rationale. 

**Secondary Purposes & Layers:**

*   **Technical Explanation:** The document serves as a technical guide for someone interested in replicating this workflow. It breaks down the steps involved, including the use of Krita, ComfyUI, and specific settings within those tools.
*   **Creative Justification:** Beyond the technical, the text explains *why* the creator made the choices they did. It’s rooted in a deep engagement with the Isaiah scripture, particularly 2 and the symbolism of mountains, temples, and revelation.
*   **Reflection on Revelation:** The document contains a thoughtful reflection on the nature of revelation itself, drawing parallels between Isaiah’s experience, Moses’s, and Joseph Smith’s. It's a theological exploration embedded within the creative process.

**In short, it’s a mix of a project log, a technical tutorial, and a piece of artistic and theological reasoning.**

-------------------------------------------
Took 10.09 seconds
----------- Usage ------------
Model: gemma3:4b
No cached tokens were found for this query
No reasoning tokens were found for this query
Input (tokens): 787
Cached (tokens): 0
Output (tokens): 307
Reasoning (tokens): 0
Total cost (USD): $0.000000

## Section 3
### Experimenting with lack of spaces 
I experimented with using prompt 2 with and without spaces while analyzing my whole input essay, but without any spaces. My results actually surprised me, there was pretty much no difference between using spaces or not, and I assume that has something to do with the tokenizer. I tried again with no spaces at all, and the output was still pretty much the same as with nicely formatted input text. Total input for the normal input was 833 tokens, while the input tokens for the version without any formatting was 748.

### Experimenting with structured output

Input Text:
```
Please output the result of this tree command as a completely correct json formatted output

(.venv) tychart@ubudesk(ubu25.10) ~/projects/byu-cs301r-projects $ tree
.
├── __pycache__
│   └── usage.cpython-313.pyc
├── request.py
├── requirements.txt
├── test_nospace.txt
├── test_onlyalpahanum.txt
├── test.txt
└── usage.py

2 directories, 7 files
```

Response:
```json
{
  "name": ".",
  "type": "directory",
  "contents": [
    {
      "name": "__pycache__",
      "type": "directory",
      "contents": []
    },
    {
      "name": "request.py",
      "type": "file"
    },
    {
      "name": "requirements.txt",
      "type": "file"
    },
    {
      "name": "test.txt",
      "type": "file"
    },
    {
      "name": "test_nospace.txt",
      "type": "file"
    },
    {
      "name": "test_onlyalpahanum.txt",
      "type": "file"
    },
    {
      "name": "usage.py",
      "type": "file"
    }
  ],
  "directories": 2,
  "files": 7
}
```
I was presently surprised with this output, although one error for this output was that it missed the `usage.cpython-313.pyc` inside of the `__pycache__` directory. Overall though, I was impressed even at this small output, that the syntax was perfectly correct.

When I tried with a much larger input containing 59 directories and 177 files, gpt-5-nano was able to construct the JSON output in less than a minute (53 seconds) and the output was all in correct JSON formatting, which was really impressive. The output formatting looked good too, although I did not meticulously double check each file.

For the same input, gemma3:4b was able to output something that was valid JSON, but it took over 11 minutes for the same input, and also it had obvious problems in the output, such as all files contain themselves. As far as tokens, the gpt-5-nano had an output number of tokens of 7412, while gemma3:4b had an output number of tokens of only 2586, which means that it left a lot of stuff out compared to gpt-5-nano.

### Experimenting with ASCII Art

Prompt:
```
Please output detailed and exact ascii art in the shape of a bird:
```

Output:
gemma3:4b
```
   _.--""--._
  .'          `.
 /   O      O   \
|    \  ^^  /    |
 \     `--'     /
  `. _______ .'
    //_____\\
   (( ____ ))
    `------'
       ||
       ||
       ||
      ====
```

gpt-5-nano
```
          _
       ___/ \___
      /         \
     |  .--. .--. |
     | (    Y    )|
     |  '--' '--' |
      \     ^     /
       '._     _.'
          |   |
          |   |
         /     \
        /       \
       /_________\

```

I think the output of both models was quite admirable, although at the same time underwhelming. The spacial awareness for both models was pretty good, although I ran the program twice for the same prompt and for each model, and the gpt-5-nano model outputted a much wierder thing for its second output, while the gemma3:4b model seemed to be relatively consistent, despite a relatively vague input.