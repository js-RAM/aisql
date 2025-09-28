import json
from openai import OpenAI
import os
import sqlite3
from time import time

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

class Agent:
    def __init__(self, schemaPath, dataPath):
        if (os.path.exists(databasePath)):
            os.remove(databasePath)
        self.conn = sqlite3.connect(databasePath)
        self.cursor = self.conn.cursor()
        with (
                open(schemaPath) as schemaFile,
                open(dataPath) as dataFile
            ):
            self.schemaScript = schemaFile.read()
            dataScript = dataFile.read()
        self.cursor.executescript(self.schemaScript)
        self.cursor.executescript(dataScript)

        configPath = getPath("config.json")
        with open(configPath) as configFile:
            config = json.load(configFile)
        self.openAiClient = OpenAI(api_key = config["openai"])
    
    def execute(self, getSqlFromQuestionEngineeredPrompt):
        try:
            sqlSyntaxResponse = self.getChatGptResponse(getSqlFromQuestionEngineeredPrompt)
            sqlSyntaxResponse = self.getJustSql(sqlSyntaxResponse)
            queryRawResponse = str(agent.execute(sqlSyntaxResponse))
            friendlyResultsPrompt = "I asked a question: \"" + question +"\" and I queried this database " + self.schemaScript + " with this query " + sqlSyntaxResponse + ". The query returned the results data: \""+queryRawResponse+"\". Could you concisely answer my question using the results data?"
            friendlyResponse = self.getChatGptResponse(friendlyResultsPrompt)
            return [
                sqlSyntaxResponse,
                queryRawResponse,
                friendlyResponse
            ]
        except Exception as err:
            error = str(err)
            print(error)

    def executeSql(self, sqlStatement):
        self.cursor.execute(sqlStatement).fetchAll()

    def getChatGptResponse(self, content):
        stream = self.openAiClient.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
            stream=True,
        )

        responseList = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                responseList.append(chunk.choices[0].delta.content)

        result = "".join(responseList)
        return result

    def getJustSql(value):
        gptStartSqlMarker = "```sql"
        gptEndSqlMarker = "```"
        if gptStartSqlMarker in value:
            value = value.split(gptStartSqlMarker)[1]
        if gptEndSqlMarker in value:
            value = value.split(gptEndSqlMarker)[0]

        return value
    
    def getSchemaScript(self):
        return self.schemaScript
    
databasePath = getPath("db.sqlite")
schemaPath = getPath("schema.sql")
dataPath = getPath("data.sql")

agent = Agent(schemaPath, dataPath)
schemaScript = agent.getSchemaScript()

sqlOnly = " Give me a sqlite select statement that answers the question. Only respond with sqlite syntax. If there is an error do not explain it!"
strategies = {
    "zero_shot": schemaScript + sqlOnly,
    "single_domain_double_shot": (schemaScript +
        " Who doesn't have a way for us to text them? " +
        " \nSELECT p.person_id, p.name\nFROM person p\nLEFT JOIN phone ph ON p.person_id = ph.person_id AND ph.can_recieve_sms = 1\nWHERE ph.phone_id IS NULL;\n " +
        sqlOnly)
}
questions = [
    
]


for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    print("########################################################################")
    print(f"Running strategy: {strategy}")
    for question in questions:

        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("Question:")
        print(question)
        error = "None"
        try:
            getSqlFromQuestionEngineeredPrompt = strategies[strategy] + " " + question
            [sqlSyntaxResponse, queryRawResponse, friendlyResponse] = agent.execute(getSqlFromQuestionEngineeredPrompt)
            print("SQL Syntax Response:")
            print(sqlSyntaxResponse)
            print("Query Raw Response:")
            print(queryRawResponse)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question,
            "sql": sqlSyntaxResponse,
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)
