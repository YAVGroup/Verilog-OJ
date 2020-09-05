import { mount } from "@vue/test-utils";
import contestannounce from "@/register";
import Vue from "vue";
import ElementUI from "element-ui";

Vue.use(ElementUI);

describe("register", () => {
  const wrapper = mount(contestannounce, {
    data () {
      return {
        dialogRegisterVisible: true,
        form: {
          username: "",
          password: "",
          confirm: "",
          last_name: "",
          first_name: "",
          email: ""
        }
      };
    },
  });

  var msg = '请重复密码';
  it("renders the correct markup: " + msg, () => {
    expect(wrapper.html()).toContain(msg);
    // expect(wrapper.text()).toMatch(msg);
  });

  it("has a button", () => {
    expect(wrapper.find("button").exists()).toBe(true);
  });

  it('button should show correct answer', () => {
    const button = wrapper.find('button')
    button.trigger('click')
    expect(wrapper.text()).toMatch('确认密码');
  })
});
