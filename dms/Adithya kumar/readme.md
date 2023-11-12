# Setup

1. open terminal
2. `git clone` the project
3. `cd` into directory with `package.json`
4. `$ npm install`
5. `$ npm start`

DM `@junaga` on [//discord.com/app](https://discord.com/app) for help

## personal notes

I answered the inital DM with

> 👋
>
> 1. who are you
> 1. what are you building
> 1. how much experience do you have
> 1. are you on windows, macos or linux

I should have asked this sooner

> are you building a website, or an app?

I refactored the entire codebase except `src/components/{Navbar.astro,Section.astro,Herosection.astro}`

## sharing code

when sending code back and forth you can either use discord file uploading or https://pastebin.com/

## zip file and large codebase

how much code is it? does it exced the discord upload limit? make sure to not include `node_modules/` everyone should run npm install themselfs, it will download all software in the `.json` file

## dynamic-content != responsive ui

responsive UI is not the same as dynamic content
you can learn everything about responsive UI here https://web.dev/learn/design

## client-side rendering

this is how you can do dynamic content with javascript without needing server-side rendering

```html
<p x-my-paragraph>Hello, World!</p>

<script>
	const selector = "p[x-my-paragraph]"
	const elements = document.querySelectorAll(selector)
	const element = elements[0]

	element.innerHTML = "Hello, Adithya kumar!"
</script>
```

When running an App, this [can be dangerous](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting). dont allow user-generated-content in `.innerHTML` or santizie it. see [web.dev/explore/secure](https://web.dev/explore/secure)

## astro is not for reactjs

is there any reason you have `npm:react` and `npm:axios` installed?
you can build an app in astro with vanilla HTML, CSS and JS without needing react

if you wanna use react i suggest you go with nextjs instead of astro
https://nextjs.org/
