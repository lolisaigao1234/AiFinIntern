Based on the following prompt, help me to generate a new markdown file that includes a detailed plan on how to implement the project. Initiate a CLAUDE.md file as the main memory file. The project is to create a AI-driven Quant Trading Bot that can analyze market data, make predictions, and execute trades automatically. The bot should be able to learn from historical data and adapt its strategies over time. The AI would use the Interactive Brockers API for trading and data retrieval. The project will be structured in several phases, including research, development, testing, and deployment. 

Before implementing any code, please provide a detailed plan in markdown files for each decision, so it is traceable and easier to debug.

For each new change, please update the CLAUDE.md file with the reasoning behind the change, the expected outcome, and any potential risks or challenges. This will help ensure that all team members are aligned and that the project is well-documented. Also, make sure that each change gets its own subdirectory in the project structure, with clear documentation and code comments explaining the purpose and functionality of each component.

Try to delegate and divide the work, and utilize subagents to handle specific tasks. For example, one subagent can focus on data retrieval and preprocessing, while another can handle the trading logic and execution.

You should also include a section inside the CLAUDE.md that outlines the overall architecture of the trading bot, including the different components and how they interact with each other. This will help ensure that the project is well-organized and that all team members are on the same page.

Finally, make sure to include a section on testing and validation, outlining how you will test the bot's performance and ensure that it is making accurate predictions and executing trades correctly. This should include both unit tests for individual components and integration tests for the entire system.

@Code/order.py and @Code/test.py are the two test python files that I used to test on Interactive Brokers API and the trading logic. The main file will be @Code/main.py which will contain the core logic of the trading bot.

The aim of the project:
%==================== PROJECTS (OPTIONAL) ====================
\section{\textbf{Projects}}
\vspace{-0.4mm}
\resumeSubHeadingListStart

\resumeProject
  {Tax and Portfolio Reconciliation System (Independent Project)} 
  {Tools: Python, Pandas, Interactive Brokers API, ChatGPT/Claude}
  {October 2024 - Ongoing}
  {}
\resumeItemListStart
  \item Extended the AiFinSphere internship's scope to \textbf{simulate broker operations}, performing trades and automatically calculating tax liabilities, capital gains, and wash-sale implications.
  \item \textbf{Reconciled} transaction data with real-time market data, generating daily statements for trade P\&L and associated tax entries.
  \item Used \textbf{Generative AI} (ChatGPT, Claude) to swiftly interpret intricate US tax guidelines and confirm alignment with standard accounting practices.
  \item Produced comprehensive documentation detailing data processing logic, focusing on \textbf{tax considerations and compliance} best practices.
\resumeItemListEnd
