<br />
<div align="center">
  <a href="https://github.com/Honeypotters/PandorasBox">
    <img src="website/public/RoundedLogo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Pandora's Box</h3>

  <p align="center">
    Pandora's Box is an AI honey-pot that utilises a fine-tuned version of distilgpt2. It comes with a convenient web interface where you can easily find all the relevant information about the requests it receives. Additionally under backend/.env users can add their free Gemini API key which will automatically classify requests as to whether or not they are malicious.
    <br />
    It should be noted that this project was made as a part of a weekend hackathon, it is not yet completed and will be further developed in the future.
    <br />
    <a href="https://github.com/Honeypotters/PandorasBox/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/Honeypotters/PandorasBox/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

## Getting Started


### Prerequisites

- npm

  ```sh
  npm install npm@latest -g
  ```

- pip
  ```sh
  pip install -r requirements.txt
  ```

## Usage
For further classification of logs, a Gemini API key can be added here:
- .env
  ```sh
  PandorasBox/backend/.env
  ```

To start up Pandora's Box manually requires a few parts:
- Server
  ```sh
  go run ./backend/server.go ./backend/stats.go
  ```
- Web Interface
  ```sh
  cd website
  npm run dev
  ```
- LLM
  ```sh
  ./llm/model/use_model_flask.py
  ```

Or to start up Pandora's Box through docker:
- ```sh
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

[contributors-shield]: https://img.shields.io/github/contributors/Honeypotters/PandorasBox.svg?style=for-the-badge
[contributors-url]: https://github.com/Honeypotters/PandorasBox/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Honeypotters/PandorasBox.svg?style=for-the-badge
[forks-url]: https://github.com/Honeypotters/PandorasBox/network/members
[stars-shield]: https://img.shields.io/github/stars/Honeypotters/PandorasBox.svg?style=for-the-badge
[stars-url]: https://github.com/Honeypotters/PandorasBox/stargazers
[issues-shield]: https://img.shields.io/github/issues/Honeypotters/PandorasBox.svg?style=for-the-badge
[issues-url]: https://github.com/Honeypotters/PandorasBox/issues
[license-shield]: https://img.shields.io/github/license/Honeypotters/PandorasBox.svg?style=for-the-badge
[license-url]: https://github.com/Honeypotters/PandorasBox/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Python.js]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[Go.js]: https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white
[Go-url]: https://golang.org/
[CSS.js]: https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white
[CSS-url]: https://developer.mozilla.org/en-US/docs/Web/CSS
[JavaScript.js]: https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black
[JavaScript-url]: https://developer.mozilla.org/en-US/docs/Web/JavaScript