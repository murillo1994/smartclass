import adapter from '@sveltejs/adapter-node';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		// adapter-node builds a standalone Node server
		adapter: adapter()
	}
};

export default config;
