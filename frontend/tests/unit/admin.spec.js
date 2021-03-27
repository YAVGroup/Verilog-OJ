import { mount } from "@vue/test-utils";
import admin from "@/components/mainpage/admin";
import Vue from "vue";
import ElementUI from "element-ui";

Vue.use(ElementUI);

describe("admin", () => {
  const wrapper = mount(admin, {
    data() {
      return {
        type: 1,
        isadmin: true,
        canshow: false,
        loading: true,
      };
    },
  });

  it("has a created hook", () => {
    expect(typeof admin.created).toBe("function");
  });

  var msg = "添加题目";
  it("renders the correct markup: " + msg, () => {
    expect(wrapper.html()).toContain(msg);
    // expect(wrapper.text()).toMatch(msg);
  });

  it("has a button", () => {
    expect(wrapper.find("button").exists()).toBe(true);
  });

  // it('button should increment the count', () => {
  //   expect(wrapper.vm.count).toBe(0)
  //   const button = wrapper.find('button')
  //   button.trigger('click')
  //   expect(wrapper.vm.count).toBe(1)
  // })
});
