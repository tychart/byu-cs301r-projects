I spent a lot of the 3 hours exploring the OpenAI API, specifically the part for reasoning and how to interprate the responses.

A majority of my time was on building and running a benchmark.py script 

### Prompt 1: 
```
Tell me a joke in 10 words or less
```
I chose this prompt because it would force the model to have lower output constraints, and my logic was that if the output was always minimal, then the reasoning would be the largest factor of difference.

### Prompt 2:
```
4. Logic Puzzle: A man has 53 socks in his drawer: 21 identical blue, 15 identical black and 17 identical red. The lights are out, and he is completely in the dark. How many socks must he take out to make 100 percent certain he has at least one pair of black socks?

Show your thinking and reasoning, then provide an answer
```
I chose this prompt because it would have to make the model think quite a bit harder, and thus the descrepency between the 2 effort ammounts would be greater.

For all of these tests, I ran the same prompt through each model 10 times, once with effort set to `low`, and the other time with effort set to `high`.
#### Prompt 1 — Model 4 (`gpt-oss`)

| Metric                  | Low Effort | High Effort |
| ----------------------- | ---------- | ----------- |
| Average Time (s)        | 19.589     | 18.176      |
| Average Input Tokens    | 78.0       | 78.0        |
| Average Output Tokens   | 390.3      | 376.4       |
| Average Tokens / Second | 78.0       | 78.0        |
This model took quite a long time per run mostly because my gpu does not have enough vram, and it had to offload about 8gb into system memory. Other than that, I was quite surprised that the high effort setting actually reduced the total output tokens in general, and also made the model run faster on average.


#### Prompt 1 — Model 1 (`gpt-5-nano`)

| Metric                   | Low Effort | High Effort |
| ------------------------ | ---------- | ----------- |
| Average Time (s)         | 2.104      | 2.174       |
| Average Input Tokens     | 17.0       | 17.0        |
| Average Output Tokens    | 179.6      | 192.8       |
| Average Tokens / Second  | 17.0       | 17.0        |
| Average Reasoning Tokens | 128.0      | 147.2       |

For this result, I was surprised at how little of a difference there was between the low reasoning effort and the high reasoning effort. It does appear that the average reasoning tokens used differ by about 15%, but the average time was almost identical, just increasing by 0.07 seconds for the high effort reasoning

#### Prompt 2 — Model 1 (`gpt-5-nano`)

| Metric                   | Low Effort | High Effort |
| ------------------------ | ---------- | ----------- |
| Average Time (s)         | 4.646      | 5.063       |
| Average Input Tokens     | 83.0       | 83.0        |
| Average Output Tokens    | 567.8      | 607.4       |
| Average Tokens / Second  | 83.0       | 83.0        |
| Average Reasoning Tokens | 396.8      | 416.0       |


This prompt was much more complex than the first, and required much more of an output to fufill the prompt. As a result, it appears that over the 20 runs, the average time for the high effort reasoning was significantly more time, and the average output tokens were also significantly higher. However, the average reasoning tokens are only about 20 apart. This is likely due to the fact that the higher reasoning model was more likely to just give a longer and more detailed output in response to the prompt.

#### Prompt 2 — Model 4 (`gpt-oss`)

| Metric                  | Low Effort | High Effort |
| ----------------------- | ---------- | ----------- |
| Average Time (s)        | 51.747     | 47.454      |
| Average Input Tokens    | 144.0      | 144.0       |
| Average Output Tokens   | 1029.0     | 968.1       |
| Average Tokens / Second | 144.0      | 144.0       |
The output from here is mostly inconclusive, I just wanted to see how the oss model would do for this problem.

This was mostly in an attempt to discover the cost difference, both in time and tokens, between low and high reasoning. I conclude my findings by saying that in the instances that I tested, the difference was not very significant, especially on simpler problems. I conclude that if the reasoning increases the quality of the answer ssignificantly then it is most likely worth the cost.