<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

</div>

<br />
<div align="center">
  <a href="https://github.com/smp46/smp46.me">
    <img src="https://cdn.statically.io/gh/smp46/smp46.me/nextjs/public/assets/pp.webp?q=85" alt="Logo" width="200" height="200" style="background-color:white; border-radius:50%">
  </a>

<h3 align="center">Personal Portfolio Website</h3>

  <p align="center">
    This repository contains the source code for my personal website. The website itself covers an intro to my projects and a little about who I am.
    <br />
    <br />
    <a href="https://smp46.me">View Live Site</a>
    ·
    <a href="https://github.com/smp46/smp46.me/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>

  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

![image](https://github.com/user-attachments/assets/244a3a0a-e0a6-4f7e-86ba-3761200c5c11)

### Features
* Written in Typescript with NextJS/React.
* Fully dynamic will scale (well) to most devices.
* Website is entirely statically generated.
* Articles (projects) are written in MDX format and get compiled automatically as a Github workflow.



### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![TailwindCSS][TailwindCSS]][Tailwind-url]
* [![TypeScript][TypeScript]][TypeScript-url]



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps:

### Prerequisites

* npm

### Usage

1.  Clone the repo
    ```sh
    git clone https://github.com/smp46/smp46.me.git
    ```
2.  Install NPM packages
    ```sh
    npm install
    ```

For developing `npm run dev`, this even works for adding MDX files. Navigating away then back to /projects, will refresh and get new files.

For building/generating a static site `npm run build`, find the website files in /out.

## How the Markdown stuff works
Painfully! It was a lot of banging my head against the wall using various guides and resources to reach my goal of *easier* article creation / updating. What ended up being the most helpful article was [this one by Colby Fayock](https://spacejelly.dev/posts/how-to-source-mdx-content-in-next-js-to-dynamically-create-pages-for-a-blog).

The end result is a relatively easy way to maintain and add articles/project write-ups. The process is as simple as:

1.  Write the article in Markdown(X) and copy it to the src/projects directory.
2.  Add the required fields to the top of the page, to extract a title and allow for categorising, meta tags etc. For example:
    ```
    ---
    title: "Portfolio Website"
    subtitle: "Building My Developer Portfolio with Next.js, MDX, and GitHub Actions"
    type: "personal"
    description: "A fully statically-generated personal portfolio built with Next.js, React, and TypeScript. It showcases projects, articles written in MDX, and a bit about me."
    keywords: "personal website, portfolio, Next.js, React, TypeScript, static site generation, MDX, GitHub Actions, web development, developer portfolio"
    github: "[https://github.com/smp46/smp46.me](https://github.com/smp46/smp46.me)"
    ---
    ```
3.  `git add . && git commit` And ta-dah, the Github workflow handles the compiling and then it goes live at [smp46.me/projects](https://smp46.me/projects).




<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` file for more information.




<!-- CONTACT -->
## Contact

Samuel P - me@smp46.me

Project Link: [https://github.com/smp46/smp46.me](https://github.com/smp46/smp46.me)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [othneildrew/Best-README-Template](https://github.com/othneildrew/Best-README-Template)
* [How To Source MDX Content In Next JS To Dynamically Create Pages For A Blog](https://spacejelly.dev/posts/how-to-source-mdx-content-in-next-js-to-dynamically-create-pages-for-a-blog)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/smp46/smp46.me.svg?style=for-the-badge
[contributors-url]: https://github.com/smp46/smp46.me/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/smp46/smp46.me.svg?style=for-the-badge
[forks-url]: https://github.com/smp46/smp46.me/network/members
[stars-shield]: https://img.shields.io/github/stars/smp46/smp46.me.svg?style=for-the-badge
[stars-url]: https://github.com/smp46/smp46.me/stargazers
[issues-shield]: https://img.shields.io/github/issues/smp46/smp46.me.svg?style=for-the-badge
[issues-url]: https://github.com/smp46/smp46.me/issues
[license-shield]: https://img.shields.io/github/license/smp46/smp46.me.svg?style=for-the-badge
[license-url]: https://github.com/smp46/smp46.me/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/smp46
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[TailwindCSS]: https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white
[Tailwind-url]: https://tailwindcss.com/
[TypeScript]: https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white
[TypeScript-url]: https://www.typescriptlang.org/


