-- SQL script to initialize the database schema

-- Table for storing agent data
CREATE TABLE IF NOT EXISTS agents (
    agent_id UUID PRIMARY KEY,
    agent_name VARCHAR,
    api_key VARCHAR
);

-- Table for storing agent prompt data
CREATE TABLE IF NOT EXISTS agent_prompts (
    agent_id UUID PRIMARY KEY,
    system_prompt VARCHAR,
    user_prompt VARCHAR,
    json_mode BOOLEAN,
    CONSTRAINT fk_agent
        FOREIGN KEY(agent_id) 
            REFERENCES agents(agent_id)
            ON DELETE CASCADE
);

-- Table for storing user requests data
CREATE TABLE IF NOT EXISTS user_requests (
    request_id UUID PRIMARY KEY,
    agent_id UUID,
    message VARCHAR,
    CONSTRAINT fk_request_agent
        FOREIGN KEY(agent_id) 
            REFERENCES agents(agent_id)
            ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS convfinqa_data (
    id VARCHAR PRIMARY KEY,
    company VARCHAR,
    year VARCHAR,
    filename VARCHAR,
    pre_text VARCHAR,
    post_text VARCHAR,
    table_ori VARCHAR,
    question VARCHAR,
    steps VARCHAR,
    program VARCHAR,
    answer VARCHAR,
    exe_answer FLOAT,
    str_exe_answer VARCHAR
);