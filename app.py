import sys, requests, json
import time

# header for all coms
headers = {
    "Content-Type": "application/json"
}

# sending link to api
params_ = {
    "apiKey": "emgn85jkankhknmwpjotm1jgkt8abedovkk54zqqw05trqec9cts3mf1x70d2haj",
    "urlInfo": {"url": "https://www.twitch.tv"}
    }

response_job = requests.post("https://developers.bolster.ai/api/neo/scan/", headers=headers, data=json.dumps(params_))
res_text = json.loads(response_job.text)

# checking if the API request was successful
if response_job.status_code != 200:
    print([0, f"Error sending API request:{response_job.text}"]) #0 => code for error
    sys.exit()

# getting results back
params_ = {
    "apiKey": "emgn85jkankhknmwpjotm1jgkt8abedovkk54zqqw05trqec9cts3mf1x70d2haj",
    "jobID": res_text["jobID"], 
    "insights": True
    }

# setting a maximum wait time for the API to process the request
max_wait_time = 30 # seconds
start_time = time.time()
sleep_time = 0.5

while True:
    time.sleep(sleep_time) # wait <sleep_time> seconds between each request
    response_final = requests.post("https://developers.bolster.ai/api/neo/scan/status", headers=headers, data=json.dumps(params_))
    res_final_text = json.loads(response_final.text)
    if res_final_text["status"] == "DONE":
        print([1, res_final_text]) #1 => code for successful results
        break
    if time.time() - start_time > max_wait_time:
        print([0, f"Error: API request timed out after {max_wait_time} seconds"]) #0 => code for error
        sys.exit()