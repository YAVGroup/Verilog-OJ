<template>
  <div style="overflow: auto" >
    <div v-html="renderedHTML" class="markdown-default"></div>
  </div>
</template>

<script>

// See: https://www.npmjs.com/package/markdown-it-for-inline
// Also, play with https://markdown-it.github.io/ for token stream examples
let mdTokIterator = require('markdown-it-for-inline');

let md = require('markdown-it')({
  html:         false,        // Enable HTML tags in source
  xhtmlOut:     false,        // Use '/' to close single tags (<br />).
                              // This is only for full CommonMark compatibility.
  breaks:       true,        // Convert '\n' in paragraphs into <br>
  langPrefix:   'language-',  // CSS language prefix for fenced blocks. Can be
                              // useful for external highlighters.
  linkify:      false,        // Autoconvert URL-like text to links

  // Enable some language-neutral replacement + quotes beautification
  // For the full list of replacements, see https://github.com/markdown-it/markdown-it/blob/master/lib/rules_core/replacements.js
  typographer:  false,

  // Double + single quotes replacement pairs, when typographer enabled,
  // and smartquotes on. Could be either a String or an Array.
  //
  // For example, you can use '«»„“' for Russian, '„“‚‘' for German,
  // and ['«\xA0', '\xA0»', '‹\xA0', '\xA0›'] for French (including nbsp).
  quotes: '“”‘’',

  // Highlighter function. Should return escaped HTML,
  // or '' if the source string is not changed and should be escaped externally.
  // If result starts with <pre... internal wrapper is skipped.
  highlight: function (/*str, lang*/) { return ''; }
});


export default {
  name: "markdownIt",
  props: {
    mdSource: String,
    enableProblemRewrite: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {};
  },
  methods: {
    isNumeric(val) {
      return /^\d+$/.test(val);
    }
  },
  created() {
    if (this.enableProblemRewrite) {
      // Rewrite Rule 1: [OJ-QUESTION-ONELINE](79)
      //  or of the form [OJ-QUESTION-ONELINE](problem-name-url)
      //  (problem-name-url must contain non-digit characters)
      md.use(
        mdTokIterator,
        'oneline_question_replace',
        'link_open',
        function (tokens, idx) {
          // Make sure link contains only text
          if ((tokens[idx + 2].type !== 'link_close') ||
            (tokens[idx + 1].type !== 'text')) {
            return;
          }
          
          if (tokens[idx + 1].content == 'OJ-QUESTION-ONELINE') {
            let problemRef = tokens[idx].attrs[1];
            // if (isNumeric(problemRef)) {
            //   let problemID = Number(problemRef);

            // } else {
              
            // }
          }
      });
    }
  },
  computed: {
    renderedHTML: function () {
      return md.render(this.mdSource)
    },
  },
};
</script>

<style scoped>
.markdown-default {
  display: block;
  margin-top: 8px;
  margin-bottom: 8px;
  margin-block-end: 8px;
  margin-block-start: 8px;
}
</style>
