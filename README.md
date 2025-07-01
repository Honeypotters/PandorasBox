<br />
<div align="center">
  <a href="https://github.com/Honeypotters/PandorasBox">
    <img src="website/public/RoundedLogo.png" alt="Logo" width="80" height="80">
  </a>

<h1 align="center">Pandora's Box</h1>

  <p align="center">
    Pandora's Box is an AI powered web honey-pot that utilises a fine-tuned version of distilgpt2. Through the use of an LLM, relevant, specific and personalised responses can be made to every incoming request. The project was built with Python, Golang and Typescript.
    <br />
    It should be noted that this project was made as a part of a weekend hackathon, it is not yet completed and will be further developed in the future.
    <br />
        <br />
    <a href="https://github.com/Honeypotters/PandorasBox/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Honeypotters/PandorasBox/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

## Prerequisites
#### Running without Docker:
- [Node and npm](https://nodejs.org/en/download)
- [Golang](https://go.dev/doc/install)
- [Python](https://www.python.org/downloads/) and [Pytorch](https://pytorch.org/get-started/locally/)

#### Running with Docker:
- [Docker and Docker Compose](https://docs.docker.com/compose/install/)



## Usage
1. Clone and cd into the repo
   ```sh
   git clone https://github.com/Honeypotters/PandorasBox.git && cd PandorasBox
   ```

2. Add a Gemini API key (get yours [here](https://aistudio.google.com/apikey)), this is required for basic classification and tagging of requests for the dashboard.
    ```sh
    backend/.env
    ```
3. To launch Pandora's Box without docker:
  - Server
    ```sh
    cd backend
    go get
    go run server.go stats.go
    ```
  - Web Interface
    ```sh
    cd website
    npm i
    npm run dev
    ```
  - LLM
    ```sh
    pip install -r ./llm/model/requirements.txt
    python3 ./llm/model/use_model_flask.py
    ```
  
    Or to start up Pandora's Box with docker:
    ```sh
     docker compose up -d
     ```

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors

<a href="https://github.com/Honeypotters/PandorasBox/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Honeypotters/PandorasBox" alt="contrib.rocks image" />
</a>

## License

Distributed under the project_license. See `LICENSE.txt` for more information.
