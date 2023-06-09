# SlackLLMChatBot

To utilize this chatbot, you will need to download Ngrok and Docker. 

Ngrok is needed to access the Slack server remotely, while Docker is required for effective use of Redis, which is the vectorized database used. The best way to download docker would be using: https://www.docker.com/
Once docker is downloaded, you can run the Redis server through the following command: docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest

I would reccommend using the approach mentioned above for Redis because one of the modules RediSearch does not operate well locally on Mac. The Docker container is able to mitigate that issue. 

You will also have to download these libraries:
langchain==0.0.123, openai==0.27.2, redis==4.5.3, numpy, pandas, gdown

ngrok http 3000
docker run -d --name redis-stack-server -p 6379:6379 redis/redis-stack-server:latest
