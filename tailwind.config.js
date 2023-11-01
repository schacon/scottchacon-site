module.exports = {
  content: [
    './_drafts/**/*.html',
    './_includes/**/*.html',
    './_layouts/**/*.html',
    './_posts/*.md',
    './*.md',
    './*.html',
  ],
  theme: {
    fontFamily: {
      'sans': ['Inter', 'sans-serif'],
      'serif': ['Georgia', 'Cambria', "Times New Roman", 'Times', 'serif'],
      'mono': ['Roboto mono', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'Monaco', 'Consolas', "Liberation Mono", "Courier New", 'monospace'],
      'blog': ['Inter'],
    },
    theme: {
      extend: {},
    },
  },
  plugins: []
}
