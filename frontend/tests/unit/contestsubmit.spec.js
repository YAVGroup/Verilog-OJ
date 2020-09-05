import { mount } from "@vue/test-utils";
import contestsubmit from "@/components/contest/contestsubmit";
import Vue from "vue";
import ElementUI from "element-ui";

Vue.use(ElementUI);

describe("contestsubmit", () => {
  it('has a created hook', () => {
    expect(typeof contestsubmit.created).toBe('function')
  })
});
