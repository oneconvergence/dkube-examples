# Create DKube Model

Goto Models and create a Model repository. Say with name “llama27b”

# Open the Jupyter notebook in DKube

- Copy download_create_version.py
- pip install -r requirements.txt
- export HUGGING_FACE_HUB_TOKEN=<token>

# Run the code

`python download_create_version.py --dkube_model="llama27b" --hf_repo_id="meta-llama/Llama-2-7b-hf`

The above command will return the version-index and version-id. Go to the DKubeUI and create dkube deployment.

# Create a dkube deployment for LLM

- Goto the `models`
- Select `llama27b`
- Click `deploy` button and fill the form with below details

`Serving Image` ocdr/kserve-vllmserver:openai
`Serving Port` 8080
`Serving Url Prefix` /v1
`Deploy using` select GPU
`Minimum Replicas` 1
`Minimum CPU` 1
`Maximum CPU` 4
`Minimum Memory` 50Gi
`Maximum Memory` 50Gi


# Wait for the deployment to running

- Copy the endpoint URL shown in DKube UI

# Sample test code

```
response = client.chat.completions.create(
  model="/mnt/models",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)
print(response)
```
