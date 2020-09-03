import { mount } from "@vue/test-utils";
import login from "@/login";
import Vue from "vue";
import ElementUI from "element-ui";

Vue.use(ElementUI);

describe("login", () => {
  const wrapper = mount(login, {
    data() {
      return {
        dialogLoginVisible: true,
        form: {
          username: "",
          password: ""
        }
      };
    }
  });

  var msg = '统一身份认证登录';
  it("renders the correct markup: " + msg, () => {
    expect(wrapper.html()).toContain(msg);
    expect(wrapper.text()).toMatch(msg);
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
