 For this assignment, I decided to improve the calls to the vector database from hw 2b by using a sub agent which would interprate the user's query and craft a custom string to embed for querrying the vector database. This is my prompt that the sub-agent had:

```text
"Your purpose is to take the user's query along with the relevent history and
craft a query to an embedding model for retiveving the information for the main agent in a RAG style acrchitecture"

Your output will be a plaintext string that will accuratly and efficiantly be used to embedd then
query the vector database to help answer the user's question
```

Some of the challenges I ran into while completeting this assignment was that I had a hard time figuring out where to start, especially while working with old code that I didn't fully understand in the first place. It took me a while to understand what was going on in the original code enough to be able to modify it without messing everything up. In the end, the modification ended up being pretty simple, but it still was not easy to come to that point. 

The additional agent that I have formatting user's queries was effective and did work in retreving documents from the database, but there are some possible improvements that I would make if I were to work more on this problem. For instance, the sub agent did not have access to the history of the main agent, so when I asked follow up questions, the sub agent did not do a good job of including the right information in the vector db query. Another improvement I would make is rewriting the agent code to be able to use gpt-3.5-turbo to further reduce the cost and increase the speed of the vector db queries.