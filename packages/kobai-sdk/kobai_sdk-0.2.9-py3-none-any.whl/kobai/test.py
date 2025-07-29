import llm_config, ai_query

llm_config = llm_config.LLMConfig(api_key="sV9LuoA5n0PwqggMXOYMhhZlt56FpgnMXFohimPhD7Ug3CnBLbO8JQQJ99ALACYeBjFXJ3w3AAABACOGZm8X", llm_provider="azure_openai")
llm_config.get_azure_ad_token()
ai_query.followup_question_1(question="abc", data={}, question_name="sample", llm_config=llm_config)