<template>
  <div style="overflow: auto" >
    <div v-html="renderedHTML" class="markdown-default"></div>
  </div>
</template>

<script>
var md = require('markdown-it')({
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
    mdSource: String
  },
  data() {
    return {};
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
