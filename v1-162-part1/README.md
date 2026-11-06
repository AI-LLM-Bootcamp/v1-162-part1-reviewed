# 164-rag-for-pdfs-v2

## Update note: current OpenAI models

* The original project is very good for learning the concept, and it worked
  with the OpenAI models available when the course was recorded:
  `gpt-4-1106-preview` to answer and `text-embedding-ada-002` for the embeddings.
* OpenAI has since retired `gpt-4-1106-preview`. With the current models, we
  would do it like this: `gpt-6-luna`, a small, fast and affordable model. It is
  defined once, in the `MODEL` constant of `app/rag_chain.py`.
* Recent OpenAI models only accept `temperature=1`, so the model sets it
  explicitly (the original used `temperature=0`).
* `text-embedding-ada-002` still works, but OpenAI now presents
  `text-embedding-3-small` as its current small embedding model. It is defined
  in the `EMBEDDING_MODEL` constant, and it must be the same in
  `app/rag_chain.py` and in `rag-data-loader/rag_load_and_process.py`.
  If you loaded the PDFs before with the old model, run
  `rag_load_and_process.py` again to rebuild the vectors.
* Recent models think before they answer, so there may be a short pause before
  the first words appear.
* Check available models at developers.openai.com/api/docs/deprecations.

## Setting up the project with Poetry

This project uses Python 3.11.4 and Poetry 1.8.2, like the other classic
projects of the course. The commands below use `poetry-1.8.2`, the name you get
if you installed Poetry with pipx and `--suffix=-1.8.2`. If your Poetry 1.8.2
command is just `poetry`, use that instead.

1. Go to the project folder (the one with `pyproject.toml`):

   ```bash
   cd v1-162-part1
   ```

2. Tell Poetry to create the virtual environment with Python 3.11.4:

   ```bash
   pyenv local 3.11.4
   poetry-1.8.2 env use $(pyenv which python)
   ```

3. Install the dependencies (the versions are fixed in `poetry.lock`):

   ```bash
   poetry-1.8.2 install
   ```

4. Activate the virtual environment:

   ```bash
   poetry-1.8.2 shell
   ```

5. Create a file called `.env` in the project folder with your OpenAI key
   (you can copy `.env.example` and rename it). Write it without quotes or spaces:

   ```
   OPENAI_API_KEY=sk-...
   ```

   The `.env` file is not uploaded to GitHub (it is in `.gitignore`), so you
   have to create it after downloading the project. Check that it exists with `ls -a`.

With the virtual environment active, the rest of the commands of the lesson
(`python rag_load_and_process.py`, `langchain serve`...) work as shown in the videos.

## Installation

Install the LangChain CLI if you haven't yet

```bash
pip install -U langchain-cli
```

## Adding packages

```bash
# adding packages from 
# https://github.com/langchain-ai/langchain/tree/master/templates
langchain app add $PROJECT_NAME

# adding custom GitHub repo packages
langchain app add --repo $OWNER/$REPO
# or with whole git string (supports other git providers):
# langchain app add git+https://github.com/hwchase17/chain-of-verification

# with a custom api mount point (defaults to `/{package_name}`)
langchain app add $PROJECT_NAME --api_path=/my/custom/path/rag
```

Note: you remove packages by their api path

```bash
langchain app remove my/custom/path/rag
```

## Setup LangSmith (Optional)
LangSmith will help us trace, monitor and debug LangChain applications. 
LangSmith is currently in private beta, you can sign up [here](https://smith.langchain.com/). 
If you don't have access, you can skip this section


```shell
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=<your-api-key>
export LANGCHAIN_PROJECT=<your-project>  # if not specified, defaults to "default"
```

## Launch LangServe

```bash
langchain serve
```

## Running in Docker

This project folder includes a Dockerfile that allows you to easily build and host your LangServe app.

### Building the Image

To build the image, you simply:

```shell
docker build . -t my-langserve-app
```

If you tag your image with something other than `my-langserve-app`,
note it for use in the next step.

### Running the Image Locally

To run the image, you'll need to include any environment variables
necessary for your application.

In the below example, we inject the `OPENAI_API_KEY` environment
variable with the value set in my local environment
(`$OPENAI_API_KEY`)

We also expose port 8080 with the `-p 8080:8080` option.

```shell
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8080:8080 my-langserve-app
```
